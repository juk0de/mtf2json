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
from dataclasses import dataclass, field
from itertools import chain
from typing import Literal, Final, get_args
from copy import deepcopy


class ItemError(Exception):
    pass


# the available item classes
ItemClass = Literal["weapon", "equipment"]
valid_item_classes: Final[tuple[ItemClass, ...]] = get_args(ItemClass)
# the available item types
ItemType = Literal[
    "physical",
    "ballistic",
    "energy",
    "pulse",
    "missile",
    "special",
    "storage",
    "electronics",
    "maneuverability",
    "miscellaneous",
]
valid_item_types: Final[tuple[ItemType, ...]] = get_args(ItemType)
# the available tech bases
ItemTechBase = Literal["IS", "Clan", "unknown"]
valid_item_tech_bases: Final[tuple[ItemTechBase, ...]] = get_args(ItemTechBase)
# the available item tags
ItemTag = Literal["omnipod", "armored"]
valid_item_tags: Final[tuple[ItemTag, ...]] = get_args(ItemTag)


@dataclass
class item:
    """
    Identifies a piece of equipment or weapon by providing:
        - a numerical key
        - a category
          - tuple of item class and type, e.g. ("weapon", "missile")
        - a name
        - a list with known MTF names
          - e.g. critical slot entries
        - a tech base
          - "IS", "Clan" or "unknown" (if it can't be determined)
        - an optional list of tags
          - e.g. ["omnipod", "armored"]
    """

    _key: int
    _name: str
    _category: tuple[ItemClass, ItemType]
    _mtf_names: list[str]
    _tech_base: ItemTechBase = "unknown"
    # NOTE: we're using a list instead of a set because we
    # want to keep the order
    _tags: list[ItemTag] = field(default_factory=lambda: list())

    @property
    def key(self) -> int:
        return self._key

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
    def category(self) -> tuple[ItemClass, ItemType]:
        return self._category

    @property
    def mtf_names(self) -> list[str]:
        return self._mtf_names

    @property
    def tech_base(self) -> ItemTechBase:
        return self._tech_base

    @tech_base.setter
    def tech_base(self, tb: ItemTechBase) -> None:
        if tb not in valid_item_tech_bases:
            raise ItemError(f"Tries to add invalid tech base '{tb}'")
        self._tech_base = tb

    @property
    def tags(self) -> list[ItemTag]:
        return self._tags

    def add_tag(self, tag: ItemTag) -> None:
        if tag not in valid_item_tags:
            raise ItemError(f"Tries to add invalid tag '{tag}'")
        if tag not in self._tags:  # keep the tags unique
            self._tags.append(tag)

    def __repr__(self) -> str:
        return f"[{self._key} | {self._name} |  {self._category} | {self._tech_base} | {self._tags}]"

    def validate(self) -> bool:
        return (
            len(self.category) == 2
            and self.category[0] in valid_item_classes
            and self.category[1] in valid_item_types
            and self.tech_base in valid_item_tech_bases
            and not any(tag not in valid_item_tags for tag in self.tags)
        )

    def __post_init__(self) -> None:
        if not self.validate():
            raise ItemError(f"Validation failed for item '{str(self)}'")


