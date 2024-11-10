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

About the dict structure:
 * The default name is the key, the verbatim names are the values.
 * MTF names are case insensitive and anything in paranthesis (e.g.
   '(omnipod)' or '[Clan]') is ignored for naming (and thus, not
   part of the verbatim name lists).
 * Default names are taken from the BattleMech Manual, with abbrevations
   in paranthesis (if any)
"""

from dataclasses import dataclass


@dataclass
class name:
    full_name: str
    short_name: str
    mtf_names: list[str]


weapons: list[name] = [
    name(
        "Machine Gun Array",
        "MGA",
        ["ISMGA", "CLMGA"],
    ),
    name(
        "Heavy Machine Gun Array",
        "Heavy MGA",
        ["ISHMGA", "CLHMGA"],
    ),
    name(
        "Light Machine Gun Array",
        "Light MGA",
        ["ISLMGA", "CLLMGA"],
    ),
]

special_weapons: list[name] = [
    name(
        "Active Probe, Beagle",
        "Beagle Active Probe",
        ["BeagleActiveProbe", "ISBeagleActiveProbe"],
    ),
    name(
        "Active Probe, Bloodhound",
        "Bloodhound Active Probe",
        ["BloodhoundActiveProbe", "ISBloodhoundActiveProbe"],
    ),
    name(
        "Active Probe, light",
        "Light Active Probe",
        ["CLLightActiveProbe"],
    ),
    name(
        "Anti-Missile System",
        "AMS",
        ["ISAntiMissileSystem", "CLAntiMissileSystem", "Anti-Missile System"],
    ),
    name(
        "Anti-Missile System, Laser",
        "Laser AMS",
        ["ISLaserAntiMissileSystem", "CLLaserAntiMissileSystem"],
    ),
    name(
        "ECM Suite",
        "ECM Suite",
        ["CLECMSuite"],
    ),
    name(
        "ECM Suite, Angel",
        "Angel ECM",
        ["ISAngelECMSuite", "ISAngelECM", "CLAngelECMSuite"],
    ),
    name(
        "ECM Suite, Guardian",
        "Guardian ECM",
        ["ISGuardianECM", "ISGuardianECMSuite"],
    ),
    name(
        "M-Pod",
        "M-Pod",
        ["M-Pod"],
    ),
    name(
        "Target Acquisition Gear",
        "TAG",
        ["TAG", "ISTAG", "CLTAG", "Clan TAG"],
    ),  # there's also "C3 Master with TAG" and "C3 Master Boosted with TAG"
    name(
        "Target Acquisition Gear, Light",
        "Light TAG",
        ["Clan Light TAG", "CLLightTAG", "Light TAG"],
    ),
    name(
        "Watchdog Composite Electronic Warfare System",
        "Watchdog CEWS",
        ["WatchdogECMSuite"],
    ),
]

physical_weapons: list[name] = [
    name(
        "Claws",
        "Claws",
        ["IS Claw", "ISClaw"],
    ),
    name(
        "Flail",
        "Flail",
        ["IS Flail", "ISFlail"],
    ),
    name(
        "Hatchet",
        "Hatchet",
        ["Hatchet"],
    ),
    name(
        "Lance",
        "Lance",
        ["IS Lance", "ISLance", "Lance"],
    ),
    name(
        "Mace",
        "Mace",
        ["Mace"],
    ),
    name(
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
    name(
        "Retractable Blade",
        "Retractable Blade",
        ["Retractable Blade"],
    ),
    name(
        "Talons",
        "Talons",
        ["Talons"],
    ),
]

storage: list[name] = [
    name(
        "Liquid Storage",
        "Liquid Storage",
        ["Liquid Storage"],
    ),
    name(
        "Cargo",
        "Cargo",
        ["Cargo"],
    ),
]

electronics: list[name] = [
    name(
        "Communications Equipment",
        "Comms Gear",
        ["Communications Equipment"],
    ),
    name(
        "Artemis IV Fire-Control System",
        "Artemis IV FCS",
        ["ISArtemisIV", "CLArtemisIV"],
    ),
    name(
        "Artemis V Fire-Control System",
        "Artemis V FCS",
        ["CLArtemisV"],
    ),
    name(
        "C3 Computer, Master",
        "C3 Computer (Master)",
        ["ISC3MasterUnit", "ISC3MasterComputer"],
    ),
    name(
        "C3 Computer, Slave",
        "C3 Computer (Slave)",
        ["ISC3SlaveUnit"],
    ),
    name(
        "C3i Computer",
        "C3i Computer",
        ["ISC3iUnit"],
    ),
    name(
        "C3 Boosted System, Master",
        "C3 Boosted System (Master)",
        ["ISC3MasterBoostedSystemUnit"],
    ),
    name(
        "C3 Boosted System, Slave",
        "C3 Boosted System (Slave)",
        ["ISC3BoostedSystemSlaveUnit"],
    ),
    name(
        "MRM Apollo Fire-Control System",
        "MRM Apollo FCS",
        ["ISApollo"],
    ),
    name(
        "Targeting Computer",
        "Targeting Computer",
        ["ISTargeting Computer", "CLTargeting Computer"],
    ),
]

miscellaneous: list[name] = [
    name(
        "Actuator Enhancement System",
        "AES",
        ["ISAES", "CLAES"],
    ),
    name(
        "Cellular Ammunition Storage Equipment",
        "CASE",
        ["ISCASE", "CLCASE"],
    ),
    name(
        "Cellular Ammunition Storage Equipment II",
        "CASE II",
        ["CLCASEII"],
    ),
    name(
        "Coolant Pod",
        "Coolant Pod",
        ["Coolant Pod", "IS Coolant Pod", "Clan Coolant Pod"],
    ),
    name(
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

maneuverability: list[name] = [
    name(
        "Myomer Acceleration Signal Circuitry",
        "MASC",
        ["ISMASC", "CLMASC"],
    ),
    name(
        "Mechanical Jump Boosters",
        "Mechanical Jump Boosters",
        ["MechanicalJumpBooster"],
    ),
    name(
        "Partial Wing",
        "Partial Wing",
        ["ISPartialWing", "CLPartialWing"],
    ),
    name(
        "Supercharger",
        "Supercharger",
        ["Supercharger"],
    ),
    name(
        "Triple-Strength Myomer",
        "TSM",
        ["TSM", "Industrial TSM"],
    ),
    name(
        "Underwater Maneuvering Unit",
        "UMU",
        ["UMU", "ISUMU", "CLUMU"],
    ),
    name(
        "Jump Jets, Standard",
        "Standard Jump Jets",
        ["Jump Jet", "ISPrototypeJumpJet"],
    ),
    name(
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
