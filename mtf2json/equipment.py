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
from .items import get_item


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

    def get_name_and_size(value: str) -> tuple[str, str]:
        """
        Split the given string using ':SIZE:' as the delimiter (case insensitive).
        Return the name of the item and the size in tons.
        """
        # remove stuff in parentheses first (e.g. '(ARMORED)' or '(OMNIPOD)')
        value = re.sub(r"\(.*?\)", "", value).strip()
        # now split the string
        res = re.split(":size:", value, flags=re.IGNORECASE)
        # convert to float and then to int if it's a whole number, otherwise keep as float
        size = (
            str(int(float(res[1])))
            if float(res[1]).is_integer()
            else str(float(res[1]))
        )
        return (res[0].strip(), f"{size}t")

    def add_sized_equipment(
        mech_data: dict[str, Any], location: str, slot_name: str, size: str
    ) -> None:
        """
        Add the given equipment of given size to the mech_data dict.
        """
        item = get_item(slot_name)
        if item.category[0] != "equipment":
            raise EquipmentError(f"Item {slot_name} is not an equipment!")
        # create the equipment section if it doesn't exist
        if "equipment" not in mech_data:
            mech_data["equipment"] = {}
        if item.category[1] not in mech_data["equipment"]:
            mech_data["equipment"][item.category[1]] = []

        # check if the given equipment already exists in the given location.
        if any(
            entry["location"] == location and entry["name"] == item.name
            for entry in mech_data["equipment"][item.category[1]]
        ):
            return
        # add it if not
        new_entry = {"name": item.name, "location": location, "size": size}
        mech_data["equipment"][item.category[1]].append(new_entry)

    # look for slot entries containing ':size:' or ':SIZE:'
    for location, slots in mech_data["critical_slots"].items():
        for key, slot_value in slots.items():
            if slot_value and ":size:" in slot_value.lower():
                slot_name, size = get_name_and_size(slot_value)
                # overwrite the old slot name
                # FIXME: add tags like 'omnipod' and 'armored' if available
                mech_data["critical_slots"][location][key] = slot_name
                # add the equipment to the list (if not yet done)
                add_sized_equipment(mech_data, location, slot_name, size)
