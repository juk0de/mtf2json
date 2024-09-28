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
from typing import Any


def add_crit_slot(key: str, value: str, mech_data: dict[str, Any]) -> None:
    """
    Add a critical slot entry.

    The MTF contains one critical slot section per location. It start with the location
    name and no value. Each following line contains a slot entry with no key. However,
    it may contain a `:` if it contains a `:SIZE:` option, but that is filtered by
    `__read_line()`.

    Here's an example for the left arm:
        ```
        Left Arm:
        Shoulder
        Upper Arm Actuator
        Lower Arm Actuator
        Hand Actuator
        Heat Sink
        Heat Sink
        ISERLargeLaser
        ISERLargeLaser
        ISAntiMissileSystem
        -Empty-
        -Empty-
        -Empty-
        ```
    In JSON, we put all locations into the `critical_slots` section and add a counter for each slot.
    Also, we replace `-Empty-` with `None`:
        ```
        "critical_slots": {
            "left_arm": {
                "1": "Shoulder",
                "2": "Upper Arm Actuator",
                "3": "Lower Arm Actuator",
                "4": "Hand Actuator",
                "5": "Heat Sink",
                "6": "Heat Sink",
                "7": "ISERLargeLaser",
                "8": "ISERLargeLaser",
                "9": "ISAntiMissileSystem",
                "10": None,
                "11": None,
                "12": None
            },
        ```
    """
    # create section if it does not exist
    if "critical_slots" not in mech_data:
        mech_data["critical_slots"] = {}

    # create new subsection if value is empty
    if not value:
        mech_data["critical_slots"][key] = {}
    # otherwise add the given slot entry
    else:
        crit_slots_section: dict[str, str | None] = mech_data["critical_slots"][key]
        slot_number = len(crit_slots_section) + 1
        crit_slots_section[str(slot_number)] = value if value != "-Empty-" else None
