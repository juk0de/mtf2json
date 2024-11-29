# https://github.com/juk0de/mtf2json
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module handles all equipment that has to be added to the
'Weapons and Equipment' section of the record sheet by storing
it in a dedicated 'equipment' section in the JSON data.

Because that kind of equipment is scattered across the various
critical slot entries in the MTF files (with different equipment
having different format, e. g. some contain a ':SIZE:' value),
it is added after the JSON conversion, in a separate step.

Another issue is that some MTF files contain some equipment in the
'Weapons' sections while others don't. This module is responsible
for cleaning that mess up a bit.
"""

from typing import Any
from .items import item, get_item, ItemTag, ItemNotFound


class EquipmentError(Exception):
    pass


def add_equipment_section(mech_data: dict[str, Any]) -> None:
    """
    The main function of this module. Creates an "equipment" section
    in the mech_data that contains all relevant equipment, grouped
    into categories.
    """

    def _add_item(mech_data: dict[str, Any], location: str, _item: item) -> None:
        """
        Add the given equipment item the mech_data dict.
        """

        # create the equipment section if it doesn't exist
        if "equipment" not in mech_data:
            mech_data["equipment"] = []

        # check if the given equipment already exists in the given location.
        if not any(
            entry["location"] == location and entry["name"] == _item.name
            for entry in mech_data["equipment"]
        ):
            # add it if not
            new_entry: dict[str, str | list[ItemTag]] = {
                "name": _item.name,
                "location": location,
                "type": _item.category[1],
            }
            if _item.tags:
                new_entry["tags"] = _item.tags
            if _item.size_str:
                new_entry["size"] = _item.size_str
            mech_data["equipment"].append(new_entry)

    for location, slots in mech_data["critical_slots"].items():
        for key, mtf_name in slots.items():
            if not mtf_name:
                continue
            # get item (including tags, tech_base and size)
            # -> ignore unnknown items
            try:
                _item = get_item(mtf_name)
            except ItemNotFound:
                continue
            # for now we limit this to sized equipment
            # -> they have to be added to the weapons/equipment list in the record sheet
            if _item.category[0] == "equipment" and _item.size is not None:
                # add the equipment to the list (if not yet done)
                _add_item(mech_data, location, _item)
                # overwrite the old slot name
                # -> include tags (e.g. 'omnipod') if available, but omit size
                mech_data["critical_slots"][location][key] = _item.name_with_tags
