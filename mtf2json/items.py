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
mapping the various names from the MTF files to new unified names. The
data for this module is stored in the CSV files of the 'data' folder.

NOTE: the rules in the CSV files are incomplete (e.g. the construction
rules are missing), therefore some items in there may seem identical but
still have an IS and Clan version. I've decided to keep separate entries
in the CSV data if there are separate string identifiers in the MTF files.
"""

from __future__ import annotations
import re
from importlib.resources import files as importfiles
import pandas as pd
from enum import StrEnum
from dataclasses import dataclass, field
from itertools import chain
from copy import deepcopy
from . import data


class ItemError(Exception):
    pass


class ItemNotFound(ItemError):
    pass


class DataError(Exception):
    pass


class ItemEnum(StrEnum):
    def __str__(self) -> str:
        # cleaner debug / error output
        return self.value

    def __repr__(self) -> str:
        return self.value


class ItemClass(ItemEnum):
    """The available item classes"""

    WEAPON = "Weapon"
    EQUIPMENT = "Equipment"


class ItemCategory(ItemEnum):
    """The available item categories"""

    # weapons
    ARTILLERY = "Artillery"
    BALLISTIC = "Ballistic"
    ENERGY = "Energy"
    PULSE = "Pulse"
    MISSILE = "Missile"
    SPECIAL = "Special"
    PHYSICAL = "Physical"
    # equipment
    AMMO_BIN = "Ammo Bin"
    ARMOR = "Armor"
    COCKPIT = "Cockpit"
    ELECTRONICS = "Electronics"
    ENGINE = "Engine"
    GYRO = "Gyro"
    MANEUVERABILITY = "Maneuverability"
    MISCELLANEOUS = "Miscellaneous"
    STRUCTURE = "Structure"
    TRANSPORT = "Transport"


class ItemTechBase(ItemEnum):
    """
    The available tech bases:
      "IS": item is exclusive to IS or has different rules than clan version (weight, damage, etc)
      "Clan": item is exclusive to clans or has different rules than IS version
      "All": item is available to all factions and the rules are identical
      "Unknown": we just don't know (yet)
    """

    IS = "IS"
    CLAN = "Clan"
    ALL = "All"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls: type[ItemTechBase], string: str) -> ItemTechBase:
        """
        Create an ItemTechBase instance from the given string.
        The string may be a valid ItemTechBase or not.
        """
        try:
            return cls[string]
        except KeyError:
            clean_string = string.strip()
            lower_string = clean_string.lower()
            if "inner sphere" in lower_string or clean_string.startswith("IS"):
                return cls.IS
            elif clean_string.startswith("Clan"):
                return cls.CLAN
            else:
                return cls.UNKNOWN


class MechTechBase(ItemEnum):
    """
    Extends the ItemTechBase class by allowing 'Mixed'.
    """

    # Python does not allow extending enums with members,
    # so we have to re-define them
    IS = ItemTechBase.IS
    CLAN = ItemTechBase.CLAN
    ALL = ItemTechBase.ALL
    UNKNOWN = ItemTechBase.UNKNOWN
    MIXED = "Mixed"

    @classmethod
    def from_string(cls: type[MechTechBase], string: str) -> MechTechBase:
        """
        Create a MechTechBase instance from the given string.
        The string may be a valid MechTechBase or not.
        """
        try:
            return cls[string]
        except KeyError:
            clean_string = string.strip()
            lower_string = clean_string.lower()
            if "inner sphere" in lower_string or clean_string.startswith("IS"):
                return cls.IS
            elif clean_string.startswith("Clan"):
                return cls.CLAN
            elif clean_string.startswith("Mixed"):
                return cls.MIXED
            else:
                return cls.UNKNOWN


class ItemTag(ItemEnum):
    """The available item tags"""

    OMNIPOD = "omnipod"
    ARMORED = "armored"
    OS = "OS"  # one-shot
    IOS = "I-OS"  # improved one-shot


class ItemEntry(ItemEnum):
    """
    The JSON entry type for an item. Only used for equipment, because:
    - we don't want all equipment to end up in the "equipment" section
      - e.g. armor and structure have their own sections
    - we want to have some equipment only once, others once with quantity
      (i.e. nr. of crit slos), e.g. jump jets and coolant pods
    - all weapons go into the 'weapons' section
    """

    IGNORE = "Ignore"  # don't add item to the 'equipment' section
    ONCE = "Once"  # add it once (no matter how many crit slots it occupies)
    ONCE_QTY = "OnceQty"  # add it once, with quantity (i.e. nr. of slots)
    WEAP_EQU = "WeapEqu"  # equipment item that is added as a weapon


@dataclass
class Item:
    """
    Identifies a piece of equipment or weapon by providing:
        - a name
        - a category
          - tuple of item class and type, e.g. ("weapon", "missile")
        - a tech base
          - "IS", "Clan" or "unknown" (if it can't be determined)
        - a list of MTF names
          - e.g. critical slot entries
        - an optional list of tags
          - e.g. ["omnipod", "armored"]
        - an optional size (in tons)
          - e.g. for 'cargo' and 'liquid storage' equipment
    """

    _name: str
    _category: tuple[ItemClass, ItemCategory]
    _tech_base: ItemTechBase
    _mtf_names: list[str]
    _entry: ItemEntry = ItemEntry.IGNORE
    # NOTE: we're using a list instead of a set because we
    # want to keep the order
    _tags: list[ItemTag] = field(default_factory=lambda: list())
    _size: float | None = None
    # a dict containing ammo types as keys and lists of MTF ammo strings as values,
    # e.g. { "Cluster" : ["IS LB 2-X Cluster Ammo"] }
    _ammo: dict[str, list[str]] = field(default_factory=lambda: dict())

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
        self._tech_base = tb

    @property
    def mtf_names(self) -> list[str]:
        return self._mtf_names

    @property
    def entry(self) -> ItemEntry:
        return self._entry

    @property
    def tags(self) -> list[ItemTag]:
        return self._tags

    def add_tag(self, tag: ItemTag) -> None:
        if tag not in self._tags:  # keep the tags unique
            self._tags.append(tag)
            self.validate()

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

    @property
    def ammo(self) -> dict[str, list[str]]:
        return self._ammo

    @ammo.setter
    def ammo(self, a: dict[str, list[str]]) -> None:
        self._ammo = a

    def add_ammo(self, ammo: str, mtf_ammo: list[str]) -> None:
        self._ammo[ammo] = mtf_ammo

    def __repr__(self) -> str:
        return f"[{self._name} |  {self._category} | {self._tech_base} | {self._tags}]"

    def validate(self) -> None:
        """Validate item category, tech base and tags"""
        if self._category[0] not in ItemClass:
            raise ItemError(f"Found invalid class '{self._category[0]}' in item {self}")
        if self._category[1] not in ItemCategory:
            raise ItemError(
                f"Found invalid category '{self._category[1]}' in item {self}"
            )
        if self._tech_base not in ItemTechBase:
            raise ItemError(
                f"Found invalid tech base '{self._tech_base}' in item {self}"
            )
        if self._entry not in ItemEntry:
            raise ItemError(f"Found invalid entry type '{self._entry}' in item {self}")
        for tag in self._tags:
            if tag not in ItemTag:
                raise ItemError(f"Found invalid tag '{tag}' in item {self}")

    def __post_init__(self) -> None:
        self.validate()


# global variables to store the items
equipment: list[Item] = []
weapons: list[Item] = []


def load_csv_data() -> None:
    """
    Load CSV data from the data folder and convert them into items.
    """
    global equipment, weapons
    if len(equipment) == 0 or len(weapons) == 0:
        # read CSV files and replace NaN with '' to make other operations easier
        try:
            with (importfiles(data) / "equipment.csv").open("r") as f:
                equipment_data = pd.read_csv(f, sep=";", skipinitialspace=True)
                equipment_data = equipment_data.fillna("")
            with (importfiles(data) / "weapons.csv").open("r") as f:
                weapons_data = pd.read_csv(f, sep=";", skipinitialspace=True)
                weapons_data = weapons_data.fillna("")
            with (importfiles(data) / "physical_weapons.csv").open("r") as f:
                physical_weapons_data = pd.read_csv(f, sep=";", skipinitialspace=True)
                physical_weapons_data = physical_weapons_data.fillna("")
        except Exception as ex:
            print(f"Reading CSV data failed with {ex!r}")
            raise DataError(ex)
        # create equipment items
        for index, row in equipment_data.iterrows():
            equipment.append(
                Item(
                    row["Name"],
                    (ItemClass.EQUIPMENT, row["Category"]),
                    row["Tech"],
                    [n.strip() for n in row["MTF"].split(",")],
                    ItemEntry(row["Entry"]),  # equipment has an "Entry" column
                )
            )
        # create ranged weapon items
        for index, row in weapons_data.iterrows():
            # If an item with the same name, category and tech_base exists,
            # don't add a new item. Instead, add an entry to the `ammo` list,
            # using to the `Ammo` and 'MTFAmmo' colum of the current item.
            # This makes sure that there's only one item per name and tech base
            # (see also "_select_item()"
            existing_item = next(
                (
                    item
                    for item in weapons
                    if item.name == row["Name"]
                    and item.category == (ItemClass.WEAPON, row["Category"])
                    and item.tech_base == row["Tech"]
                ),
                None,
            )
            if existing_item:
                existing_item.add_ammo(
                    row["Ammo"], [n.strip() for n in row["MTFAmmo"].split(",")]
                )
            else:
                item = Item(
                    row["Name"],
                    (ItemClass.WEAPON, row["Category"]),
                    row["Tech"],
                    [n.strip() for n in row["MTF"].split(",")],
                )
                # add the ammo (if any)
                if row["MTFAmmo"]:
                    mtf_ammo = [m.strip() for m in row["MTFAmmo"].split(",")]
                    item.add_ammo(row["Ammo"] or "Standard", mtf_ammo)
                weapons.append(item)
        # create physical weapon items
        for index, row in physical_weapons_data.iterrows():
            weapons.append(
                Item(
                    row["Name"],
                    (ItemClass.WEAPON, row["Category"]),
                    row["Tech"],
                    [n.strip() for n in row["MTF"].split(",")],
                )
            )


def get_item(mtf_name: str, tech_base: ItemTechBase | None = None) -> Item:
    """
    Return an item instance for the given MTF name. The returned item always contains the category.
    The tech_base will be determined from the data tables, extracted from the given mtf name or the
    given tech base will be used. Otherwise it will be "Unknown". However, this function only accepts
    tech bases that conform to the 'ItemTechBase' format.

    Tags will be added if the given MTF name also contains some (e.g. 'armored', 'omnipod', etc.)
    """
    global equipment, weapons

    def _get_tech_base(mtf_name: str) -> ItemTechBase:
        """Extract the tech base from the given string"""
        if mtf_name.startswith("IS"):
            return ItemTechBase.IS
        elif mtf_name.startswith("CL"):
            return ItemTechBase.CLAN
        elif "(IS)" in mtf_name:
            return ItemTechBase.IS
        elif "(Clan)" in mtf_name:
            return ItemTechBase.CLAN
        return ItemTechBase.UNKNOWN

    def _select_item(
        items: list[Item], mtf_name: str, tech_base: ItemTechBase | None = None
    ) -> Item:
        """
        Select the correct item from the given list, based on the tech base.

        Note that sometimes the given 'mtf_name' does not contain the tech base.
        E.g. "Machine Gun" can refer to "ISMG" or "CLMG". However, in that case
        the tech base is usually not required (it's only about the unified name).

        Also note that for mechs with a mixed tech base, it is NOT guaranteed
        that the MTF weapon names contain the tech base!
        """
        # 1. make sure that all names are identical (otherwise it's a bug)
        # Check the names of the items in the given list
        unique_names = {item.name for item in items}
        if len(unique_names) != 1:
            raise ItemError(f"Not all 'Name' values are identical in {unique_names}")

        # 2. use given tech base or extract it from the given MTF name
        tech_base = tech_base or _get_tech_base(mtf_name)

        # 3. if it's still unknown, select the first item but set 'Tech' to 'Unknown'
        if tech_base == ItemTechBase.UNKNOWN:
            res_item = items[0]
            res_item.tech_base = ItemTechBase.UNKNOWN
        # otherwise select the item based on the given tech base
        else:
            filtered_items = [item for item in items if item.tech_base == tech_base]
            if not filtered_items:
                raise ItemError(
                    f"Could not find item with tech base '{tech_base}' in {items}"
                )
            res_item = filtered_items[0]
        return res_item

    def _clean_name(mtf_name: str) -> str:
        """Strip the name of all irrelevant components"""
        # Remove ':SIZE:' and ':size:' and anything within parentheses.
        name = re.sub(
            r":size:\d*\.?\d*|\(.*?\)", "", mtf_name, flags=re.IGNORECASE
        ).strip()
        return name

    def _add_tags(item: Item, mtf_name: str) -> None:
        if "(armored)" in mtf_name.lower():
            item.add_tag(ItemTag.ARMORED)
        if "(omnipod)" in mtf_name.lower():
            item.add_tag(ItemTag.OMNIPOD)
        if "(I-OS)" in mtf_name or "(IOS)" in mtf_name:
            item.add_tag(ItemTag.IOS)
        if "(OS)" in mtf_name:
            item.add_tag(ItemTag.OS)

    def _add_size(item: Item, mtf_name: str) -> None:
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

    clean_name = _clean_name(mtf_name)
    # search for all items with the given MTF name
    items: list[Item] = []
    for i in chain(equipment, weapons):
        if clean_name in i.mtf_names:
            items.append(deepcopy(i))
    # not found
    if len(items) == 0:
        # not found
        raise ItemNotFound(f"MTF name '{clean_name}' not found in any item list.")
    # if more than one has been found, select one based on the tech base
    # -> this happens if the given MTF name is used for multiple items
    elif len(items) > 1:
        res_item = _select_item(items, mtf_name, tech_base)
    else:
        res_item = items[0]
    # extract and add tags (if any)
    _add_tags(res_item, mtf_name)
    # extract and add size (if any)
    _add_size(res_item, mtf_name)
    return res_item
