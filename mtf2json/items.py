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
This module is all about identifying, naming and categorizing individual
items (weapons and equipment). The goal is to have consistent names for
weapons and equipment in all JSON mech files. Unfortunately, this is
currently not the case in the MTF files, e.g. ECM Suites are sometimes
called "ECMSuite" and sometimes just "ECM" and so on. Therefore we're
mapping the various names from the MTF files to new unified names.

Each item is also assigned a unique key, that can later be used to
access additional data (e.g. damage values or special rules).
"""

import re
import pandas as pd
from dataclasses import dataclass, field
from typing import Literal, Final, get_args


class ItemError(Exception):
    pass


class ItemNotFound(ItemError):
    pass


class DataError(Exception):
    pass


# the available item classes
ItemClass = Literal["Weapon", "Equipment"]
valid_item_classes: Final[tuple[ItemClass, ...]] = get_args(ItemClass)
# the available item categories
ItemCategory = Literal[
    "Artillery",
    "Ballistic",
    "Energy",
    "Pulse",
    "Missile",
    "Special",
    "Physical",
    "Transport",
    "Electronics",
    "Maneuverability",
    "Miscellaneous",
]
valid_item_categories: Final[tuple[ItemCategory, ...]] = get_args(ItemCategory)

# The available tech bases
# "IS": item is exclusive to IS or has different rules than clan version (weight, damage, etc)
# "Clan": item is exclusive to clans or has different rules than IS version
# "All": item is available to all factions and the rules are identical
# "Unknown": we just don't know (yet)

# NOTE: the rules in the CSV files are incomplete (e.g. the construction rules
# are missing), therefore some items in there may seem identical but still have
# an IS and Clan version. I've decided to keep them separate if there are
# separate string identifiers in the MTF files.

ItemTechBase = Literal["IS", "Clan", "All", "Unknown"]
valid_item_tech_bases: Final[tuple[ItemTechBase, ...]] = get_args(ItemTechBase)
# the available item tags
ItemTag = Literal["omnipod", "armored"]
valid_item_tags: Final[tuple[ItemTag, ...]] = get_args(ItemTag)

# global variables to store the CSV data
equipment_data: pd.DataFrame
weapons_data: pd.DataFrame
physical_weapons_data: pd.DataFrame


@dataclass
class item:
    """
    Identifies a piece of equipment or weapon by providing:
        - a category
          - tuple of item class and type, e.g. ("weapon", "missile")
        - a name
        - a tech base
          - "IS", "Clan" or "unknown" (if it can't be determined)
        - an optional list of tags
          - e.g. ["omnipod", "armored"]
        - an optional size (in tons)
          - e.g. for 'cargo' and 'liquid storage' equipment
    """

    _name: str
    _category: tuple[ItemClass, ItemCategory]
    _tech_base: ItemTechBase = "Unknown"
    # NOTE: we're using a list instead of a set because we
    # want to keep the order
    _tags: list[ItemTag] = field(default_factory=lambda: list())
    _size: float | None = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def name_with_tags(self) -> str:
        if len(self._tags) > 0:
            return f"{self._name} [{' '.join(self._tags)}]"
        else:
            return self._name

    @property
    def category(self) -> tuple[ItemClass, ItemCategory]:
        return self._category

    @property
    def tech_base(self) -> ItemTechBase:
        return self._tech_base

    @tech_base.setter
    def tech_base(self, tb: ItemTechBase) -> None:
        if tb not in valid_item_tech_bases:
            raise ItemError(f"Got invalid tech base '{tb}' for item {self}")
        self._tech_base = tb

    @property
    def tags(self) -> list[ItemTag]:
        return self._tags

    def add_tag(self, tag: ItemTag) -> None:
        if tag not in valid_item_tags:
            raise ItemError(f"Got invalid tag '{tag}' for item {self}")
        if tag not in self._tags:  # keep the tags unique
            self._tags.append(tag)

    @property
    def size(self) -> float | None:
        return self._size

    @size.setter
    def size(self, s: float) -> None:
        self._size = s

    @property
    def size_str(self) -> str | None:
        """Return size and unit as a string"""
        if not self._size:
            return None
        # convert to float and then to int if it's a whole number, otherwise keep as float
        # -> e.g. "1.0" becomes "1t", but "2.5" becomes "2.5t"
        string_size = (
            str(int(self._size)) if self._size.is_integer() else str(self._size)
        )
        return f"{string_size}t"  # so far size is always measured in tons

    def __repr__(self) -> str:
        return f"{self._name} |  {self._category} | {self._tech_base} | {self._tags}]"

    def validate(self) -> bool:
        return (
            len(self.category) == 2
            and self.category[0] in valid_item_classes
            and self.category[1] in valid_item_categories
            and self.tech_base in valid_item_tech_bases
            and not any(tag not in valid_item_tags for tag in self.tags)
        )

    def __post_init__(self) -> None:
        if not self.validate():
            raise ItemError(f"Validation failed for item '{str(self)}'")


def load_csv_data() -> None:
    """
    Load CSV data from the data folder into global variables.
    """
    global equipment_data, weapons_data, physical_weapons_data
    try:
        equipment_data = pd.read_csv("mtf2json/data/equipment.csv", sep=";")
        weapons_data = pd.read_csv("mtf2json/data/weapons.csv", sep=";")
        physical_weapons_data = pd.read_csv(
            "mtf2json/data/physical_weapons.csv", sep=";"
        )
    except Exception as ex:
        print(f"Reading CSV data failed with {ex!r}")
        raise DataError(ex)


def load_item(clean_mtf_name: str) -> tuple[pd.DataFrame, ItemClass]:
    """
    Searches for the given MTF name in the loaded CSV files.
    Returns all matching rows as a tuple.
    """
    global equipment_data, weapons_data, physical_weapons_data

    # each cell in the MTF column contains a list of comma-separated strings
    # that we have to compare against
    equipment_matches = equipment_data[
        equipment_data["MTF"].apply(
            lambda x: any(clean_mtf_name == name.strip() for name in str(x).split(","))
        )
    ]
    if not equipment_matches.empty:
        return (equipment_matches, "Equipment")
    weapons_matches = weapons_data[
        weapons_data["MTF"].apply(
            lambda x: any(clean_mtf_name == name.strip() for name in str(x).split(","))
        )
    ]
    if not weapons_matches.empty:
        return (weapons_matches, "Weapon")
    physical_weapons_matches = physical_weapons_data[
        physical_weapons_data["MTF"].apply(
            lambda x: any(clean_mtf_name == name.strip() for name in str(x).split(","))
        )
    ]
    if not physical_weapons_matches.empty:
        return (physical_weapons_matches, "Weapon")
    raise ItemNotFound(f"MTF name '{clean_mtf_name}' not found in any CSV table.")


def get_item(mtf_name: str) -> item:
    """
    Return an item instance for the given MTF name. The returned item always contains the category.
    The tech_base will be determined from the given name, if possible. Otherwise it will be "unknown".
    Tags will be added if the given MTF name also contains some (e.g. 'armored', 'omnipod', etc.)
    """

    def _get_tech_base(mtf_name: str) -> str:
        """Extract the tech base from the given string"""
        if mtf_name.startswith("IS"):
            return "IS"
        elif mtf_name.startswith("CL"):
            return "Clan"
        elif "(IS)" in mtf_name:
            return "Clan"
        elif "(Clan)" in mtf_name:
            return "Clan"
        return "Unknown"

    def _select_item(item_data: pd.DataFrame, mtf_name: str) -> pd.DataFrame:
        """
        Select the correct item from the given DataFrame, based on the tech base.
        Only called if 'load_item' returns more than one result row.
        """
        # 1. make sure that all names are identical (otherwise it's a bug)
        if item_data["Name"].nunique() != 1:  # Check if there's more than 1 unique name
            raise ItemError("Not all 'Name' values are identical in {item_data}")

        # 2. try to extract the tech base from the given MTF name
        tech_base = _get_tech_base(mtf_name)

        # 3. if it's still unknown, select the first item but set 'Tech' to 'Uknown'
        if tech_base == "Unknown":
            item_data = item_data.iloc[:1]
            item_data.at[item_data.index[0], "Tech"] = "Unknown"
        # otherwise select the item based in the extracted tech base
        else:
            item_data = item_data[item_data["Tech"].str.contains(tech_base)]
            if item_data.empty:
                raise ItemError(
                    f"Could not find item with tech base '{tech_base}' in {item_data}"
                )
        return item_data

    def _clean_name(mtf_name: str) -> str:
        """Strip the name of all irrelevant components"""
        # Remove ':SIZE:' and ':size:' and anything within parentheses.
        name = re.sub(
            r":size:\d*\.?\d*|\(.*?\)", "", mtf_name, flags=re.IGNORECASE
        ).strip()
        return name

    def _add_tags(item: item, mtf_name: str) -> None:
        if "(armored)" in mtf_name.lower():
            item.add_tag("armored")
        if "(omnipod)" in mtf_name.lower():
            item.add_tag("omnipod")

    def _add_size(item: item, mtf_name: str) -> None:
        """Extract the size value from the given string"""
        size: str | None = None
        if ":size:" in mtf_name.lower():
            # split the string
            size = re.split(":size:", mtf_name, flags=re.IGNORECASE)[1]
        if not size:
            # check for legacy-style sizes like '(5 tons)' or '(1 ton)'
            match = re.search(r"\((\d+(\.\d+)?)\s*tons?\)", mtf_name, re.IGNORECASE)
            if match:
                size = match.group(1)
        if size:
            # remove everything that is not part of the number, i.e. not a digit or a dot
            size = re.sub(r"[^\d.]", "", size)
            item.size = float(size)

    # load the item data (based on the clean name)
    clean_name = _clean_name(mtf_name)
    item_data, item_class = load_item(clean_name)
    # if more than one has been found, select one based on the tech base
    # -> this happens if the given MTF name is used for multiple items
    if len(item_data) > 1:
        item_data = _select_item(item_data, mtf_name)
        if len(item_data) != 1:
            print(item_data)
            raise ItemError(
                f"Item selection did not return unique result for MTF name '{mtf_name}"
            )
    # create the item based on the selected CSV data
    res_item = item(
        item_data.at[0, "Name"],
        (item_class, item_data.at[0, "Category"]),
        item_data.at[0, "Tech"],
    )
    # extract and add tags (if any)
    _add_tags(res_item, mtf_name)
    # extract and add size (if any)
    _add_size(res_item, mtf_name)
    return res_item
