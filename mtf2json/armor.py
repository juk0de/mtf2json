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


def add_armor_type(value: str, mech_data: dict[str, Any]) -> None:
    """
    Add the armor type.

    The MTF `Armor:` key in is a bit of a mess: it can contain a value that only describes
    the type of armor, e.g:
        ```
        Armor:Standard Armor
        ```
    or the type + tech base (delimited by `(...)`), e.g.:
        ```
        Armor:Standard(Inner Sphere)
        ```
    Furthermore the type description is not consistent. E.g. it can be `Standard` or
    `Standard Armor`. We try to clean up the mess a bit by storing all available
    information in the JSON 'armor' section, while also choosing a consistent type string:
        ```
        "armor": {
            "type": "Standard",
            "tech_base: "Inner Sphere"
            ...
        }
        ```
    Note that `tech_base` is optional (only added if there's a string in `(...)`) and
    that the term 'Armor' has been removed from the type string.
    """
    # create armor section if it doesn't exist
    if "armor" not in mech_data:
        mech_data["armor"] = {}
    armor_type_section: dict[str, str | dict[str, Any]] = mech_data["armor"]

    # Extract type and tech base if present
    if "(" in value and ")" in value:
        type_, tech_base = value.split("(", 1)
        tech_base = tech_base.rstrip(")")
    else:
        type_ = value
        tech_base = None

    # Clean up type string
    type_ = type_.replace(" Armor", "").strip()

    # Populate armor section
    armor_type_section["type"] = type_
    if tech_base:
        armor_type_section["tech_base"] = tech_base.strip()


def add_armor_locations(key: str, value: str, mech_data: dict[str, Any]) -> None:
    """
    Add individual armor locations to the given `armor_section` dictionary.
    The armor pips are stored as individual keys in an MTF file:
        ```
        LA armor:21
        RA armor:21
        LT armor:30
        RT armor:30
        CT armor:40
        HD armor:9
        LL armor:26
        RL armor:26
        RTL armor:10
        RTR armor:10
        RTC armor:17
        ```
    We're structuring the values in the JSON 'armor' section like this:
        ```
        "armor": {
            ...
           "left_arm": {
             "pips": 21
           },
           "right_arm": {
             "pips": 21
           },
           "left_torso": {
             "front": {
               "pips": 30
             },
             "rear": {
               "pips": 10
             },
           },
           "right_torso": {
             "front": {
               "pips": 30
             },
             "rear": {
               "pips": 10
             },
           },
           "center_torso": {
             "front": {
               "pips": 40
             },
             "rear": {
               "pips": 17
             },
           },
           "head": {
             "pips": 9
           }
           "left_leg": {
             "pips": 26
            },
           "right_leg": {
             "pips": 26
           }
        }
        ```
    In case of patchwork armor, the location keys MAY contain subkeys
    describing the armor type in that location, e.g.:
        ```
        HD Armor:Standard(IS/Clan):9
        LL Armor:Reactive(Inner Sphere):34
        RTL Armor:8
        ```
    In that case, we add a `type` key to the affected location:
        ```
        "head": {
          "pips": 9,
          "type": "Standard(IS/Clan)"
        }
        "left_leg": {
          "pips": 26,
          "type": "Reactive(Inner Sphere)"
        },
        ```
    """
    # create armor section if it doesn't exist
    if "armor" not in mech_data:
        mech_data["armor"] = {}
    armor_section: dict[str, Any] = mech_data["armor"]

    # Extract subkeys if present
    parts = value.split(":")
    if len(parts) == 2:
        armor_type = parts[0].strip()
        pips_value = int(parts[1].strip())
    else:
        armor_type = None
        pips_value = int(parts[0].strip())

    # center torso (front and rear)
    if key in ["ct_armor", "rtc_armor"]:
        if "center_torso" not in armor_section:
            armor_section["center_torso"] = {}
        side = "front" if key == "ct_armor" else "rear"
        if side not in armor_section["center_torso"]:
            armor_section["center_torso"][side] = {}
        armor_section["center_torso"][side]["pips"] = pips_value
        if armor_type:
            armor_section["center_torso"][side]["type"] = armor_type
    # right torso (front and rear)
    elif key in ["rt_armor", "rtr_armor"]:
        if "right_torso" not in armor_section:
            armor_section["right_torso"] = {}
        side = "front" if key == "rt_armor" else "rear"
        if side not in armor_section["right_torso"]:
            armor_section["right_torso"][side] = {}
        armor_section["right_torso"][side]["pips"] = pips_value
        if armor_type:
            armor_section["right_torso"][side]["type"] = armor_type
    # left torso (front and rear)
    elif key in ["lt_armor", "rtl_armor"]:
        if "left_torso" not in armor_section:
            armor_section["left_torso"] = {}
        side = "front" if key == "lt_armor" else "rear"
        if side not in armor_section["left_torso"]:
            armor_section["left_torso"][side] = {}
        armor_section["left_torso"][side]["pips"] = pips_value
        if armor_type:
            armor_section["left_torso"][side]["type"] = armor_type
    else:
        if key not in armor_section:
            armor_section[key] = {}
        armor_section[key]["pips"] = pips_value
        if armor_type:
            armor_section[key]["type"] = armor_type
