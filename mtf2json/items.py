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
        - a category (e.g ("weapon", "ranged", "missile"))
        - a name (e.g. "Target Acquisition Gear")
        - a list with known MTF names (e.g. critical slot entries)
        - a tech base (e.g. "Clan")
        - an optional short name (e.g. "TAG")
    """

    key: int
    name: str
    category: tuple[str, ...]
    mtf_names: list[str]
    tech_base: Literal["unknown", "IS", "Clan"] = "unknown"
    short_name: str | None = None


class ItemError(Exception):
    pass


ranged_weapons: list[item] = [
    # Ballistic weapons
    item(
        key=-1,
        name="Autocannon/2",
        category=("weapon", "ranged", "ballistic"),
        mtf_names=[],
        short_name="AC/2",
    ),
    item(
        -1,
        "Autocannon/5",
        ("weapon", "ranged", "ballistic"),
        [],
        short_name="AC/5",
    ),
    item(
        -1,
        "Autocannon/10",
        ("weapon", "ranged", "ballistic"),
        [],
        short_name="AC/10",
    ),
    item(
        -1,
        "Autocannon/20",
        ("weapon", "ranged", "ballistic"),
        [],
        short_name="AC/20",
    ),
    item(
        -1,
        "Light Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Heavy Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Improved Heavy Gauss",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Magshot Gauss Rifle",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Silver Bullet Gauss",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "LB 2-X AC",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "LB 5-X AC",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "LB 10-X AC",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "LB 20-X AC",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Light AC/2",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Light AC/5",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Light Machine Gun",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Machine Gun",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Heavy Machine Gun",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Machine Gun Array",
        ("weapon", "ranged", "ballistic"),
        ["ISMGA", "CLMGA"],
    ),
    item(
        -1,
        "Heavy Machine Gun Array",
        ("weapon", "ranged", "ballistic"),
        ["ISHMGA", "CLHMGA"],
    ),
    item(
        -1,
        "Light Machine Gun Array",
        ("weapon", "ranged", "ballistic"),
        ["ISLMGA", "CLLMGA"],
    ),
    item(
        -1,
        "Light Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Medium Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Heavy Rifle (Cannon)",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Rotary AC/2",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Rotary AC/5",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Ultra AC/2",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Ultra AC/5",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    item(
        -1,
        "Ultra AC/10",
        ("weapon", "ranged", "ballistic"),
        [],
    ),
    # Energy weapons
    item(
        -1,
        "Binary (Blazer) Cannon",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Flamer",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER Flamer",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Heavy Flamer",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Small Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Medium Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Large Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER Small Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER Medium Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER Large Laser",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Plasma Rifle",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Light PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Heavy PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "ER PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    item(
        -1,
        "Snub-Nose PPC",
        ("weapon", "ranged", "energy"),
        [],
    ),
    # Pulse weapons
    item(
        -1,
        "Small Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Medium Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Large Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Small X-Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Medium X-Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Large X-Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
    ),
    item(
        -1,
        "Small Re-engineered Laser",
        ("weapons", "ranged", "pulse"),
        [],
        short_name="Small RE Laser",
    ),
    item(
        -1,
        "Medium Re-engineered Laser",
        ("weapons", "ranged", "pulse"),
        [],
        short_name="Medium RE Laser",
    ),
    item(
        -1,
        "Large Re-engineered Laser",
        ("weapons", "ranged", "pulse"),
        [],
        short_name="Large RE Laser",
    ),
    item(
        -1,
        "Small Variable-Speed Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
        short_name="Small VSP Laser",
    ),
    item(
        -1,
        "Medium Variable-Speed Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
        short_name="Medium VSP Laser",
    ),
    item(
        -1,
        "Large Variable-Speed Pulse Laser",
        ("weapons", "ranged", "pulse"),
        [],
        short_name="Large VSP Laser",
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
        "Anti-Missile System, Laser",
        ("weapon", "special"),
        ["ISLaserAntiMissileSystem", "CLLaserAntiMissileSystem"],
        short_name="Laser AMS",
    ),
    item(
        -1,
        "ECM Suite",
        ("weapon", "special"),
        ["CLECMSuite"],
    ),
    item(
        -1,
        "ECM Suite, Angel",
        ("weapon", "special"),
        ["ISAngelECMSuite", "ISAngelECM", "CLAngelECMSuite"],
        short_name="Angel ECM",
    ),
    item(
        -1,
        "ECM Suite, Guardian",
        ("weapon", "special"),
        ["ISGuardianECM", "ISGuardianECMSuite"],
        short_name="Guardian ECM",
    ),
    item(
        -1,
        "M-Pod",
        ("weapon", "special"),
        ["M-Pod"],
    ),
    item(
        -1,
        "Target Acquisition Gear",
        ("weapon", "special"),
        ["TAG", "ISTAG", "CLTAG", "Clan TAG"],
        short_name="TAG",
    ),  # there's also "C3 Master with TAG" and "C3 Master Boosted with TAG"
    item(
        -1,
        "Target Acquisition Gear, Light",
        ("weapon", "special"),
        ["Clan Light TAG", "CLLightTAG", "Light TAG"],
        short_name="Light TAG",
    ),
    item(
        -1,
        "Watchdog Composite Electronic Warfare System",
        ("weapon", "special"),
        ["WatchdogECMSuite"],
        short_name="Watchdog CEWS",
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
        short_name="Comms Gear",
    ),
    item(
        -1,
        "Artemis IV Fire-Control System",
        ("equipment", "electronics"),
        ["ISArtemisIV", "CLArtemisIV"],
        short_name="Artemis IV FCS",
    ),
    item(
        -1,
        "Artemis V Fire-Control System",
        ("equipment", "electronics"),
        ["CLArtemisV"],
        short_name="Artemis V FCS",
    ),
    item(
        -1,
        "C3 Computer, Master",
        ("equipment", "electronics"),
        ["ISC3MasterUnit", "ISC3MasterComputer"],
        short_name="C3 Computer (Master)",
    ),
    item(
        -1,
        "C3 Computer, Slave",
        ("equipment", "electronics"),
        ["ISC3SlaveUnit"],
        short_name="C3 Computer (Slave)",
    ),
    item(
        -1,
        "C3i Computer",
        ("equipment", "electronics"),
        ["ISC3iUnit"],
    ),
    item(
        -1,
        "C3 Boosted System, Master",
        ("equipment", "electronics"),
        ["ISC3MasterBoostedSystemUnit"],
        short_name="C3 Boosted System (Master)",
    ),
    item(
        -1,
        "C3 Boosted System, Slave",
        ("equipment", "electronics"),
        ["ISC3BoostedSystemSlaveUnit"],
        short_name="C3 Boosted System (Slave)",
    ),
    item(
        -1,
        "MRM Apollo Fire-Control System",
        ("equipment", "electronics"),
        ["ISApollo"],
        short_name="MRM Apollo FCS",
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
        "Actuator Enhancement System",
        ("equipment", "miscellaneous"),
        ["ISAES", "CLAES"],
        short_name="AES",
    ),
    item(
        -1,
        "Cellular Ammunition Storage Equipment",
        ("equipment", "miscellaneous"),
        ["ISCASE", "CLCASE"],
        short_name="CASE",
    ),
    item(
        -1,
        "Cellular Ammunition Storage Equipment II",
        ("equipment", "miscellaneous"),
        ["CLCASEII"],
        short_name="CASE II",
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
        "Myomer Acceleration Signal Circuitry",
        ("equipment", "maneuverability"),
        ["ISMASC", "CLMASC"],
        short_name="MASC",
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
        "Triple-Strength Myomer",
        ("equipment", "maneuverability"),
        ["TSM", "Industrial TSM"],
        short_name="TSM",
    ),
    item(
        -1,
        "Underwater Maneuvering Unit",
        ("equipment", "maneuverability"),
        ["UMU", "ISUMU", "CLUMU"],
        short_name="UMU",
    ),
    item(
        -1,
        "Jump Jets, Standard",
        ("equipment", "maneuverability"),
        ["Jump Jet", "ISPrototypeJumpJet"],
        short_name="Jump Jets",
    ),
    item(
        -1,
        "Jump Jets, Improved",
        ("equipment", "maneuverability"),
        [
            "Improved Jump Jet",
            "Clan Improved Jump Jet",
            "IS Improved Jump Jet",
            "ISImprovedJump Jet",
            "ISPrototypeImprovedJumpJet",
        ],
        short_name="Improved Jump Jets",
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