ranged_weapons: Final[list[item]] = [
    ### Ballistic weapons ###
    # Autocannons
    item(
        -1,
        "AC/2",
        ("weapon", "ballistic"),
        ["AC/2", "Autocannon/2"],
    ),
    item(
        -1,
        "AC/5",
        ("weapon", "ballistic"),
        ["AC/5", "Autocannon/5"],
    ),
    item(
        -1,
        "AC/10",
        ("weapon", "ballistic"),
        ["AC/10", "Autocannon/10"],
    ),
    item(
        -1,
        "AC/20",
        ("weapon", "ballistic"),
        ["AC/20", "Autocannon/20"],
    ),
    item(
        -1,
        "LB 2-X AC",
        ("weapon", "ballistic"),
        ["CLLBXAC2", "ISLBXAC2"],
    ),
    item(
        -1,
        "LB 5-X AC",
        ("weapon", "ballistic"),
        ["CLLBXAC5", "ISLBXAC5"],
    ),
    item(
        -1,
        "LB 10-X AC",
        ("weapon", "ballistic"),
        ["CLLBXAC10", "ISLBXAC10"],
    ),
    item(
        -1,
        "LB 20-X AC",
        ("weapon", "ballistic"),
        ["CLLBXAC20", "ISLBXAC20"],
    ),
    item(
        -1,
        "Light AC/2",
        ("weapon", "ballistic"),
        ["Light AC/2", "Light Auto Cannon/2"],
        "IS",
    ),
    item(
        -1,
        "Light AC/5",
        ("weapon", "ballistic"),
        ["Light AC/5", "Light Auto Cannon/5"],
        "IS",
    ),
    # Rotary Autocannons
    item(
        -1,
        "Rotary AC/2",
        ("weapon", "ballistic"),
        ["ISRotaryAC2", "CLRotaryAC2", "Rotary AC/2"],
    ),
    item(
        -1,
        "Rotary AC/5",
        ("weapon", "ballistic"),
        ["ISRotaryAC5", "CLRotaryAC5", "Rotary AC/5"],
    ),
    # Ultra Autocannons
    item(
        -1,
        "Ultra AC/2",
        ("weapon", "ballistic"),
        ["CLUltraAC2", "ISUltraAC2", "Ultra AC/2"],
    ),
    item(
        -1,
        "Ultra AC/5",
        ("weapon", "ballistic"),
        ["CLUltraAC5", "ISUltraAC5", "Ultra AC/5"],
    ),
    item(
        -1,
        "Ultra AC/10",
        ("weapon", "ballistic"),
        ["CLUltraAC10", "ISUltraAC10", "Ultra AC/10"],
    ),
    item(
        -1,
        "Ultra AC/20",
        ("weapon", "ballistic"),
        ["CLUltraAC20", "ISUltraAC20", "Ultra AC/20"],
    ),
    # ProtoMech Autocannons
    item(
        -1,
        "ProtoMech AC/2",
        ("weapon", "ballistic"),
        ["CLProtoMechAC2", "ProtoMech AC/2", "Clan ProtoMech AC/2"],
        "Clan",
    ),
    item(
        -1,
        "ProtoMech AC/4",
        ("weapon", "ballistic"),
        ["CLProtoMechAC4", "ProtoMech AC/4", "Clan ProtoMech AC/4"],
        "Clan",
    ),
    item(
        -1,
        "ProtoMech AC/8",
        ("weapon", "ballistic"),
        ["CLProtoMechAC8", "ProtoMech AC/8", "Clan ProtoMech AC/8"],
        "Clan",
    ),
    # Gauss Rifles
    item(
        -1,
        "Gauss Rifle",
        ("weapon", "ballistic"),
        ["ISGaussRifle", "CLGaussRifle", "Gauss Rifle"],
    ),
    item(
        -1,
        "Light Gauss Rifle",
        ("weapon", "ballistic"),
        ["ISLightGaussRifle", "Light Gauss Rifle"],
        "IS",
    ),
    item(
        -1,
        "Heavy Gauss Rifle",
        ("weapon", "ballistic"),
        ["ISHeavyGaussRifle"],
        "IS",
    ),
    item(
        -1,
        "Improved Heavy Gauss",
        ("weapon", "ballistic"),
        ["ISImprovedHeavyGaussRifle"],
        "IS",
    ),
    item(
        -1,
        "Magshot Gauss Rifle",
        ("weapon", "ballistic"),
        ["ISMagshotGR", "Magshot"],
        "IS",
    ),
    item(
        -1,
        "Silver Bullet Gauss",
        ("weapon", "ballistic"),
        ["Silver Bullet Gauss Rifle", "ISSBGR"],
        "IS",
    ),
    item(
        -1,
        "AP Gauss Rifle",
        ("weapon", "ballistic"),
        ["CLAPGaussRifle", "AP Gauss Rifle"],
        "Clan",
    ),
    item(
        -1,
        "HAG/20",  # Hyper Assault Gauss Rifle
        ("weapon", "ballistic"),
        ["CLHAG20", "HAG/20"],
        "Clan",
    ),
    item(
        -1,
        "HAG/30",
        ("weapon", "ballistic"),
        ["CLHAG30", "HAG/30"],
        "Clan",
    ),
    item(
        -1,
        "HAG/40",
        ("weapon", "ballistic"),
        ["CLHAG40", "HAG/40"],
        "Clan",
    ),
    # Machine Guns
    item(
        -1,
        "Light Machine Gun",
        ("weapon", "ballistic"),
        ["Light Machine Gun", "CLLightMG", "ISLightMG"],
    ),
    item(
        -1,
        "Machine Gun",
        ("weapon", "ballistic"),
        ["Machine Gun", "ISMachine Gun", "CLMG", "ISMG"],
    ),
    item(
        -1,
        "Heavy Machine Gun",
        ("weapon", "ballistic"),
        ["Heavy Machine Gun", "CLHeavyMG"],
    ),
    item(
        -1,
        "Machine Gun Array",
        ("weapon", "ballistic"),
        ["ISMGA", "CLMGA", "Machine Gun Array"],
    ),
    item(
        -1,
        "Heavy Machine Gun Array",
        ("weapon", "ballistic"),
        ["ISHMGA", "CLHMGA", "Heavy Machine Gun Array", "Clan Heavy Machine Gun Array"],
    ),
    item(
        -1,
        "Light Machine Gun Array",
        ("weapon", "ballistic"),
        ["ISLMGA", "CLLMGA", "Light Machine Gun Array"],
    ),
    # Rifles (Cannons)
    item(
        -1,
        "Light Rifle (Cannon)",
        ("weapon", "ballistic"),
        [],
        "IS",
    ),
    item(
        -1,
        "Medium Rifle (Cannon)",
        ("weapon", "ballistic"),
        [],
        "IS",
    ),
    item(
        -1,
        "Heavy Rifle (Cannon)",
        ("weapon", "ballistic"),
        ["Rifle (Cannon, Heavy)", "ISHeavyRifle", "Heavy Rifle", "Heavy Rifle (T)"],
        "IS",
    ),
    ### Energy weapons ###
    # Lasers
    item(
        -1,
        "Blazer Cannon",
        ("weapon", "energy"),
        [
            "Binary Laser (Blazer) Cannon",
        ],
        "IS",
    ),
    item(
        -1,
        "Small Laser",
        ("weapon", "energy"),
        ["ISSmallLaser", "Small Laser"],
    ),
    item(
        -1,
        "Medium Laser",
        ("weapon", "energy"),
        ["ISMediumLaser", "Medium Laser"],
    ),
    item(
        -1,
        "Large Laser",
        ("weapon", "energy"),
        ["ISLargeLaser", "Large Laser"],
    ),
    item(
        -1,
        "ER Micro Laser",
        ("weapon", "energy"),
        [],
        "Clan",
    ),
    item(
        -1,
        "ER Small Laser",
        ("weapon", "energy"),
        ["ISERSmallLaser", "CLERSmallLaser", "ER Small Laser"],
    ),
    item(
        -1,
        "ER Medium Laser",
        ("weapon", "energy"),
        ["ISERMediumLaser", "CLERMediumLaser", "ER Medium Laser"],
    ),
    item(
        -1,
        "ER Large Laser",
        ("weapon", "energy"),
        ["ISERLargeLaser", "CLERLargeLaser", "ER Large Laser"],
    ),
    item(
        -1,
        "Small Chem. Laser",
        ("weapon", "energy"),
        ["CLSmallChemLaser", "Small Chem Laser"],
        "Clan",
    ),
    item(
        -1,
        "Medium Chem. Laser",
        ("weapon", "energy"),
        ["CLMediumChemLaser", "Medium Chem Laser"],
        "Clan",
    ),
    item(
        -1,
        "Large Chem. Laser",
        ("weapon", "energy"),
        ["CLLargeChemLaser", "Large Chem Laser"],
        "Clan",
    ),
    item(
        -1,
        "Heavy Small Laser",
        ("weapon", "energy"),
        ["CLHeavySmallLaser", "Heavy Small Laser"],
        "Clan",
    ),
    item(
        -1,
        "Heavy Medium Laser",
        ("weapon", "energy"),
        ["CLHeavyMediumLaser", "Heavy Medium Laser"],
        "Clan",
    ),
    item(
        -1,
        "Heavy Large Laser",
        ("weapon", "energy"),
        ["CLHeavyLargeLaser", "Heavy Large Laser"],
        "Clan",
    ),
    item(
        -1,
        "Improved Heavy Small Laser",
        ("weapon", "energy"),
        ["CLImprovedSmallHeavyLaser", "Improved Heavy Small Laser"],
        "Clan",
    ),
    item(
        -1,
        "Improved Heavy Medium Laser",
        ("weapon", "energy"),
        ["CLImprovedMediumHeavyLaser", "Improved Heavy Medium Laser"],
        "Clan",
    ),
    item(
        -1,
        "Improved Heavy Large Laser",
        ("weapon", "energy"),
        ["CLImprovedHeavyLargeLaser", "Improved Heavy Large Laser"],
        "Clan",
    ),
    # Plasma Weapons
    item(
        -1,
        "Plasma Rifle",
        ("weapon", "energy"),
        ["ISPlasmaRifle", "Plasma Rifle"],
        "IS",
    ),
    item(
        -1,
        "Plasma Cannon",
        ("weapon", "energy"),
        ["CLPlasmaCannon", "Plasma Cannon"],
        "Clan",
    ),
    # PPCs
    item(
        -1,
        "Light PPC",
        ("weapon", "energy"),
        ["ISLightPPC", "Light PPC"],
        "IS",
    ),
    item(
        -1,
        "PPC",
        ("weapon", "energy"),
        ["ISPPC", "PPC"],
        "IS",
    ),
    item(
        -1,
        "Heavy PPC",
        ("weapon", "energy"),
        ["ISHeavyPPC", "Heavy PPC"],
        "IS",
    ),
    item(
        -1,
        "ER PPC",
        ("weapon", "energy"),
        ["ISERPPC", "CLERPPC", "ER PPC"],
    ),
    item(
        -1,
        "Snub-Nose PPC",
        ("weapon", "energy"),
        ["ISSNPPC", "Snub-Nose PPC"],
    ),
    # Flamers
    item(
        -1,
        "Flamer",
        ("weapon", "energy"),
        ["ISFlamer", "CLFlamer", "Flamer"],
    ),
    item(
        -1,
        "ER Flamer",
        ("weapon", "energy"),
        ["ISERFlamer", "CLERFlamer", "ER Flamer"],
    ),
    item(
        -1,
        "Heavy Flamer",
        ("weapon", "energy"),
        ["ISHeavyFlamer", "CLHeavyFlamer", "Heavy Flamer"],
    ),
    ### Pulse weapons ###
    item(
        -1,
        "Micro Pulse Laser",
        ("weapon", "pulse"),
        ["CLMicroPulseLaser", "Micro Pulse Laser"],
        "Clan",
    ),
    item(
        -1,
        "Small Pulse Laser",
        ("weapon", "pulse"),
        ["ISSmallPulseLaser", "CLSmallPulseLaser", "Small Pulse Laser"],
    ),
    item(
        -1,
        "Medium Pulse Laser",
        ("weapon", "pulse"),
        ["ISMediumPulseLaser", "CLMediumPulseLaser", "Medium Pulse Laser"],
    ),
    item(
        -1,
        "Large Pulse Laser",
        ("weapon", "pulse"),
        ["ISLargePulseLaser", "CLLargePulseLaser", "Large Pulse Laser"],
    ),
    item(
        -1,
        "Small X-Pulse Laser",
        ("weapon", "pulse"),
        ["ISSmallXPulseLaser", "Small X-Pulse Laser"],
        "IS",
    ),
    item(
        -1,
        "Medium X-Pulse Laser",
        ("weapon", "pulse"),
        ["ISMediumXPulseLaser", "Medium X-Pulse Laser"],
        "IS",
    ),
    item(
        -1,
        "Large X-Pulse Laser",
        ("weapon", "pulse"),
        ["ISLargeXPulseLaser", "Large X-Pulse Laser"],
        "IS",
    ),
    item(
        -1,
        "Small RE Laser",
        ("weapon", "pulse"),
        ["Small Re-engineered Laser"],
        "IS",
    ),
    item(
        -1,
        "Medium RE Laser",
        ("weapon", "pulse"),
        ["Medium Re-engineered Laser"],
        "IS",
    ),
    item(
        -1,
        "Large RE Laser",
        ("weapon", "pulse"),
        ["Large Re-engineered Laser"],
        "IS",
    ),
    item(
        -1,
        "Small VSP Laser",
        ("weapon", "pulse"),
        ["ISSmallVSPLaser", "ISSmallVariableSpeedLaser", "Small VSP Laser"],
        "IS",
    ),
    item(
        -1,
        "Medium VSP Laser",
        ("weapon", "pulse"),
        ["ISMediumVSPLaser", "ISMediumVariableSpeedLaser", "Medium VSP Laser"],
        "IS",
    ),
    item(
        -1,
        "Large VSP Laser",
        ("weapon", "pulse"),
        ["ISLargeVSPLaser", "ISLargeVariableSpeedLaser", "Large VSP Laser"],
        "IS",
    ),
    item(
        -1,
        "ER Small Pulse Laser",
        ("weapon", "pulse"),
        ["CLERSmallPulseLaser", "ER Small Pulse Laser"],
        "Clan",
    ),
    item(
        -1,
        "ER Medium Pulse Laser",
        ("weapon", "pulse"),
        ["CLERMediumPulseLaser", "ER Medium Pulse Laser"],
        "Clan",
    ),
    item(
        -1,
        "ER Large Pulse Laser",
        ("weapon", "pulse"),
        ["CLERLargePulseLaser", "ER Large Pulse Laser"],
        "Clan",
    ),
    ### Missile weapons ###
    item(
        -1,
        "LRM 5",
        ("weapon", "missile"),
        ["ISLRM5", "CLLRM5", "LRM 5"],
    ),
    item(
        -1,
        "LRM 10",
        ("weapon", "missile"),
        ["ISLRM10", "CLLRM10", "LRM 10"],
    ),
    item(
        -1,
        "LRM 15",
        ("weapon", "missile"),
        ["ISLRM15", "CLLRM15", "LRM 15"],
    ),
    item(
        -1,
        "LRM 20",
        ("weapon", "missile"),
        ["ISLRM20", "CLLRM20", "LRM 20"],
    ),
    item(
        -1,
        "Enhanced LRM 5",
        ("weapon", "missile"),
        ["ISEnhancedLRM5", "Enhanced LRM 5"],
        "IS",
    ),
    item(
        -1,
        "Enhanced LRM 10",
        ("weapon", "missile"),
        ["ISEnhancedLRM10", "Enhanced LRM 10"],
        "IS",
    ),
    item(
        -1,
        "Enhanced LRM 15",
        ("weapon", "missile"),
        ["ISEnhancedLRM15", "Enhanced LRM 15"],
        "IS",
    ),
    item(
        -1,
        "Enhanced LRM 20",
        ("weapon", "missile"),
        ["ISEnhancedLRM20", "Enhanced LRM 20"],
        "IS",
    ),
    item(
        -1,
        "Extended LRM 5",
        ("weapon", "missile"),
        ["Extended LRM 5"],
        "IS",
    ),
    item(
        -1,
        "Extended LRM 10",
        ("weapon", "missile"),
        ["Extended LRM 10"],
        "IS",
    ),
    item(
        -1,
        "Extended LRM 15",
        ("weapon", "missile"),
        ["Extended LRM 15"],
        "IS",
    ),
    item(
        -1,
        "Extended LRM 20",
        ("weapon", "missile"),
        ["Extended LRM 20"],
        "IS",
    ),
    item(
        -1,
        "MML 3",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "MML 5",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "MML 7",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "MML 9",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "MRM 10",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "MRM 20",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "MRM 30",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "MRM 40",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Narc Missile Beacon",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Improved Narc Launcher",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Rocket Launcher 10",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Rocket Launcher 15",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Rocket Launcher 20",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "SRM 2",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "SRM 4",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "SRM 6",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Streak SRM 2",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Streak SRM 4",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Streak SRM 6",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Thunderbolt 5",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Thunderbolt 10",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Thunderbolt 15",
        ("weapon", "missile"),
        [],
    ),
    item(
        -1,
        "Thunderbolt 20",
        ("weapon", "missile"),
        [],
    ),
    # Artillery
]

