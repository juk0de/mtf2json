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
from .items import ItemTechBase


def add_engine(value: str, mech_data: dict[str, Any]) -> None:
    """
    Add the engine section.

    An MTF engine entry looks like this:
        ```
        engine:400 XL (Clan) Engine
        ```

    We extract name, type and tech base and create a JSON section like this:
        ```
        "engine": {
            "name": "400 XL",
            "type": "XL",
            "tech_base": "Clan"
        }
        ```
    Supported engine types are:
        - Compact
        - Light
        - XL
        - XXL
        - Standard (if no other type matches)

    Note that some MTF files contain buggy engine entries with 2 tech bases, e.g. 'Turkina U':
        ```
        engine:400 XL (Clan) Engine
        ```
    We work around this as follows:
        - choose the tech base that matches the mech tech base (`mech_data['tech_base']`)
        - if none matches (e.g. because mech tech base is 'Mixed'), choose the first one in the string
    """

    # create engine section if it doesn't exist
    if "engine" not in mech_data:
        mech_data["engine"] = {}
    engine_section: dict[str, str] = mech_data["engine"]

    # determine engine type
    if "compact" in value.lower():
        engine_type = "Compact"
    elif "light" in value.lower():
        engine_type = "Light"
    elif "XXL" in value:
        engine_type = "XXL"
    elif "XL" in value:
        engine_type = "XL"
    else:
        engine_type = "Standard"

    # extract engine name by removing the tech base
    name = re.sub(r"\(.*?\)", "", value).strip()
    # replace resulting double spaces with single space
    name = re.sub(r"\s{2,}", " ", name)

    # extract tech base
    tech_bases = [
        ItemTechBase.from_string(tb) for tb in re.findall(r"\((.*?)\)", value)
    ]
    # select mech tech base if no engine tech base is found
    if len(tech_bases) == 0:
        tech_base = mech_data["tech_base"]
    else:
        # work around buggy entries with multiple tech bases by setting it to the
        # mech tech base if one of the extracted tech bases matches (otherwise
        # choose the first extracted tech base)
        tech_base = next(
            (tb for tb in tech_bases if tb == mech_data["tech_base"]), tech_bases[0]
        )

    # populate engine section
    engine_section["name"] = name
    engine_section["type"] = engine_type
    engine_section["tech_base"] = tech_base
