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

import re
from typing import Any
from .items import item, get_item, ItemTag


class EquipmentError(Exception):
    pass


def add_equipment_section(mech_data: dict[str, Any]) -> None:
    """
    The main function of this module. Creates an "equipment" section
    in the mech_data that contains all relevant equipment, grouped
    into categories.
    """
    __add_sized_equipment(mech_data)


def __add_sized_equipment(mech_data: dict[str, Any]) -> None:
    """
    Some equipment contains a `:SIZE:` or `:size:` parameter (e.g. storage equipment).
    This function searches for such equipment in the critial slots, adds the equipment
    to the 'equipment' section and removes the size string from the crit slot entries.
    """

    def _size(value: str) -> str:
        """
        Extract the size from the given str.

        Example:

        - input value : "Liquid Storage (OMNIPOD):SIZE:1.0 (ARMORED)"
        - return value: "1t"
        """
        # split the string
        size = re.split(":size:", value, flags=re.IGNORECASE)[1]
        # remove stuff in parentheses from the size (e.g. '(ARMORED)' or '(OMNIPOD)')
        size = re.sub(r"\(.*?\)", "", size).strip()
        # remove everything that is not part of the number, i.e. not a digit or a dot
        size = re.sub(r"[^\d.]", "", size)
        # convert to float and then to int if it's a whole number, otherwise keep as float
        # -> e.g. ":SIZE:1.0" becomes "1t", but ":SIZE:2.5" becomes "2.5t"
        size = str(int(float(size))) if float(size).is_integer() else str(float(size))
        return f"{size}t"

    def _add_sized_equipment(
        mech_data: dict[str, Any], location: str, mtf_name: str, size: str
    ) -> item:
        """
        Add the given equipment of given size to the mech_data dict.
        """
        sized_item = get_item(mtf_name)
        if sized_item.category[0] != "equipment":
            raise EquipmentError(f"Item {mtf_name} is not an equipment!")
        # create the equipment section if it doesn't exist
        if "equipment" not in mech_data:
            mech_data["equipment"] = {}
        if sized_item.category[1] not in mech_data["equipment"]:
            mech_data["equipment"][sized_item.category[1]] = []

        # check if the given equipment already exists in the given location.
        if not any(
            entry["location"] == location and entry["name"] == sized_item.name
            for entry in mech_data["equipment"][sized_item.category[1]]
        ):
            # add it if not
            new_entry: dict[str, str | list[ItemTag]] = {
                "name": sized_item.name,
                "location": location,
                "size": size,
            }
            if sized_item.tags:
                new_entry["tags"] = list(sized_item.tags)
            mech_data["equipment"][sized_item.category[1]].append(new_entry)
        return sized_item

    # look for slot entries containing ':size:' or ':SIZE:'
    for location, slots in mech_data["critical_slots"].items():
        for key, mtf_name in slots.items():
            if mtf_name and ":size:" in mtf_name.lower():
                size = _size(mtf_name)
                # add the equipment to the list (if not yet done)
                sized_item = _add_sized_equipment(mech_data, location, mtf_name, size)
                # overwrite the old slot name
                # -> including tags (e.g. 'omnipod') if available
                mech_data["critical_slots"][location][key] = sized_item.name_with_tags
