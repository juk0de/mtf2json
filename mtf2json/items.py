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

from dataclasses import dataclass
from itertools import chain
from typing import Literal


@dataclass
class item:
    """
    Identifies a piece of equipment or weapon by providing:
        - a numerical key (e.g. 12)
        - a category (e.g ("weapon", "ranged", "missile"))
        - a name (e.g. "Target Acquisition Gear")
        - a list with known MTF names (e.g. critical slot entries)
        - a tech base (e.g. "Clan")
    """

    key: int
    name: str
    category: tuple[str, ...]
    mtf_names: list[str]
    tech_base: Literal["unknown", "IS", "Clan"] = "unknown"


class ItemError(Exception):
    pass


ranged_weapons: list[item] = [
    # Ballistic weapons
    item(
        key=-1,
        name="AC/2",
        category=("weapon", "ranged", "ballistic"),
        mtf_names=["AC/2", "Autocannon/2"],
    ),
    item(
        -1,
        "AC/5",
        ("weapon", "ranged", "ballistic"),
        ["AC/5", "Autocannon/5"],
    ),
    item(
        -1,
        "AC/10",
        ("weapon", "ranged", "ballistic"),
        ["AC/10", "Autocannon/10"],
    ),
    item(
        -1,
        "AC/20",
        ("weapon", "ranged", "ballistic"),
        ["AC/20", "Autocannon/20"],
    ),
    item(
        -1,
        "LB 2-X AC",
        ("weapon", "ranged", "ballistic"),
        ["CLLBXAC2", "ISLBXAC2"],
    ),
    item(
        -1,
        "LB 5-X AC",
        ("weapon", "ranged", "ballistic"),
        ["CLLBXAC5", "ISLBXAC5"],
    ),
    item(
        -1,
        "LB 10-X AC",
        ("weapon", "ranged", "ballistic"),
        ["CLLBXAC10", "ISLBXAC10"],
    ),
    item(
        -1,
        "LB 20-X AC",
        ("weapon", "ranged", "ballistic"),
        ["CLLBXAC20", "ISLBXAC20"],
    ),
    item(
        -1,
        "Light AC/2",
        ("weapon", "ranged", "ballistic"),
        ["Light AC/2", "Light Auto Cannon/2"],
        tech_base="IS",
    ),
    item(
        -1,
        "Light AC/5",
        ("weapon", "ranged", "ballistic"),
        ["Light AC/5", "Light Auto Cannon/5"],
        tech_base="IS",
    ),
    item(
        -1,
        "Light Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        ["ISLightGaussRifle", "Light Gauss Rifle"],
        tech_base="IS",
    ),
    item(
        -1,
        "Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        ["ISGaussRifle", "CLGaussRifle", "Gauss Rifle"],
    ),
    item(
        -1,
        "Heavy Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        ["ISHeavyGaussRifle"],
        tech_base="IS",
    ),
    item(
        -1,
        "Improved Heavy Gauss",
        ("weapon", "ranged", "ballistic"),
        ["ISImprovedHeavyGaussRifle"],
        tech_base="IS",
    ),
    item(
        -1,
        "Magshot Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        ["ISMagshotGR", "Magshot"],
        tech_base="IS",
    ),
    item(
        -1,
        "Silver Bullet Gauss",
        ("weapon", "ranged", "ballistic"),
        ["Silver Bullet Gauss Rifle", "ISSBGR"],
        tech_base="IS",
    ),
    item(
        -1,
        "Light Machine Gun",
        ("weapon", "ranged", "ballistic"),
        ["Light Machine Gun", "CLLightMG", "ISLightMG"],
    ),
    item(
        -1,
        "Machine Gun",
        ("weapon", "ranged", "ballistic"),
        ["Machine Gun", "ISMachine Gun", "CLMG", "ISMG"],
    ),
    item(
        -1,
        "Heavy Machine Gun",
        ("weapon", "ranged", "ballistic"),
        ["Heavy Machine Gun", "CLHeavyMG"],
    ),
    item(
        -1,
        "Machine Gun Array",
        ("weapon", "ranged", "ballistic"),
        ["ISMGA", "CLMGA", "Machine Gun Array"],
    ),
    item(
        -1,
        "Heavy Machine Gun Array",
        ("weapon", "ranged", "ballistic"),
        ["ISHMGA", "CLHMGA", "Heavy Machine Gun Array", "Clan Heavy Machine Gun Array"],
    ),
    item(
        -1,
        "Light Machine Gun Array",
        ("weapon", "ranged", "ballistic"),
        ["ISLMGA", "CLLMGA", "Light Machine Gun Array"],
    ),
    item(
        -1,
        "Light Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        [],
        tech_base="IS",
    ),
    item(
        -1,
        "Medium Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        [],
        tech_base="IS",
    ),
    item(
        -1,
        "Heavy Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        ["Rifle (Cannon, Heavy)", "ISHeavyRifle", "Heavy Rifle", "Heavy Rifle (T)"],
        tech_base="IS",
    ),
    item(
        -1,
        "Rotary AC/2",
        ("weapon", "ranged", "ballistic"),
        ["ISRotaryAC2", "CLRotaryAC2", "Rotary AC/2"],
    ),
    item(
        -1,
        "Rotary AC/5",
        ("weapon", "ranged", "ballistic"),
        ["ISRotaryAC5", "CLRotaryAC5", "Rotary AC/5"],
    ),
    item(
        -1,
        "Ultra AC/2",
        ("weapon", "ranged", "ballistic"),
        ["CLUltraAC2", "ISUltraAC2", "Ultra AC/2"],
    ),
    item(
        -1,
        "Ultra AC/5",
        ("weapon", "ranged", "ballistic"),
        ["CLUltraAC5", "ISUltraAC5", "Ultra AC/5"],
    ),
    item(
        -1,
        "Ultra AC/10",
        ("weapon", "ranged", "ballistic"),
        ["CLUltraAC10", "ISUltraAC10", "Ultra AC/10"],
    ),
    # Energy weapons
    item(
        -1,
        "Blazer Cannon",
        ("weapon", "ranged", "energy"),
        [
            "Binary Laser (Blazer) Cannon",
        ],
        tech_base="IS",
    ),
    item(
        -1,
        "Flamer",
        ("weapon", "ranged", "energy"),
        ["ISFlamer", "CLFlamer", "Flamer"],
    ),
    item(
        -1,
        "ER Flamer",
        ("weapon", "ranged", "energy"),
        ["ISERFlamer", "CLERFlamer", "ER Flamer"],
    ),
    item(
        -1,
        "Heavy Flamer",
        ("weapon", "ranged", "energy"),
        ["ISHeavyFlamer", "CLHeavyFlamer", "Heavy Flamer"],
    ),
    item(
        -1,
        "Small Laser",
        ("weapon", "ranged", "energy"),
        ["ISSmallLaser", "Small Laser"],
    ),
    item(
        -1,
        "Medium Laser",
        ("weapon", "ranged", "energy"),
        ["ISMediumLaser", "Medium Laser"],
    ),
    item(
        -1,
        "Large Laser",
        ("weapon", "ranged", "energy"),
        ["ISLargeLaser", "Large Laser"],
    ),
    item(
        -1,
        "ER Small Laser",
        ("weapon", "ranged", "energy"),
        ["ISERSmallLaser", "CLERSmallLaser", "ER Small Laser"],
    ),
    item(
        -1,
        "ER Medium Laser",
        ("weapon", "ranged", "energy"),
        ["ISERMediumLaser", "CLERMediumLaser", "ER Medium Laser"],
    ),
    item(
        -1,
        "ER Large Laser",
        ("weapon", "ranged", "energy"),
        ["ISERLargeLaser", "CLERLargeLaser", "ER Large Laser"],
    ),
    item(
        -1,
        "Plasma Rifle",
        ("weapon", "ranged", "energy"),
        ["ISPlasmaRifle", "Plasma Rifle"],
        tech_base="IS",
    ),
    item(
        -1,
        "Light PPC",
        ("weapon", "ranged", "energy"),
        ["ISLightPPC", "Light PPC"],
        tech_base="IS",
    ),
    item(
        -1,
        "PPC",
        ("weapon", "ranged", "energy"),
        ["ISPPC", "PPC"],
        tech_base="IS",
    ),
    item(
        -1,
        "Heavy PPC",
        ("weapon", "ranged", "energy"),
        ["ISHeavyPPC", "Heavy PPC"],
        tech_base="IS",
    ),
    item(
        -1,
        "ER PPC",
        ("weapon", "ranged", "energy"),
        ["ISERPPC", "CLERPPC", "ER PPC"],
    ),
    item(
        -1,
        "Snub-Nose PPC",
        ("weapon", "ranged", "energy"),
        ["ISSNPPC", "Snub-Nose PPC"],
    ),
    # Pulse weapons
    item(
        -1,
        "Small Pulse Laser",
        ("weapon", "ranged", "pulse"),
        ["ISSmallPulseLaser", "CLSmallPulseLaser", "Small Pulse Laser"],
    ),
    item(
        -1,
        "Medium Pulse Laser",
        ("weapon", "ranged", "pulse"),
        ["ISMediumPulseLaser", "CLMediumPulseLaser", "Medium Pulse Laser"],
    ),
    item(
        -1,
        "Large Pulse Laser",
        ("weapon", "ranged", "pulse"),
        ["ISLargePulseLaser", "CLLargePulseLaser", "Large Pulse Laser"],
    ),
    item(
        -1,
        "Small X-Pulse Laser",
        ("weapon", "ranged", "pulse"),
        ["ISSmallXPulseLaser", "Small X-Pulse Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Medium X-Pulse Laser",
        ("weapon", "ranged", "pulse"),
        ["ISMediumXPulseLaser", "Medium X-Pulse Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Large X-Pulse Laser",
        ("weapon", "ranged", "pulse"),
        ["ISLargeXPulseLaser", "Large X-Pulse Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Small RE Laser",
        ("weapon", "ranged", "pulse"),
        ["Small Re-engineered Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Medium RE Laser",
        ("weapon", "ranged", "pulse"),
        ["Medium Re-engineered Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Large RE Laser",
        ("weapon", "ranged", "pulse"),
        ["Large Re-engineered Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Small VSP Laser",
        ("weapon", "ranged", "pulse"),
        ["ISSmallVSPLaser", "ISSmallVariableSpeedLaser", "Small VSP Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Medium VSP Laser",
        ("weapon", "ranged", "pulse"),
        ["ISMediumVSPLaser", "ISMediumVariableSpeedLaser", "Medium VSP Laser"],
        tech_base="IS",
    ),
    item(
        -1,
        "Large VSP Laser",
        ("weapon", "ranged", "pulse"),
        ["ISLargeVSPLaser", "ISLargeVariableSpeedLaser", "Large VSP Laser"],
        tech_base="IS",
    ),
    # Missile weapons
    item(
        -1,
        "LRM 5",
        ("weapon", "ranged", "missile"),
        ["ISLRM5", "CLLRM5", "LRM 5"],
    ),
    item(
        -1,
        "LRM 10",
        ("weapon", "ranged", "missile"),
        ["ISLRM10", "CLLRM10", "LRM 10"],
    ),
    item(
        -1,
        "LRM 15",
        ("weapon", "ranged", "missile"),
        ["ISLRM15", "CLLRM15", "LRM 15"],
    ),
    item(
        -1,
        "LRM 20",
        ("weapon", "ranged", "missile"),
        ["ISLRM20", "CLLRM20", "LRM 20"],
    ),
    item(
        -1,
        "Enhanced LRM 5",
        ("weapon", "ranged", "missile"),
        ["ISEnhancedLRM5", "Enhanced LRM 5"],
        tech_base="IS",
    ),
    item(
        -1,
        "Enhanced LRM 10",
        ("weapon", "ranged", "missile"),
        ["ISEnhancedLRM10", "Enhanced LRM 10"],
        tech_base="IS",
    ),
    item(
        -1,
        "Enhanced LRM 15",
        ("weapon", "ranged", "missile"),
        ["ISEnhancedLRM15", "Enhanced LRM 15"],
        tech_base="IS",
    ),
    item(
        -1,
        "Enhanced LRM 20",
        ("weapon", "ranged", "missile"),
        ["ISEnhancedLRM20", "Enhanced LRM 20"],
        tech_base="IS",
    ),
    item(
        -1,
        "Extended LRM 5",
        ("weapon", "ranged", "missile"),
        ["Extended LRM 5"],
        tech_base="IS",
    ),
    item(
        -1,
        "Extended LRM 10",
        ("weapon", "ranged", "missile"),
        ["Extended LRM 10"],
        tech_base="IS",
    ),
    item(
        -1,
        "Extended LRM 15",
        ("weapon", "ranged", "missile"),
        ["Extended LRM 15"],
        tech_base="IS",
    ),
    item(
        -1,
        "Extended LRM 20",
        ("weapon", "ranged", "missile"),
        ["Extended LRM 20"],
        tech_base="IS",
    ),
    item(
        -1,
        "MML 3",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "MML 5",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "MML 7",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "MML 9",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "MRM 10",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "MRM 20",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "MRM 30",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "MRM 40",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Narc Missile Beacon",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Improved Narc Launcher",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Rocket Launcher 10",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Rocket Launcher 15",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Rocket Launcher 20",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "SRM 2",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "SRM 4",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "SRM 6",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Streak SRM 2",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Streak SRM 4",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Streak SRM 6",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Thunderbolt 5",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Thunderbolt 10",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Thunderbolt 15",
        ("weapon", "ranged", "missile"),
        [],
    ),
    item(
        -1,
        "Thunderbolt 20",
        ("weapon", "ranged", "missile"),
        [],
    ),
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
        ("weapon", "melee"),
        ["IS Claw", "ISClaw"],
    ),
    item(
        -1,
        "Flail",
        ("weapon", "melee"),
        ["IS Flail", "ISFlail"],
    ),
    item(
        -1,
        "Hatchet",
        ("weapon", "melee"),
        ["Hatchet"],
    ),
    item(
        -1,
        "Lance",
        ("weapon", "melee"),
        ["IS Lance", "ISLance", "Lance"],
    ),
    item(
        -1,
        "Mace",
        ("weapon", "melee"),
        ["Mace"],
    ),
    item(
        -1,
        "Vibroblade",
        ("weapon", "melee"),
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
        ("weapon", "melee"),
        ["Retractable Blade"],
    ),
    item(
        -1,
        "Talons",
        ("weapon", "melee"),
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


def get_item(mtf_name: str) -> item:
    """
    Return an item instance for the given MTF name.
    """
    for item in chain(
        ranged_weapons,
        special_weapons,
        melee_weapons,
        storage_equipment,
        electronics_equipment,
        miscellaneous_equipment,
        maneuverability_equipment,
    ):
        if mtf_name in item.mtf_names:
            return item
    raise ItemError(f"MTF name '{mtf_name}' not found in any item list.")
