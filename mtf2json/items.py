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
This module is all about naming individual items. The goal is to have
consistent names for weapons and equipment in all JSON mech files.
Unfortunately, this is currently not the case in the MTF files, e.g.
ECM Suites are sometimes called "ECMSuite" and sometimes just "ECM"
and so on. Therefore we're mapping the various names from the MTF
files to new unified names.
"""

from dataclasses import dataclass
from itertools import chain
from typing import Literal


@dataclass
class item:
    """
    Identifies a piece of equipment or weapon by providing:
        - a numerical key (e.g. 12)
        - a category      (e.g ("weapon", "ranged", "missile"))
        - a full name     (e.g. "Target Acquisition Gear")
        - a short name    (e.g. "TAG")
        - a list with known MTF names (e.g. critical slot entries)
    """

    key: int
    full_name: str
    short_name: str
    category: tuple[str, ...]
    mtf_names: list[str]
    tech_base: Literal["unknown", "IS", "Clan"] = "unknown"


class ItemError(Exception):
    pass


ranged_weapons: list[item] = [
    # Ballistic weapons
    item(
        -1,
        "Machine Gun Array",
        "MGA",
        ("weapon", "ranged", "ballistic"),
        ["ISMGA", "CLMGA"],
    ),
    item(
        -1,
        "Heavy Machine Gun Array",
        "Heavy MGA",
        ("weapon", "ranged", "ballistic"),
        ["ISHMGA", "CLHMGA"],
    ),
    item(
        -1,
        "Light Machine Gun Array",
        "Light MGA",
        ("weapon", "ranged", "ballistic"),
        ["ISLMGA", "CLLMGA"],
    ),
    item(
        -1,
        "Autocannon/2",
        "AC/2",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Autocannon/5",
        "AC/5",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Autocannon/10",
        "AC/10",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Autocannon/20",
        "AC/20",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Light Gauss Rifle",
        "Light Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Gauss Rifle",
        "Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Heavy Gauss Rifle",
        "Heavy Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Improved Heavy Gauss",
        "Improved Heavy Gauss",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Magshot Gauss Rifle",
        "Magshot Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Silver Bullet Gauss",
        "Silver Bullet Gauss",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "LB 2-X AC",
        "LB 2-X AC",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "LB 5-X AC",
        "LB 5-X AC",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "LB 10-X AC",
        "LB 10-X AC",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "LB 20-X AC",
        "LB 20-X AC",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Light AC/2",
        "Light AC/2",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Light AC/5",
        "Light AC/5",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Light Machine Gun",
        "Light Machine Gun",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Machine Gun",
        "Machine Gun",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Heavy Machine Gun",
        "Heavy Machine Gun",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Light Rifle (Cannon)",
        "Light Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Medium Rifle (Cannon)",
        "Medium Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Heavy Rifle (Cannon)",
        "Heavy Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Rotary AC/2",
        "Rotary AC/2",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Rotary AC/5",
        "Rotary AC/5",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Ultra AC/2",
        "Ultra AC/2",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Ultra AC/5",
        "Ultra AC/5",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Ultra AC/10",
        "Ultra AC/10",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Ultra AC/2",
        "Ultra AC/2",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    # Energy weapons
    item(
        -1,
        "Binary (Blazer) Cannon",
        "Binary (Blazer) Cannon",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Flamer",
        "Flamer",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER Flamer",
        "ER Flamer",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Heavy Flamer",
        "Heavy Flamer",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Small Laser",
        "Small Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Medium Laser",
        "Medium Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Large Laser",
        "Large Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER Small Laser",
        "ER Small Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER Medium Laser",
        "ER Medium Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER Large Laser",
        "ER Large Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Plasma Rifle",
        "Plasma Rifle",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Light PPC",
        "Light PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "PPC",
        "PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Heavy PPC",
        "Heavy PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER PPC",
        "ER PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Snub-Nose PPC",
        "Snub-Nose PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    # Pulse weapons
    item(
        -1,
        "Small Pulse Laser",
        "Small Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Medium Pulse Laser",
        "Medium Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Large Pulse Laser",
        "Large Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Small X-Pulse Laser",
        "Small X-Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Medium X-Pulse Laser",
        "Medium X-Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Large X-Pulse Laser",
        "Large X-Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Small Re-engineered Laser",
        "Small Re-engineered Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Medium Re-engineered Laser",
        "Medium Re-engineered Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Large Re-engineered Laser",
        "Large Re-engineered Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Small VSP Laser",
        "Small VSP Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Medium VSP Laser",
        "Medium VSP Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Large VSP Laser",
        "Large VSP Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
]

special_weapons: list[item] = [
    item(
        -1,
        "Active Probe, Beagle",
        "Beagle Active Probe",
        ("weapon", "special"),
        ["BeagleActiveProbe", "ISBeagleActiveProbe"],
    ),
    item(
        -1,
        "Active Probe, Bloodhound",
        "Bloodhound Active Probe",
        ("weapon", "special"),
        ["BloodhoundActiveProbe", "ISBloodhoundActiveProbe"],
    ),
    item(
        -1,
        "Active Probe, light",
        "Light Active Probe",
        ("weapon", "special"),
        ["CLLightActiveProbe"],
    ),
    item(
        -1,
        "Anti-Missile System",
        "AMS",
        ("weapon", "special"),
        ["ISAntiMissileSystem", "CLAntiMissileSystem", "Anti-Missile System"],
    ),
    item(
        -1,
        "Anti-Missile System, Laser",
        "Laser AMS",
        ("weapon", "special"),
        ["ISLaserAntiMissileSystem", "CLLaserAntiMissileSystem"],
    ),
    item(
        -1,
        "ECM Suite",
        "ECM Suite",
        ("weapon", "special"),
        ["CLECMSuite"],
    ),
    item(
        -1,
        "ECM Suite, Angel",
        "Angel ECM",
        ("weapon", "special"),
        ["ISAngelECMSuite", "ISAngelECM", "CLAngelECMSuite"],
    ),
    item(
        -1,
        "ECM Suite, Guardian",
        "Guardian ECM",
        ("weapon", "special"),
        ["ISGuardianECM", "ISGuardianECMSuite"],
    ),
    item(
        -1,
        "M-Pod",
        "M-Pod",
        ("weapon", "special"),
        ["M-Pod"],
    ),
    item(
        -1,
        "Target Acquisition Gear",
        "TAG",
        ("weapon", "special"),
        ["TAG", "ISTAG", "CLTAG", "Clan TAG"],
    ),  # there's also "C3 Master with TAG" and "C3 Master Boosted with TAG"
    item(
        -1,
        "Target Acquisition Gear, Light",
        "Light TAG",
        ("weapon", "special"),
        ["Clan Light TAG", "CLLightTAG", "Light TAG"],
    ),
    item(
        -1,
        "Watchdog Composite Electronic Warfare System",
        "Watchdog CEWS",
        ("weapon", "special"),
        ["WatchdogECMSuite"],
    ),
]

melee_weapons: list[item] = [
    item(
        -1,
        "Claws",
        "Claws",
        ("weapon", "melee"),
        ["IS Claw", "ISClaw"],
    ),
    item(
        -1,
        "Flail",
        "Flail",
        ("weapon", "melee"),
        ["IS Flail", "ISFlail"],
    ),
    item(
        -1,
        "Hatchet",
        "Hatchet",
        ("weapon", "melee"),
        ["Hatchet"],
    ),
    item(
        -1,
        "Lance",
        "Lance",
        ("weapon", "melee"),
        ["IS Lance", "ISLance", "Lance"],
    ),
    item(
        -1,
        "Mace",
        "Mace",
        ("weapon", "melee"),
        ["Mace"],
    ),
    item(
        -1,
        "Vibroblade",
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
        "Retractable Blade",
        ("weapon", "melee"),
        ["Retractable Blade"],
    ),
    item(
        -1,
        "Talons",
        "Talons",
        ("weapon", "melee"),
        ["Talons"],
    ),
]

storage_equipment: list[item] = [
    item(
        -1,
        "Liquid Storage",
        "Liquid Storage",
        ("equipment", "storage"),
        ["Liquid Storage"],
    ),
    item(
        -1,
        "Cargo",
        "Cargo",
        ("equipment", "storage"),
        ["Cargo"],
    ),
]

electronics_equipment: list[item] = [
    item(
        -1,
        "Communications Equipment",
        "Comms Gear",
        ("equipment", "electronics"),
        ["Communications Equipment"],
    ),
    item(
        -1,
        "Artemis IV Fire-Control System",
        "Artemis IV FCS",
        ("equipment", "electronics"),
        ["ISArtemisIV", "CLArtemisIV"],
    ),
    item(
        -1,
        "Artemis V Fire-Control System",
        "Artemis V FCS",
        ("equipment", "electronics"),
        ["CLArtemisV"],
    ),
    item(
        -1,
        "C3 Computer, Master",
        "C3 Computer (Master)",
        ("equipment", "electronics"),
        ["ISC3MasterUnit", "ISC3MasterComputer"],
    ),
    item(
        -1,
        "C3 Computer, Slave",
        "C3 Computer (Slave)",
        ("equipment", "electronics"),
        ["ISC3SlaveUnit"],
    ),
    item(
        -1,
        "C3i Computer",
        "C3i Computer",
        ("equipment", "electronics"),
        ["ISC3iUnit"],
    ),
    item(
        -1,
        "C3 Boosted System, Master",
        "C3 Boosted System (Master)",
        ("equipment", "electronics"),
        ["ISC3MasterBoostedSystemUnit"],
    ),
    item(
        -1,
        "C3 Boosted System, Slave",
        "C3 Boosted System (Slave)",
        ("equipment", "electronics"),
        ["ISC3BoostedSystemSlaveUnit"],
    ),
    item(
        -1,
        "MRM Apollo Fire-Control System",
        "MRM Apollo FCS",
        ("equipment", "electronics"),
        ["ISApollo"],
    ),
    item(
        -1,
        "Targeting Computer",
        "Targeting Computer",
        ("equipment", "electronics"),
        ["ISTargeting Computer", "CLTargeting Computer"],
    ),
]

miscellaneous_equipment: list[item] = [
    item(
        -1,
        "Actuator Enhancement System",
        "AES",
        ("equipment", "miscellaneous"),
        ["ISAES", "CLAES"],
    ),
    item(
        -1,
        "Cellular Ammunition Storage Equipment",
        "CASE",
        ("equipment", "miscellaneous"),
        ["ISCASE", "CLCASE"],
    ),
    item(
        -1,
        "Cellular Ammunition Storage Equipment II",
        "CASE II",
        ("equipment", "miscellaneous"),
        ["CLCASEII"],
    ),
    item(
        -1,
        "Coolant Pod",
        "Coolant Pod",
        ("equipment", "miscellaneous"),
        ["Coolant Pod", "IS Coolant Pod", "Clan Coolant Pod"],
    ),
    item(
        -1,
        "PPC Capacitor",
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
        "Myomer Acceleration Signal Circuitry",
        "MASC",
        ("equipment", "maneuverability"),
        ["ISMASC", "CLMASC"],
    ),
    item(
        -1,
        "Mechanical Jump Boosters",
        "Mechanical Jump Boosters",
        ("equipment", "maneuverability"),
        ["MechanicalJumpBooster"],
    ),
    item(
        -1,
        "Partial Wing",
        "Partial Wing",
        ("equipment", "maneuverability"),
        ["ISPartialWing", "CLPartialWing"],
    ),
    item(
        -1,
        "Supercharger",
        "Supercharger",
        ("equipment", "maneuverability"),
        ["Supercharger"],
    ),
    item(
        -1,
        "Triple-Strength Myomer",
        "TSM",
        ("equipment", "maneuverability"),
        ["TSM", "Industrial TSM"],
    ),
    item(
        -1,
        "Underwater Maneuvering Unit",
        "UMU",
        ("equipment", "maneuverability"),
        ["UMU", "ISUMU", "CLUMU"],
    ),
    item(
        -1,
        "Jump Jets, Standard",
        "Standard Jump Jets",
        ("equipment", "maneuverability"),
        ["Jump Jet", "ISPrototypeJumpJet"],
    ),
    item(
        -1,
        "Jump Jets, Improved",
        "Improved Jump Jets",
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