special_weapons: Final[list[item]] = [
    item(
        -1,
        "Active Probe, Beagle",
        ("weapon", "special"),
        ["BeagleActiveProbe", "ISBeagleActiveProbe"],
    ),
    item(
        -1,
        "Active Probe, Bloodhound",
        ("weapon", "special"),
        ["BloodhoundActiveProbe", "ISBloodhoundActiveProbe"],
    ),
    item(
        -1,
        "Active Probe, light",
        ("weapon", "special"),
        ["CLLightActiveProbe"],
    ),
    item(
        -1,
        "Anti-Missile System",
        ("weapon", "special"),
        ["ISAntiMissileSystem", "CLAntiMissileSystem", "Anti-Missile System"],
    ),
    item(
        -1,
        "Laser AMS",
        ("weapon", "special"),
        ["ISLaserAntiMissileSystem", "CLLaserAntiMissileSystem"],
    ),
    item(
        -1,
        "ECM Suite",
        ("weapon", "special"),
        ["CLECMSuite"],
    ),
    item(
        -1,
        "Angel ECM Suite",
        ("weapon", "special"),
        ["ISAngelECMSuite", "ISAngelECM", "CLAngelECMSuite"],
    ),
    item(
        -1,
        "Guardian ECM Suite",
        ("weapon", "special"),
        ["ISGuardianECM", "ISGuardianECMSuite"],
    ),
    item(
        -1,
        "M-Pod",
        ("weapon", "special"),
        ["M-Pod"],
    ),
    item(
        -1,
        "TAG",
        ("weapon", "special"),
        ["TAG", "ISTAG", "CLTAG", "Clan TAG"],
    ),  # there's also "C3 Master with TAG" and "C3 Master Boosted with TAG"
    item(
        -1,
        "Light TAG",
        ("weapon", "special"),
        ["Clan Light TAG", "CLLightTAG", "Light TAG", "Light TAG [Clan]"],
    ),
    item(
        -1,
        "Watchdog CEWS",
        ("weapon", "special"),
        ["WatchdogECMSuite"],
    ),
]

