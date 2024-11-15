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
from dataclasses import dataclass
from itertools import chain
from typing import Literal

# the available item classes
item_classes = ["weapon", "equipment"]
# the available item types
item_types = [
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
    """

    key: int
    name: str
    category: tuple[str, str]
    mtf_names: list[str]
    tech_base: Literal["unknown", "IS", "Clan"] = "unknown"

    def __post_init__(self):
        # the first entry must be the item class
        assert self.category[0] in item_classes
        # the second entry must be the item type
        assert self.category[1] in item_types


class ItemError(Exception):
    pass


ranged_weapons: list[item] = [
    ### Ballistic weapons ###
    # Autocannons
    item(
        key=-1,
        name="AC/2",
        category=("weapon", "ballistic"),
        mtf_names=["AC/2", "Autocannon/2"],
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
        tech_base="IS",
    ),
    item(
        -1,
        "Light AC/5",
        ("weapon", "ballistic"),
        ["Light AC/5", "Light Auto Cannon/5"],
        tech_base="IS",
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
        tech_base="Clan",
    ),
    item(
        -1,
        "ProtoMech AC/4",
        ("weapon", "ballistic"),
        ["CLProtoMechAC4", "ProtoMech AC/4", "Clan ProtoMech AC/4"],
        tech_base="Clan",
    ),
    item(
        -1,
        "ProtoMech AC/8",
        ("weapon", "ballistic"),
        ["CLProtoMechAC8", "ProtoMech AC/8", "Clan ProtoMech AC/8"],
        tech_base="Clan",
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
        tech_base="IS",
    ),
    item(
        -1,
        "Heavy Gauss Rifle",
        ("weapon", "ballistic"),
        ["ISHeavyGaussRifle"],
        tech_base="IS",
    ),
    item(
        -1,
        "Improved Heavy Gauss",
        ("weapon", "ballistic"),
        ["ISImprovedHeavyGaussRifle"],
        tech_base="IS",
    ),
    item(
        -1,
        "Magshot Gauss Rifle",
        ("weapon", "ballistic"),
        ["ISMagshotGR", "Magshot"],
        tech_base="IS",
    ),
    item(
        -1,
        "Silver Bullet Gauss",
        ("weapon", "ballistic"),
        ["Silver Bullet Gauss Rifle", "ISSBGR"],
        tech_base="IS",
    ),
    item(
        -1,
        "AP Gauss Rifle",
        ("weapon", "ballistic"),
        ["CLAPGaussRifle", "AP Gauss Rifle"],
        tech_base="Clan",
    ),
    item(
        -1,
        "HAG/20",  # Hyper Assault Gauss Rifle
        ("weapon", "ballistic"),
        ["CLHAG20", "HAG/20"],
        tech_base="Clan",
    ),
    item(
        -1,
        "HAG/30",
        ("weapon", "ballistic"),
        ["CLHAG30", "HAG/30"],
        tech_base="Clan",
    ),
    item(
        -1,
        "HAG/40",
        ("weapon", "ballistic"),
        ["CLHAG40", "HAG/40"],
        tech_base="Clan",
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
        tech_base="IS",
    ),
    item(
        -1,
        "Medium Rifle (Cannon)",
        ("weapon", "ballistic"),
        [],
        tech_base="IS",
    ),
    item(
        -1,
        "Heavy Rifle (Cannon)",
        ("weapon", "ballistic"),
        ["Rifle (Cannon, Heavy)", "ISHeavyRifle", "Heavy Rifle", "Heavy Rifle (T)"],
        tech_base="IS",
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
        tech_base="IS",
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
        tech_base="Clan",
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
        tech_base="Clan",
    ),
    item(
        -1,
        "Medium Chem. Laser",
        ("weapon", "energy"),
        ["CLMediumChemLaser", "Medium Chem Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "Large Chem. Laser",
        ("weapon", "energy"),
        ["CLLargeChemLaser", "Large Chem Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "Heavy Small Laser",
        ("weapon", "energy"),
        ["CLHeavySmallLaser", "Heavy Small Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "Heavy Medium Laser",
        ("weapon", "energy"),
        ["CLHeavyMediumLaser", "Heavy Medium Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "Heavy Large Laser",
        ("weapon", "energy"),
        ["CLHeavyLargeLaser", "Heavy Large Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "Improved Heavy Small Laser",
        ("weapon", "energy"),
        ["CLImprovedSmallHeavyLaser", "Improved Heavy Small Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "Improved Heavy Medium Laser",
        ("weapon", "energy"),
        ["CLImprovedMediumHeavyLaser", "Improved Heavy Medium Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "Improved Heavy Large Laser",
        ("weapon", "energy"),
        ["CLImprovedHeavyLargeLaser", "Improved Heavy Large Laser"],
        tech_base="Clan",
    ),
    # Plasma Weapons
    item(
        -1,
        "Plasma Rifle",
        ("weapon", "energy"),
        ["ISPlasmaRifle", "Plasma Rifle"],
        tech_base="IS",
    ),
    item(
        -1,
        "Plasma Cannon",
        ("weapon", "energy"),
        ["CLPlasmaCannon", "Plasma Cannon"],
        tech_base="Clan",
    ),
    # PPCs
    item(
        -1,
        "Light PPC",
        ("weapon", "energy"),
        ["ISLightPPC", "Light PPC"],
        tech_base="IS",
    ),
    item(
        -1,
        "PPC",
        ("weapon", "energy"),
        ["ISPPC", "PPC"],
        tech_base="IS",
    ),
    item(
        -1,
        "Heavy PPC",
        ("weapon", "energy"),
        ["ISHeavyPPC", "Heavy PPC"],
        tech_base="IS",
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
        tech_base="Clan",
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
        tech_base="IS",
    ),
    item(
        -1,
        "Medium X-Pulse Laser",
        ("weapon", "pulse"),
        ["ISMediumXPulseLaser", "Medium X-Pulse Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Large X-Pulse Laser",
        ("weapon", "pulse"),
        ["ISLargeXPulseLaser", "Large X-Pulse Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Small RE Laser",
        ("weapon", "pulse"),
        ["Small Re-engineered Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Medium RE Laser",
        ("weapon", "pulse"),
        ["Medium Re-engineered Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Large RE Laser",
        ("weapon", "pulse"),
        ["Large Re-engineered Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Small VSP Laser",
        ("weapon", "pulse"),
        ["ISSmallVSPLaser", "ISSmallVariableSpeedLaser", "Small VSP Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Medium VSP Laser",
        ("weapon", "pulse"),
        ["ISMediumVSPLaser", "ISMediumVariableSpeedLaser", "Medium VSP Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Large VSP Laser",
        ("weapon", "pulse"),
        ["ISLargeVSPLaser", "ISLargeVariableSpeedLaser", "Large VSP Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "ER Small Pulse Laser",
        ("weapon", "pulse"),
        ["CLERSmallPulseLaser", "ER Small Pulse Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "ER Medium Pulse Laser",
        ("weapon", "pulse"),
        ["CLERMediumPulseLaser", "ER Medium Pulse Laser"],
        tech_base="Clan",
    ),
    item(
        -1,
        "ER Large Pulse Laser",
        ("weapon", "pulse"),
        ["CLERLargePulseLaser", "ER Large Pulse Laser"],
        tech_base="Clan",
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
        tech_base="IS",
    ),
    item(
        -1,
        "Enhanced LRM 10",
        ("weapon", "missile"),
        ["ISEnhancedLRM10", "Enhanced LRM 10"],
        tech_base="IS",
    ),
    item(
        -1,
        "Enhanced LRM 15",
        ("weapon", "missile"),
        ["ISEnhancedLRM15", "Enhanced LRM 15"],
        tech_base="IS",
    ),
    item(
        -1,
        "Enhanced LRM 20",
        ("weapon", "missile"),
        ["ISEnhancedLRM20", "Enhanced LRM 20"],
        tech_base="IS",
    ),
    item(
        -1,
        "Extended LRM 5",
        ("weapon", "missile"),
        ["Extended LRM 5"],
        tech_base="IS",
    ),
    item(
        -1,
        "Extended LRM 10",
        ("weapon", "missile"),
        ["Extended LRM 10"],
        tech_base="IS",
    ),
    item(
        -1,
        "Extended LRM 15",
        ("weapon", "missile"),
        ["Extended LRM 15"],
        tech_base="IS",
    ),
    item(
        -1,
        "Extended LRM 20",
        ("weapon", "missile"),
        ["Extended LRM 20"],
        tech_base="IS",
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

special_weapons: list[item] = [
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

melee_weapons: list[item] = [
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

storage_equipment: list[item] = [
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

electronics_equipment: list[item] = [
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

miscellaneous_equipment: list[item] = [
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

maneuverability_equipment: list[item] = [
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


def get_clean_name(mtf_name: str) -> str:
    """
    Strips the name of all irrelevant components,
    including anything within parentheses.
    """
    name = re.sub(r"\(.*?\)", "", mtf_name).strip()
    return name


def get_item(mtf_name: str) -> item:
    """
    Return an item instance for the given MTF name.
    The returned item always contains the category.
    The tech_base will be determined from the given name,
    if possible. Otherwise it will be "unknown".
    """
    # TODO: extract tags
    clean_name = get_clean_name(mtf_name)
    for item in chain(
        ranged_weapons,
        special_weapons,
        melee_weapons,
        storage_equipment,
        electronics_equipment,
        miscellaneous_equipment,
        maneuverability_equipment,
    ):
        if clean_name in item.mtf_names:
            return item
    raise ItemError(f"MTF name '{mtf_name}' not found in any item list.")
