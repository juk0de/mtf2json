"""
Converts MegaMek's MTF format to JSON. Restructures the data to make it easily accessible.
Adds some data for convenience (e.g. internal structure pips).
"""
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

import json
import re
import codecs
from math import ceil
from pathlib import Path
from typing import Any, TextIO, Iterator
from .error import ConversionError  # noqa
from .weapons import add_weapon, merge_weapons
from .armor import add_armor_type, add_armor_locations
from .structure import add_structure_type, add_biped_structure_pips
from .critical_slots import add_crit_slot
from .quirks import add_quirk, add_weapon_quirk
from .fluff import add_fluff
from .rules_level import add_rules_level
from .heat_sinks import add_heat_sinks
from .equipment import add_equipment_section


version = "0.2.5"
mm_commit = "dfeb43e28132c2723ac8e3147e41b00960b989fd"


# the dictionaries below all contain converted keys,
# not the original MTF ones (see '__extract_key_value()')
critical_slot_keys = [
    "left_arm",
    "right_arm",
    "left_torso",
    "right_torso",
    "center_torso",
    "head",
    "left_leg",
    "right_leg",
]
armor_location_keys = [
    "la_armor",
    "ra_armor",
    "lt_armor",
    "rt_armor",
    "ct_armor",
    "hd_armor",
    "ll_armor",
    "rl_armor",
    "rtl_armor",
    "rtr_armor",
    "rtc_armor",
]
fluff_keys = [
    "overview",
    "capabilities",
    "deployment",
    "history",
    "manufacturer",
    "primaryfactory",
    "systemmode",
    "systemmanufacturer",
]
other_keys = [
    "generator",
    "chassis",
    "model",
    "mul_id",
    "config",
    "techbase",
    "era",
    "source",
    "rules_level",
    "role",
    "mass",
    "engine",
    "myomer",
    "cockpit",
    "gyro",
    "walk_mp",
    "jump_mp",
    "heat_sinks",
    "quirk",
    "weaponquirk",
    "structure",
    "armor",
    "weapons",
    "clanname",
    "base_chassis_heat_sinks",
    "ejection",
    "notes",
]
# keys that are intentionally ignored
ignored_keys = [
    "fluffimage",
    "imagefile",
    "nocrit",
]

# internally renamed keys
renamed_keys = {
    "la_armor": "left_arm",
    "ra_armor": "right_arm",
    "lt_armor": "left_torso",
    "rt_armor": "right_torso",
    "ct_armor": "center_torso",
    "hd_armor": "head",
    "ll_armor": "left_leg",
    "rl_armor": "right_leg",
    "rtl_armor": "left_torso",
    "rtr_armor": "right_torso",
    "rtc_armor": "center_torso",
}

# keys that should always be stored as strings,
# even if they can sometimes be numbers
string_keys = ["model"]

# dict for the '--statistics' option
statistics: dict[str, dict[str, list[str]]] = {
    "unknown_keys": {},
    "empty_value_keys": {},
    "no_key_lines": {},
}


def __add_statistics(category: str, key: str, file: str) -> None:
    """
    Add given entry and file to the given statistics category.
    """
    if key not in statistics[category]:
        statistics[category][key] = []
    if file not in statistics[category][key]:
        statistics[category][key].append(file)


# decoder that catches utf8 decoding errors and switches to cp1252
def mixed_decoder(error: UnicodeError) -> tuple[str, int]:
    bs: bytes = error.object[error.start : error.end]  # type: ignore[attr-defined]
    return bs.decode("cp1252"), error.start + 1  # type: ignore[attr-defined]


codecs.register_error("mixed", mixed_decoder)


def __key_is_known(key: str) -> bool:
    """
    Checks if he given key is known.
    """
    return (
        key in critical_slot_keys
        or key in armor_location_keys
        or key in fluff_keys
        or key in other_keys
        or key in ignored_keys
    )