melee_weapons: Final[list[item]] = [
    item(
        -1,
        "Claws",
        ("weapon", "physical"),
        ["IS Claw", "ISClaw"],
    ),
    item(
        -1,
        "Flail",
        ("weapon", "physical"),
        ["IS Flail", "ISFlail"],
    ),
    item(
        -1,
        "Hatchet",
        ("weapon", "physical"),
        ["Hatchet"],
    ),
    item(
        -1,
        "Lance",
        ("weapon", "physical"),
        ["IS Lance", "ISLance", "Lance"],
    ),
    item(
        -1,
        "Mace",
        ("weapon", "physical"),
        ["Mace"],
    ),
    item(
        -1,
        "Vibroblade",
        ("weapon", "physical"),
        [
            "ISSmallVibroBlade",
            "ISMediumVibroblade",
            "ISLargeVibroblade",
            "Small Vibroblade",
            "Medium Vibroblade",
            "Large Vibroblade",
        ],
    ),
    item(
        -1,
        "Retractable Blade",
        ("weapon", "physical"),
        ["Retractable Blade"],
    ),
    item(
        -1,
        "Talons",
        ("weapon", "physical"),
        ["Talons"],
    ),
]

storage_equipment: Final[list[item]] = [
    item(
        -1,
        "Liquid Storage",
        ("equipment", "storage"),
        ["Liquid Storage"],
    ),
    item(
        -1,
        "Cargo",
        ("equipment", "storage"),
        ["Cargo"],
    ),
]

