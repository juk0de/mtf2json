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
from typing import Any
from .error import ConversionError


def add_quirk(value: str, mech_data: dict[str, Any]) -> None:
    """
    Add mech quirk.

    The MTF file can contain multiple 'quirk' entries that we merge
    into a single JSON 'quirks' section.
    """
    if "quirks" not in mech_data:
        mech_data["quirks"] = []
    mech_data["quirks"].append(value)


def add_weapon_quirk(value: str, mech_data: dict[str, Any]) -> None:
    """
    Add a weapon quirk.

    Weapon quirks are stored in the MTF files like this:
        ```
        weaponquirk:mod_weapons:RT:2:CLERMediumLaser
        weaponquirk:mod_weapons:RT:3:CLMG
        weaponquirk:mod_weapons:RT:4:CLMG
        ```
    The given value is already missing the `weaponquirk:` key and thus has the following structure:
        ```
        <quirk_name>:<location>:<slot_number>:<weapon_name>
        ```
    This function turns each given weapon quirk into a dictionary and adds it to the given list.
    The locations are translated according to the 'loc_names' dictionary.
    The weapon_quirks_section eventually looks like this:
        ```
        "weapon_quirks": [
            {
                "quirk": "mod_weapons",
                "weapon": "CLERMediumLaser",
                "location": "right_torso",
                "slot": 2,
            }
            {
                "quirk": "mod_weapons",
                "weapon": "CLMG",
                "location": "right_torso",
                "slot": 3,
            }
            {
                "quirk": "mod_weapons",
                "weapon": "CLMG",
                "location": "right_torso",
                "slot": 2,
            }
        ]
        ```
    """
    loc_names = {
        "HD": "head",
        "LA": "left_arm",
        "RA": "right_arm",
        "CT": "center_torso",
        "LT": "left_torso",
        "RT": "right_torso",
        "LL": "left_leg",
        "RL": "right_leg",
    }
    # add weapon quirks section if not present
    if "weapon_quirks" not in mech_data:
        mech_data["weapon_quirks"] = []
    weapon_quirks_section: list[dict[str, str | int]] = mech_data["weapon_quirks"]

    parts = value.split(":")
    if len(parts) != 4:
        raise ConversionError(f"Invalid weapon quirk format: {value}")

    quirk_name, location, slot_number, weapon_name = parts
    location = loc_names.get(location, location.lower())

    weapon_quirks_section.append(
        {
            "quirk": quirk_name,
            "weapon": weapon_name,
            "location": location,
            "slot": int(slot_number),
        }
    )