def __rename_keys(obj: Any) -> Any:
    """
    Rename the keys in the given object according to
    the `renamed_keys` dictionary.
    """
    if isinstance(obj, dict):
        return {renamed_keys.get(k, k): __rename_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [__rename_keys(i) for i in obj]
    else:
        return obj


def __extract_key_value(line: str) -> tuple[str, str]:
    """
    Extract key and value from the given MTF line.
    The key is converted to our internal representation
    (all lower case, ' ' replaced by '_').
    """
    key, value = line.split(":", 1)
    key = key.strip().lower().replace(" ", "_")
    value = value.strip()
    return (key, value)


def __is_biped_mech(config_value: str) -> bool:
    """
    Return 'True' if given 'Config:' value belongs to a biped mech,
    'False' otherwise.
    """
    # 'Biped' or 'Biped Omnimech'
    return config_value.startswith("Biped")


def __check_compat(file: TextIO) -> None:
    """
    Check compatibility of given file.
    We're checking two things:
        1. A key named `Config` must exist
           -> otherwise it's not a valid MTF file
        2. The value of `Config` must be `Biped`
          -> we currently only support biped mechs
    If the check fails, we raise a `ConversionError`.
    """
    config_found = False
    for line in file:
        if line.startswith("Config:"):
            config_found = True
            key, value = __extract_key_value(line)
            # 'Biped' or 'Biped Omnimech'
            if not __is_biped_mech(value):
                raise ConversionError("Only 'Biped' mechs are supported.")
            break
    # no 'Config:' key -> invalid file
    if not config_found:
        raise ConversionError("The MTF file is not valid. 'Config' key is missing.")
    # reset file pointer
    file.seek(0)


def __read_line(
    file: TextIO, filename: str, verbose: bool = False
) -> Iterator[tuple[str, str, str]]:
    """
    A generator that reads the next line and returns (key, value, section).
    The value may be empty. This can be because of an empty value in the MTF file,
    or it indicates the beginning of a new section (the calling function must
    distinguish between those cases based on the key).
    """

    key: str = ""
    value: str = ""
    section: str = "other"
    for i, line in enumerate(file):
        line = line.strip()
        if verbose:
            print(f"==> Analyzing line {i+1}: {line}")
            print(f"> last section: '{section}'")
        if not line or line.startswith("#"):
            if verbose:
                print("> skipping line because it's empty or a comment")
            continue
        if ":" in line:
            # === filter out lines that contain `:` but are NOT key:value entries ===
            # line belongs to a weapon (`:` is part of `, Ammo:` and there is NO preceding `:`)
            # -> see __add_weapon()
            if section == "weapons" and re.search(r"^[^:]*,[^:]*:", line):
                if verbose:
                    print(
                        f"> detected weapon entry in 'weapons' section: ['{key}', '{line}', '{section}']"
                    )
                yield (key, line, section)
                continue
            # line belongs to a critical slot (`:` is part of `:size:` or `:SIZE:`)
            # -> keep the size in the value, will be handled by 'add_equipment_section'
            elif section == "critical_slots" and ":size:" in line.lower():
                value = line
                if verbose:
                    print(
                        f"> detected critical slot entry in 'critical_slots' section: ['{key}', '{value}', '{section}']"
                    )
                yield (key, value, section)
                continue

            # === determine key, value and current section ===
            key, value = __extract_key_value(line)
            # ignore lines with unknown keys
            # -> fixes #14 and similar issues
            if not __key_is_known(key):
                if verbose:
                    print(f"> detected line with unknown key '{key}', skipping it")
                __add_statistics("unknown_keys", key, filename)
                continue
            if key in ignored_keys:
                if verbose:
                    print(f"> detected line with ignored key '{key}', skipping it")
                continue
            elif key == "armor" or key in armor_location_keys:
                section = "armor"
            elif key in critical_slot_keys:
                section = "critical_slots"
                # set value to '', to signal that the crit slot section starts
                # but this is not a crit slot entry
                value = ""
            elif key == "weapons":
                section = "weapons"
                # set value to '', to signal that the weapon section starts
                # but this is not a weapon entry
                value = ""
            elif key in fluff_keys:
                section = "fluff"
            else:
                section = "other"
            if verbose:
                print(
                    f"> detected key, value and section: ['{key}', '{value}', '{section}']"
                )
            if value == "" and section not in ["weapons", "armor", "critical_slots"]:
                __add_statistics("empty_value_keys", key, filename)
            yield (key, value, section)
            continue
        else:
            # weapon and crit slot entries are handled by the calling function
            # -> yield the last key, since it's required for adding crit slots
            if section == "weapons":
                if verbose:
                    print(
                        f"> detected weapon entry in 'weapons' section: ['{key}', '{line}', '{section}']"
                    )
                yield (key, line, section)
            elif section == "critical_slots":
                if verbose:
                    print(
                        f"> detected critical slot entry in 'critical_slots' section: ['{key}', '{line}', '{section}']"
                    )
                yield (key, line, section)
            # a line without a key
            else:
                if verbose:
                    print(
                        "> line contains no key and is no known special case, skipping it"
                    )
                __add_statistics("no_key_lines", line, filename)
                continue
    return None


def read_mtf(path: Path, verbose: bool = False) -> dict[str, Any]:
    """
    Read given MTF file and return content as JSON.
    """
    mech_data: dict[str, Any] = {}

    with open(path, "r", encoding="utf8", errors="mixed") as file:
        __check_compat(file)
        mech_data["mtf2json"] = version
        for key, value, section in __read_line(file, path.name, verbose):
            # = rules level =
            if key == "rules_level":
                add_rules_level(value, mech_data)
            # = heat sinks =
            elif key in ["heat_sinks", "base_chassis_heat_sinks"]:
                add_heat_sinks(key, value, mech_data)
            # = walk mp =
            # -> calculate and add 'run_mp' for convenience
            elif key == "walk_mp":
                mech_data[key] = int(value)
                mech_data["run_mp"] = ceil(int(value) * 1.5)
            # = structure =
            elif key == "structure":
                add_structure_type(value, mech_data)
            # = armor =
            elif section == "armor":
                if key == "armor":
                    add_armor_type(value, mech_data)
                elif key in armor_location_keys:
                    add_armor_locations(key, value, mech_data)
            # = critical slot =
            elif section == "critical_slots":
                add_crit_slot(key, value, mech_data)
            # = weapon =
            elif section == "weapons":
                add_weapon(value, mech_data)
            # = fluff =
            elif section == "fluff":
                add_fluff(key, value, mech_data)
            # = quirks =
            elif key == "quirk":
                add_quirk(value, mech_data)
            # = weapon quirk =
            elif key == "weaponquirk":
                add_weapon_quirk(value, mech_data)
            # = other key:value pair =
            else:
                # convert to int if possible
                # -> except for those keys that should always be strings!
                if key not in string_keys:
                    try:
                        mech_data[key] = int(value)
                    except ValueError:
                        mech_data[key] = value
                else:
                    mech_data[key] = value

    # rename some keys
    mech_data = __rename_keys(mech_data)
    # merge identical weapons
    merge_weapons(mech_data)
    # add equipment section
    add_equipment_section(mech_data)
    # add structure pips
    if __is_biped_mech(mech_data["config"]):
        add_biped_structure_pips(mech_data)
    return mech_data


def write_json(data: dict[str, Any], path: Path) -> None:
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)
