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


def add_rules_level(value: str, mech_data: dict[str, Any]) -> None:
    """
    Add the given rules level and also a rules level string, to be used as the
    "Rules Level" record sheet entry. The string is determined based on the
    code in 'SimpleTechLevel.java', which converts the compound tech levels to
    simplified rules level.

    However, those levels are NOT always identical to those from the MUL.
    E.g. the 'Atlas II AS7-D-H (Devlin)' is listed as 'Experimental' in MUL,
    but has rules level 'Standard' in MegaMek.
    """
    introductory_levels = [0]
    standard_levels = [1, 2, 3, 4]
    advanced_levels = [5, 6]
    experimental_levels = [7, 8]
    unofficial_levels = [9, 10]

    # add verbatim rules level (integer)
    mech_data["rules_level"] = int(value)

    # add rules level string based on 'rules_level' number
    if mech_data["rules_level"] in introductory_levels:
        mech_data["rules_level_str"] = "Introductory"
    elif mech_data["rules_level"] in standard_levels:
        mech_data["rules_level_str"] = "Standard"
    elif mech_data["rules_level"] in advanced_levels:
        mech_data["rules_level_str"] = "Advanced"
    elif mech_data["rules_level"] in experimental_levels:
        mech_data["rules_level_str"] = "Experimental"
    elif mech_data["rules_level"] in unofficial_levels:
        mech_data["rules_level_str"] = "Unofficial"
    else:
        raise ConversionError(f"Found invalid rules_level: {mech_data['rules_level']}")
