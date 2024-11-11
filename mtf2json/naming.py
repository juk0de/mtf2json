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
This module is all about naming. The goal is to have consistent names
for weapons and equipment in all JSON mech files. Unfortunately, this
is currently not the case in the MTF files, e.g. ECM Suites are sometimes
called "ECMSuite" and sometimes just "ECM" and so on. Therefore we're
mapping the various names from the MTF files to new default names.
"""

from dataclasses import dataclass
from itertools import chain


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
    category: tuple[str, ...]
    full_name: str
    short_name: str
    mtf_names: list[str]


class ItemError(Exception):
    pass


ranged_weapons: list[item] = [
    # Ballistic weapons
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Machine Gun Array",
        "MGA",
        ["ISMGA", "CLMGA"],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Heavy Machine Gun Array",
        "Heavy MGA",
        ["ISHMGA", "CLHMGA"],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Light Machine Gun Array",
        "Light MGA",
        ["ISLMGA", "CLLMGA"],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Autocannon/2",
        "AC/2",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Autocannon/5",
        "AC/5",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Autocannon/10",
        "AC/10",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Autocannon/20",
        "AC/20",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Light Gauss Rifle",
        "Light Gauss Rifle",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Gauss Rifle",
        "Gauss Rifle",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Heavy Gauss Rifle",
        "Heavy Gauss Rifle",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Improved Heavy Gauss",
        "Improved Heavy Gauss",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Magshot Gauss Rifle",
        "Magshot Gauss Rifle",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Silver Bullet Gauss",
        "Silver Bullet Gauss",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "LB 2-X AC",
        "LB 2-X AC",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "LB 5-X AC",
        "LB 5-X AC",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "LB 10-X AC",
        "LB 10-X AC",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "LB 20-X AC",
        "LB 20-X AC",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Light AC/2",
        "Light AC/2",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Light AC/5",
        "Light AC/5",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Light Machine Gun",
        "Light Machine Gun",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Machine Gun",
        "Machine Gun",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Heavy Machine Gun",
        "Heavy Machine Gun",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Light Rifle (Cannon)",
        "Light Rifle (Cannon)",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Medium Rifle (Cannon)",
        "Medium Rifle (Cannon)",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Heavy Rifle (Cannon)",
        "Heavy Rifle (Cannon)",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Rotary AC/2",
        "Rotary AC/2",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Rotary AC/5",
        "Rotary AC/5",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Ultra AC/2",
        "Ultra AC/2",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Ultra AC/5",
        "Ultra AC/5",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Ultra AC/10",
        "Ultra AC/10",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "ballistic"),
        "Ultra AC/2",
        "Ultra AC/2",
        [],
    ),
    # Energy weapons
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Binary (Blazer) Cannon",
        "Binary (Blazer) Cannon",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Flamer",
        "Flamer",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "ER Flamer",
        "ER Flamer",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Heavy Flamer",
        "Heavy Flamer",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Small Laser",
        "Small Laser",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Medium Laser",
        "Medium Laser",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Large Laser",
        "Large Laser",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "ER Small Laser",
        "ER Small Laser",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "ER Medium Laser",
        "ER Medium Laser",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "ER Large Laser",
        "ER Large Laser",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Plasma Rifle",
        "Plasma Rifle",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Light PPC",
        "Light PPC",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "PPC",
        "PPC",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Heavy PPC",
        "Heavy PPC",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "ER PPC",
        "ER PPC",
        [],
    ),
    item(
        -1,
        ("weapon", "ranged", "energy"),
        "Snub-Nose PPC",
        "Snub-Nose PPC",
        [],
    ),
]

special_weapons: list[item] = [
    item(
        -1,
        ("weapon", "special"),
        "Active Probe, Beagle",
        "Beagle Active Probe",
        ["BeagleActiveProbe", "ISBeagleActiveProbe"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "Active Probe, Bloodhound",
        "Bloodhound Active Probe",
        ["BloodhoundActiveProbe", "ISBloodhoundActiveProbe"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "Active Probe, light",
        "Light Active Probe",
        ["CLLightActiveProbe"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "Anti-Missile System",
        "AMS",
        ["ISAntiMissileSystem", "CLAntiMissileSystem", "Anti-Missile System"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "Anti-Missile System, Laser",
        "Laser AMS",
        ["ISLaserAntiMissileSystem", "CLLaserAntiMissileSystem"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "ECM Suite",
        "ECM Suite",
        ["CLECMSuite"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "ECM Suite, Angel",
        "Angel ECM",
        ["ISAngelECMSuite", "ISAngelECM", "CLAngelECMSuite"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "ECM Suite, Guardian",
        "Guardian ECM",
        ["ISGuardianECM", "ISGuardianECMSuite"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "M-Pod",
        "M-Pod",
        ["M-Pod"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "Target Acquisition Gear",
        "TAG",
        ["TAG", "ISTAG", "CLTAG", "Clan TAG"],
    ),  # there's also "C3 Master with TAG" and "C3 Master Boosted with TAG"
    item(
        -1,
        ("weapon", "special"),
        "Target Acquisition Gear, Light",
        "Light TAG",
        ["Clan Light TAG", "CLLightTAG", "Light TAG"],
    ),
    item(
        -1,
        ("weapon", "special"),
        "Watchdog Composite Electronic Warfare System",
        "Watchdog CEWS",
        ["WatchdogECMSuite"],
    ),
]

melee_weapons: list[item] = [
    item(
        -1,
        ("weapon", "melee"),
        "Claws",
        "Claws",
        ["IS Claw", "ISClaw"],
    ),
    item(
        -1,
        ("weapon", "melee"),
        "Flail",
        "Flail",
        ["IS Flail", "ISFlail"],
    ),
    item(
        -1,
        ("weapon", "melee"),
        "Hatchet",
        "Hatchet",
        ["Hatchet"],
    ),
    item(
        -1,
        ("weapon", "melee"),
        "Lance",
        "Lance",
        ["IS Lance", "ISLance", "Lance"],
    ),
    item(
        -1,
        ("weapon", "melee"),
        "Mace",
        "Mace",
        ["Mace"],
    ),
    item(
        -1,
        ("weapon", "melee"),
        "Vibroblade",
        "Vibroblade",
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
        ("weapon", "melee"),
        "Retractable Blade",
        "Retractable Blade",
        ["Retractable Blade"],
    ),
    item(
        -1,
        ("weapon", "melee"),
        "Talons",
        "Talons",
        ["Talons"],
    ),
]

storage_equipment: list[item] = [
    item(
        -1,
        ("equipment", "storage"),
        "Liquid Storage",
        "Liquid Storage",
        ["Liquid Storage"],
    ),
    item(
        -1,
        ("equipment", "storage"),
        "Cargo",
        "Cargo",
        ["Cargo"],
    ),
]

electronics_equipment: list[item] = [
    item(
        -1,
        ("equipment", "electronics"),
        "Communications Equipment",
        "Comms Gear",
        ["Communications Equipment"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "Artemis IV Fire-Control System",
        "Artemis IV FCS",
        ["ISArtemisIV", "CLArtemisIV"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "Artemis V Fire-Control System",
        "Artemis V FCS",
        ["CLArtemisV"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "C3 Computer, Master",
        "C3 Computer (Master)",
        ["ISC3MasterUnit", "ISC3MasterComputer"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "C3 Computer, Slave",
        "C3 Computer (Slave)",
        ["ISC3SlaveUnit"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "C3i Computer",
        "C3i Computer",
        ["ISC3iUnit"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "C3 Boosted System, Master",
        "C3 Boosted System (Master)",
        ["ISC3MasterBoostedSystemUnit"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "C3 Boosted System, Slave",
        "C3 Boosted System (Slave)",
        ["ISC3BoostedSystemSlaveUnit"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "MRM Apollo Fire-Control System",
        "MRM Apollo FCS",
        ["ISApollo"],
    ),
    item(
        -1,
        ("equipment", "electronics"),
        "Targeting Computer",
        "Targeting Computer",
        ["ISTargeting Computer", "CLTargeting Computer"],
    ),
]

miscellaneous_equipment: list[item] = [
    item(
        -1,
        ("equipment", "miscellaneous"),
        "Actuator Enhancement System",
        "AES",
        ["ISAES", "CLAES"],
    ),
    item(
        -1,
        ("equipment", "miscellaneous"),
        "Cellular Ammunition Storage Equipment",
        "CASE",
        ["ISCASE", "CLCASE"],
    ),
    item(
        -1,
        ("equipment", "miscellaneous"),
        "Cellular Ammunition Storage Equipment II",
        "CASE II",
        ["CLCASEII"],
    ),
    item(
        -1,
        ("equipment", "miscellaneous"),
        "Coolant Pod",
        "Coolant Pod",
        ["Coolant Pod", "IS Coolant Pod", "Clan Coolant Pod"],
    ),
    item(
        -1,
        ("equipment", "miscellaneous"),
        "PPC Capacitor",
        "PPC Capacitor",
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
        ("equipment", "maneuverability"),
        "Myomer Acceleration Signal Circuitry",
        "MASC",
        ["ISMASC", "CLMASC"],
    ),
    item(
        -1,
        ("equipment", "maneuverability"),
        "Mechanical Jump Boosters",
        "Mechanical Jump Boosters",
        ["MechanicalJumpBooster"],
    ),
    item(
        -1,
        ("equipment", "maneuverability"),
        "Partial Wing",
        "Partial Wing",
        ["ISPartialWing", "CLPartialWing"],
    ),
    item(
        -1,
        ("equipment", "maneuverability"),
        "Supercharger",
        "Supercharger",
        ["Supercharger"],
    ),
    item(
        -1,
        ("equipment", "maneuverability"),
        "Triple-Strength Myomer",
        "TSM",
        ["TSM", "Industrial TSM"],
    ),
    item(
        -1,
        ("equipment", "maneuverability"),
        "Underwater Maneuvering Unit",
        "UMU",
        ["UMU", "ISUMU", "CLUMU"],
    ),
    item(
        -1,
        ("equipment", "maneuverability"),
        "Jump Jets, Standard",
        "Standard Jump Jets",
        ["Jump Jet", "ISPrototypeJumpJet"],
    ),
    item(
        -1,
        ("equipment", "maneuverability"),
        "Jump Jets, Improved",
        "Improved Jump Jets",
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
