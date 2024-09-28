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
from typing import Any, cast
from .error import ConversionError


def add_fluff(key: str, value: str, mech_data: dict[str, Any]) -> None:
    value = __remove_p_tags(value)
    """
    Add the given fluff key and value.

    Some of the fluff keys can appear multiple times in an MTF file, e.g.:
        ```
        systemmanufacturer:CHASSIS:Star League
        systemmanufacturer:ENGINE:GM
        systemmanufacturer:ARMOR:Starshield
        systemmanufacturer:TARGETING:Dalban
        systemmanufacturer:COMMUNICATIONS:Dalban
        systemmode:ENGINE:380
        systemmode:CHASSIS:XT
        systemmode:TARGETING:HiRez-B
        systemmode:COMMUNICATIONS:Commline
        ```
    All fluff keys that appears more than once have "subkeys", i.e. the given
    value contains another key / value pair separated by `:`. We create a JSON
    subsection for each "primary" key and add the "subkey" entries to it, e.g.:
        ```
        "systemmanufacturer": {
            "chassis": "Star League",
            "engine": "GM",
            "armor": "Starshield"
            "targeting": "Dalban",
            "communication": "Dalban"
        },
        "systemmode": {
            "engine": "380",
            "chassis": "XT",
            "targeting": "HiRez-B",
            "communications": "Commline"
        },
        ...
    The following keys can contain lists as values (separated by `,`):
        ```
        manufacturer
        primaryfactory
        ```
    In this case we store the values as JSON lists, e.g.:
        ```
        "manufacturer": [
            "Defiance Industries",
            "Hegemony Research and Development Department",
            "Weapons Division"
        ],
        "primaryfactory": [
            "Hesperus II",
            "New Earth"
        ],
        ...
        ```
    All other keys and values are added verbatim.
    """
    # add fluff section if not present
    if "fluff" not in mech_data:
        mech_data["fluff"] = {}
    fluff_section: dict[str, str | list[str] | dict[str, str]] = mech_data["fluff"]

    # the key is already in the fluff section
    # -> it's a subsection
    if key in fluff_section:
        try:
            subkey, subvalue = value.split(":", 1)
        except ValueError:
            raise ConversionError(
                f"Key '{key}' already exists in the fluff section but value is missing the ':' delimiter!"
            )
        if isinstance(fluff_section[key], dict):
            cast(dict, fluff_section[key])[subkey.lower()] = subvalue.strip()
        else:
            raise ConversionError(
                f"Tried to add '{subkey}:{subvalue}' to fluff section '{key}', but '{key}' is not a dictionary!"
            )
    # the key is new
    else:
        # value contains a subkey
        # -> create a new subsection
        if ":" in value:
            subkey, subvalue = value.split(":", 1)
            # but ONLY if the subkey is all UPPERCASE, e.g.:
            # ```
            # systemmanufacturer:CHASSIS:Republic-R
            # ```
            # Otherwise we could turn some of the longer text strings
            # (that sometimes contain `:`) into dicts.
            if subkey.isupper():
                fluff_section[key] = {subkey.lower(): subvalue.strip()}
            else:
                fluff_section[key] = value
        # value contains a list
        elif key in ["manufacturer", "primaryfactory"]:
            fluff_section[key] = [item.strip() for item in value.split(",")]
        # simple value
        else:
            fluff_section[key] = value


def __remove_p_tags(text: str) -> str:
    """
    Remove <p>, <P>, </p> and </P> tags from the given text.
    """
    return (
        text.replace("<p>", "")
        .replace("</p>", "")
        .replace("<P>", "")
        .replace("</P>", "")
    )
