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

special_weapons: list[dict[str, list[str]]] = [
    {"Active Probe, Beagle": ["BeagleActiveProbe", "ISBeagleActiveProbe"]},
    {"Active Probe, Bloodhound": ["BloodhoundActiveProbe", "ISBloodhoundActiveProbe"]},
    {"Active Probe, light": ["CLLightActiveProbe"]},
    {
        "Anti-Missile System": [
            "ISAntiMissileSystem",
            "CLAntiMissileSystem",
            "Anti-Missile System",
        ]
    },
    {
        "Anti-Missile System, Laser": [
            "ISLaserAntiMissileSystem",
            "CLLaserAntiMissileSystem",
        ]
    },
    {"ECM Suite": ["CLECMSuite"]},
    {"ECM Suite, Angel": ["ISAngelECMSuite", "ISAngelECM", "CLAngelECMSuite"]},
    {"ECM Suite, Guardian": ["ISGuardianECM", "ISGuardianECMSuite"]},
    {"M-Pod": ["M-Pod"]},
    {
        "Target Acquisition Gear (TAG)": ["TAG", "ISTAG", "CLTAG", "Clan TAG"]
    },  # there's also "C3 Master with TAG" and "C3 Master Boosted with TAG"
    {
        "Target Acquisition Gear, Light (Light TAG)": [
            "Clan Light TAG",
            "CLLightTAG",
            "Light TAG",
        ]
    },
    {"Watchdog CEWS": ["WatchdogECMSuite"]},
]


physical_weapons: list[dict[str, list[str]]] = [
    {"Claws": ["IS Claw", "ISClaw"]},
    {"Flail": ["IS Flail", "ISFlail"]},
    {"Hatchet": ["Hatchet"]},
    {"Lance": ["IS Lance", "ISLance", "Lance"]},
    {"Mace": ["Mace"]},
    {
        "Vibroblade": [
            "ISSmallVibroBlade",
            "ISMediumVibroblade",
            "ISLargeVibroblade",
            "Small Vibroblade",
            "Medium Vibroblade",
            "Large Vibroblade",
        ]
    },
    {"Retractable Blade": ["Retractable Blade"]},
    {"Talons": ["Talons"]},
]

storage: list[dict[str, list[str]]] = [
    {"Liquid Storage": ["Liquid Storage"]},
    {"Cargo": ["Cargo"]},
]

electronics: list[dict[str, list[str]]] = [
    {"Comms Gear": ["Communications Equipment"]},
    {"Artemis IV FCS": ["ISArtemisIV", "CLArtemisIV"]},
    {"Artemis V FCS": ["CLArtemisV"]},
    {"C3 Computer, Master": ["ISC3MasterUnit", "ISC3MasterComputer"]},
    {"C3 Computer, Slave": ["ISC3SlaveUnit"]},
    {"C3i Computer": ["ISC3iUnit"]},
    {"C3 Boosted System, Master": ["ISC3MasterBoostedSystemUnit"]},
    {"C3 Boosted System, Slave": ["ISC3BoostedSystemSlaveUnit"]},
    {"MRM Apollo FCS": ["ISApollo"]},
    {"Targeting Computer": ["ISTargeting Computer", "CLTargeting Computer"]},
]

miscellaneous: list[dict[str, list[str]]] = [
    {"Actuator Enhancement System (AES)": ["ISAES", "CLAES"]},
    {"Cellular Ammunition Storage Equipment (CASE)": ["ISCASE", "CLCASE"]},
    {"Cellular Ammunition Storage Equipment II (CASE II)": ["CLCASEII"]},
    {"Coolant Pod": ["Coolant Pod", "IS Coolant Pod", "Clan Coolant Pod"]},
    {"Machine Gun Array": ["ISMGA", "CLMGA"]},
    {"Heavy Machine Gun Array": ["ISHMGA", "CLHMGA"]},
    {"Light Machine Gun Array": ["ISLMGA", "CLLMGA"]},
    {
        "PPC Capacitor": [
            "PPC Capacitor",
            "ISPPCCapacitor",
            "ISERPPCCapacitor",
            "ISHeavyPPCCapacitor",
            "ISLightPPCCapacitor",
        ]
    },
]

maneuverability: list[dict[str, list[str]]] = [
    {
        "Myomer Acceleration Signal Circuitry (MASC)": ["ISMASC", "CLMASC"]
    },  # some mechs with MASC have 'Myomer: MASC', others have 'Myomer: Standard'
    {"Mechanical Jump Boosters": ["MechanicalJumpBooster"]},
    {"Partial Wing": ["ISPartialWing", "CLPartialWing"]},
    {"Supercharger": ["Supercharger"]},
    {"Triple-Strength Myomer (TSM)": ["TSM", "Industrial TSM"]},
    {"Underwater Maneuvering Unit (UMU)": ["UMU", "ISUMU", "CLUMU"]},
    {"Jump Jets, Standard": ["Jump Jet", "ISPrototypeJumpJet"]},
    {
        "Jump Jets, Improved": [
            "Improved Jump Jet",
            "Clan Improved Jump Jet",
            "IS Improved Jump Jet",
            "ISImprovedJump Jet",
            "ISPrototypeImprovedJumpJet",
        ]
    },
]
