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
import re
from typing import Any


def add_weapon(value: str, mech_data: dict[str, Any]) -> None:
    """
    Add a new weapon. If value is empty, it's just the beginning of the section.

    The MTF weapon section starts with the key 'Weapons:', followed by the
    total nr. of weapons (which we don't store in JSON). The lines below the
    section start line each describe one weapon slot (until the next section
    starts). Each weapon slot line consists of:

    - the weapon quantity (optional), ended by ` `
    - the weapon name, ended by `,`
    - the location, ended either by `,`, end of line or `(R)`
    - if the location is followed by `(R)` on the same line, the `facing` of
      the weapon changes to `rear`, otherwise `facing` is always `front`
    - ammo quantity, consisting of the word `Ammo`, followed by `:` and the
      quantity value

    Here's an MTF example containing all of the described features (Atlas AS7-K):
        ```
        Weapons:6
        1 ISGaussRifle, Right Torso, Ammo:16
        1 ISLRM20, Left Torso, Ammo:12
        1 ISERLargeLaser, Left Arm
        1 ISERLargeLaser, Right Arm
        2 ISMediumPulseLaser, Center Torso (R)
        1 ISAntiMissileSystem, Left Arm, Ammo:12
        ```
    And here's how the JSON looks like (a list of dictionaries):
        ```
        "weapons": [
            {
                "name": "ISGaussRifle",
                "location": "right_torso",
                "facing": "front",
                "quantity": 1,
                "ammo": 16

            },
            {
                "name": "ISLRM20",
                "location": "left_torso",
                "facing": "front",
                "quantity": 1,
                "ammo": 12
            },
            {
                "name": "ISERLargeLaser",
                "location": "left_arm",
                "facing": "front",
                "quantity": 1
            },
            {
                "name": "ISERLargeLaser",
                "location": "right_arm",
                "facing": "front",
                "quantity": 1
            },
            {
                "name": "ISMediumPulseLaser",
                "location": "center_torso",
                "facing": "rear",
                "quantity": 2
            },
            {
                "name": "ISAntiMissileSystem",
                "location": "left_arm",
                "facing": "front",
                "quantity": 1,
                "ammo": 12
            }
        ],

        ```
    """

    # create section if it doesn't exist
    if "weapons" not in mech_data:
        mech_data["weapons"] = []
    # value is empty if it's just the section start
    if not value:
        return
    weapons_section: list[dict[str, str | int]] = mech_data["weapons"]

    weapon_data: dict[str, str | int]

    # Extract weapon quantity if present
    quantity_match = re.match(r"(\d+)\s+", value)
    if quantity_match:
        quantity = int(quantity_match.group(1))
        value = value[quantity_match.end() :]
    else:
        quantity = 1

    # Extract weapon name
    weapon_name, value = value.split(",", 1)
    weapon_name = weapon_name.strip()

    # Extract location and facing
    location_match = re.match(r"([^,]+)(,|$)", value)
    if location_match:
        location = location_match.group(1).strip()
        value = value[location_match.end() :]
        facing = "rear" if "(R)" in location else "front"
        location = location.replace("(R)", "").strip()
    else:
        location = value.strip()
        facing = "front"

    # Extract ammo quantity if present
    ammo_match = re.search(r"Ammo:(\d+)", value)
    if ammo_match:
        ammo = int(ammo_match.group(1))
    else:
        ammo = None

    # Populate weapon data
    weapon_data = {
        "name": weapon_name,
        "location": location.lower().replace(" ", "_"),
        "facing": facing,
        "quantity": quantity,
    }
    if ammo is not None:
        weapon_data["ammo"] = ammo

    # Add weapon data to the weapon section
    weapons_section.append(weapon_data)


def merge_weapons(mech_data: dict[str, Any]) -> None:
    """
    Sometimes the MTF format contains individual entries for identical weapons in the
    same location, e.g.:
        ```
        Small Pulse Laser, Left Arm
        Small Pulse Laser, Left Arm
        ```
    These will result in separate entries in the JSON file:
        ```
        {
            "name": "Small Pulse Laser",
            "location": "left_arm",
            "facing": "front",
            "quantity": 1
        },
        {
            "name": "Small Pulse Laser",
            "location": "left_arm",
            "facing": "front",
            "quantity": 1
        },
        ```
    This function merges all weapons with identical name, location and facing to a single entry,
    so it looks like this:
        ```
        {
            "name": "Small Pulse Laser",
            "location": "left_arm",
            "facing": "front",
            "quantity": 2
        },
        ```
    """
    weapon_dict: dict[tuple[str, str, str], dict[str, str | int]] = {}
    for weapon in mech_data.get("weapons", []):
        key = (weapon["name"], weapon["location"], weapon["facing"])
        if key in weapon_dict:
            weapon_dict[key]["quantity"] += weapon["quantity"]
        else:
            weapon_dict[key] = weapon

    mech_data["weapons"] = list(weapon_dict.values())
