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
This module handles all euqipment that has to be added to the
'Weapons and Equipment' section of the record sheet by storing
it in a dedicated 'equipment' section in the JSON data.

Because that kind of equipment is scattered across the various
critical slot entries in the MTF files (with different equipment
having different format, e. g. some contain a ':SIZE:' value),
it is added after the JSON conversion, in a separate step.

The equipment names below contain the verbatim names (including all
variants). The reason for this is, that we want to have consistent
equipment names. Unfortunately, this is currently not the case in
the MTF files, e.g. ECM Suites are sometimes called "ECMSuite" and
sometimes just "ECM". Therefore we're mapping the various names from
the MTF files to new default names.

Another issue is that some MTF files contain some equipment in the
'Weapons' sections while others don't. If we want to separate cleanly
between weapons and equipment (as done in the rulebooks), we need to
know all existing names for a given equipment.
"""

# The default name is the key, the verbatim names are the values.
# MTF names are case insensitive and anything in paranthesis (e.g.
# '(omnipod)') is ignored (and thus, not part of the verbatim name
# lists).
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

storage = ["Liquid Storage", "Cargo"]