electronics_equipment: Final[list[item]] = [
    item(
        -1,
        "Communications Equipment",
        ("equipment", "electronics"),
        ["Communications Equipment"],
    ),
    item(
        -1,
        "Artemis IV FCS",
        ("equipment", "electronics"),
        ["ISArtemisIV", "CLArtemisIV"],
    ),
    item(
        -1,
        "Artemis V FCS",
        ("equipment", "electronics"),
        ["CLArtemisV"],
    ),
    item(
        -1,
        "C3 Computer (Master)",
        ("equipment", "electronics"),
        ["ISC3MasterUnit", "ISC3MasterComputer"],
    ),
    item(
        -1,
        "C3 Computer (Slave)",
        ("equipment", "electronics"),
        ["ISC3SlaveUnit"],
    ),
    item(
        -1,
        "C3i Computer",
        ("equipment", "electronics"),
        ["ISC3iUnit"],
    ),
    item(
        -1,
        "C3 Boosted System (Master)",
        ("equipment", "electronics"),
        ["ISC3MasterBoostedSystemUnit"],
    ),
    item(
        -1,
        "C3 Boosted System (Slave)",
        ("equipment", "electronics"),
        ["ISC3BoostedSystemSlaveUnit"],
    ),
    item(
        -1,
        "MRM Apollo FCS",
        ("equipment", "electronics"),
        ["ISApollo"],
    ),
    item(
        -1,
        "Targeting Computer",
        ("equipment", "electronics"),
        ["ISTargeting Computer", "CLTargeting Computer"],
    ),
]

