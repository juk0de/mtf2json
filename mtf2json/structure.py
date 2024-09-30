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


def add_structure_type(value: str, mech_data: dict[str, Any]) -> None:
    """
    Add the structure type.

    The MTF `Structure:` key has a value that either represents the structure type only, e.g.:
        ```
        Structure:Standard
        ```
    or the tech base + type (separated by the first ` `), e.g.:
        ```
        structure:IS Standard
        structure:IS Endo Steel
        structure:Clan Endo Steel
        ```
    Similar to the `armor` section, we store all information in the `structure` JSON section, e.g.:
        ```
        "structure": {
            ...
            "type": "Standard",
            "tech_base": "Inner Sphere"
        }
        ```
        Note that `tech_base` is optional and we convert 'IS' to 'Inner Sphere', in order to be
        consistent with the `armor` section names.
        ```
    """
    # create structure section if not present
    if "structure" not in mech_data:
        mech_data["structure"] = {}

    # extract tech base and type if present
    parts = value.split(" ", 1)
    if parts[0] in ["IS", "Clan"]:
        tech_base = "Inner Sphere" if parts[0] == "IS" else parts[0]
        type_ = parts[1] if len(parts) > 1 else ""
    else:
        tech_base = None
        type_ = value

    # Populate structure section
    mech_data["structure"]["type"] = type_.strip()
    if tech_base:
        mech_data["structure"]["tech_base"] = tech_base.strip()


def add_biped_structure_pips(mech_data: dict[str, Any]) -> None:
    """
    Add the structure pips for biped mechs based on the tonnage.
    The structure are not part of an MTF file. Instead, they are
    computed and added later (see 'Mech.java'). We add them to
    the JSON structure for convenience, like this:
        ```
        "structure": {
            ...
            "left_arm": {
                "pips": 17
             },
            "right_arm": {
                "pips": 17
            },
            "left_torso": {
                "pips": 21
            },
            "right_torso": {
                "pips": 21
            },
            "center_torso": {
                "pips": 31
            },
            "head": {
                "pips": 3
            },
            "left_leg": {
                "pips": 21
            },
            "right_leg": {
                "pips": 21
            }
        }
        ```
    """
    # Static list of pips for each weight
    # The list order is: [Head, Center Torso, L/R Torso, L/R Arm, L/R Leg]
    biped_weight_pips = {
        10: [3, 4, 3, 1, 2],
        15: [3, 5, 4, 2, 3],
        20: [3, 6, 5, 3, 4],
        25: [3, 8, 6, 4, 6],
        30: [3, 10, 7, 5, 7],
        35: [3, 11, 8, 6, 8],
        40: [3, 12, 10, 6, 10],
        45: [3, 14, 11, 7, 11],
        50: [3, 16, 12, 8, 12],
        55: [3, 18, 13, 9, 13],
        60: [3, 20, 14, 10, 14],
        65: [3, 21, 15, 10, 15],
        70: [3, 22, 15, 11, 15],
        75: [3, 23, 16, 12, 16],
        80: [3, 25, 17, 13, 17],
        85: [3, 27, 18, 14, 18],
        90: [3, 29, 19, 15, 19],
        95: [3, 30, 20, 16, 20],
        100: [3, 31, 21, 17, 21],
        105: [4, 32, 22, 17, 22],
        110: [4, 33, 23, 18, 23],
        115: [4, 35, 24, 19, 24],
        120: [4, 36, 25, 20, 25],
        125: [4, 38, 26, 21, 26],
        130: [4, 39, 27, 21, 27],
        135: [4, 41, 28, 22, 28],
        140: [4, 42, 29, 23, 29],
        145: [4, 44, 31, 24, 31],
        150: [4, 45, 32, 25, 32],
        155: [4, 47, 33, 26, 33],
        160: [4, 48, 34, 26, 34],
        165: [4, 50, 35, 27, 35],
        170: [4, 51, 36, 28, 36],
        175: [4, 53, 37, 29, 37],
        180: [4, 54, 38, 30, 38],
        185: [4, 56, 39, 31, 39],
        190: [4, 57, 40, 31, 40],
        195: [4, 59, 41, 32, 41],
        200: [4, 60, 42, 33, 42],
    }
    if "mass" not in mech_data:
        raise ConversionError(
            "Mech data must contain 'mass' to calculate structure pips."
        )

    mass = mech_data["mass"]
    if mass not in biped_weight_pips:
        raise ConversionError(f"Unsupported mech mass: {mass}")

    pips = biped_weight_pips[mass]
    mech_data["structure"]["head"] = {"pips": pips[0]}
    mech_data["structure"]["center_torso"] = {"pips": pips[1]}
    mech_data["structure"]["left_torso"] = {"pips": pips[2]}
    mech_data["structure"]["right_torso"] = {"pips": pips[2]}
    mech_data["structure"]["left_arm"] = {"pips": pips[3]}
    mech_data["structure"]["right_arm"] = {"pips": pips[3]}
    mech_data["structure"]["left_leg"] = {"pips": pips[4]}
    mech_data["structure"]["right_leg"] = {"pips": pips[4]}
