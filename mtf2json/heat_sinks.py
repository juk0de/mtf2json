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


def add_heat_sinks(key: str, value: str, mech_data: dict[str, Any]) -> None:
    """
    Add heat sinks section.

    Heat sinks are stored as a flat key:value pair in the MTF file, with the value containing
    both type and quantity of heat sinks, e.g.:
        ```
        heat sinks:10 IS Double
        ```
    We separate heat sink type and quantity, using the first ` ` as delimiter, and store them
    in a JSON section like this:
        ```
        "heat_sinks": {
            "quantity": 10,
            "type": "IS Double"
        }
        ```
    Some MTF files also contain the nr. of base chassis heat sinks:
        ```
        base chassis heat sinks:12
        ```
    Those are also added to the JSON "heat_sinks" section.
    """
    # add heat sinks section if not present
    if "heat_sinks" not in mech_data:
        mech_data["heat_sinks"] = {}
    heat_sinks_section: dict[str, int | str] = mech_data["heat_sinks"]

    if key == "heat_sinks":
        quantity, type_ = value.split(" ", 1)
        heat_sinks_section["quantity"] = int(quantity)
        heat_sinks_section["type"] = type_.strip()
    elif key == "base_chassis_heat_sinks":
        heat_sinks_section["base_chassis_heat_sinks"] = int(value)
    else:
        raise ConversionError(f"Got illegal key '{key}' for heat sinks")