miscellaneous_equipment: Final[list[item]] = [
    item(
        -1,
        "AES",
        ("equipment", "miscellaneous"),
        ["ISAES", "CLAES"],
    ),
    item(
        -1,
        "CASE",
        ("equipment", "miscellaneous"),
        ["ISCASE", "CLCASE"],
    ),
    item(
        -1,
        "CASE II",
        ("equipment", "miscellaneous"),
        ["CLCASEII"],
    ),
    item(
        -1,
        "Coolant Pod",
        ("equipment", "miscellaneous"),
        ["Coolant Pod", "IS Coolant Pod", "Clan Coolant Pod"],
    ),
    item(
        -1,
        "PPC Capacitor",
        ("equipment", "miscellaneous"),
        [
            "PPC Capacitor",
            "ISPPCCapacitor",
            "ISERPPCCapacitor",
            "ISHeavyPPCCapacitor",
            "ISLightPPCCapacitor",
        ],
    ),
]

maneuverability_equipment: Final[list[item]] = [
    item(
        -1,
        "MASC",
        ("equipment", "maneuverability"),
        ["ISMASC", "CLMASC"],
    ),
    item(
        -1,
        "Mechanical Jump Boosters",
        ("equipment", "maneuverability"),
        ["MechanicalJumpBooster"],
    ),
    item(
        -1,
        "Partial Wing",
        ("equipment", "maneuverability"),
        ["ISPartialWing", "CLPartialWing"],
    ),
    item(
        -1,
        "Supercharger",
        ("equipment", "maneuverability"),
        ["Supercharger"],
    ),
    item(
        -1,
        "TSM",
        ("equipment", "maneuverability"),
        ["TSM", "Industrial TSM"],
    ),
    item(
        -1,
        "UMU",
        ("equipment", "maneuverability"),
        ["UMU", "ISUMU", "CLUMU"],
    ),
    item(
        -1,
        "Jump Jet",
        ("equipment", "maneuverability"),
        ["Jump Jet", "ISPrototypeJumpJet"],
    ),
    item(
        -1,
        "Improved Jump Jet",
        ("equipment", "maneuverability"),
        [
            "Improved Jump Jet",
            "Clan Improved Jump Jet",
            "IS Improved Jump Jet",
            "ISImprovedJump Jet",
            "ISPrototypeImprovedJumpJet",
        ],
    ),
]


def get_item(mtf_name: str) -> item:
    """
    Return an item instance for the given MTF name. The returned item always contains the category.
    The tech_base will be determined from the given name, if possible. Otherwise it will be "unknown".
    Tags will be added if the given MTF name also contains some (e.g. 'armored', 'omnipod', etc.)
    """

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

    res_item: item | None = None
    clean_name = _clean_name(mtf_name)
    for i in chain(
        ranged_weapons,
        special_weapons,
        melee_weapons,
        storage_equipment,
        electronics_equipment,
        miscellaneous_equipment,
        maneuverability_equipment,
    ):
        if clean_name in i.mtf_names:
            # create a copy, because some values will be modified according
            # to the current item (e.g. tags and tech_base)
            res_item = deepcopy(i)
            break
    # raise exception if item is unknown
    if not res_item:
        raise ItemError(f"MTF name '{mtf_name}' not found in any item list.")
    # extract and add tags (if any)
    _add_tags(res_item, mtf_name)
    return res_item
