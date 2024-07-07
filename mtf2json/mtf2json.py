"""
Converts MegaMek's MTF format to JSON. Restructures the data to make it easily accessible.
Adds some data for convenience (e.g. internal structure pips).
"""
import json
import re
from math import ceil
from pathlib import Path
from typing import Dict, Any, Tuple, Union, Optional, List, cast, TextIO


version = "0.1.2"
mm_version = "0.49.19.1"


class ConversionError(Exception):
    pass


# the dictionaries below all contain converted keys,
# not the original MTF ones (see '__extract_key_value()')
critical_slot_keys = [
    'left_arm',
    'right_arm',
    'left_torso',
    'right_torso',
    'center_torso',
    'head',
    'left_leg',
    'right_leg'
]
armor_pips_keys = [
    'la_armor',
    'ra_armor',
    'lt_armor',
    'rt_armor',
    'ct_armor',
    'hd_armor',
    'll_armor',
    'rl_armor',
    'rtl_armor',
    'rtr_armor',
    'rtc_armor'
]
fluff_keys = [
    'overview',
    'capabilities',
    'deployment',
    'history',
    'manufacturer',
    'primaryfactory',
    'systemmode',
    'systemmanufacturer'
]
# internally renamed keys
renamed_keys = {
    'la_armor': 'left_arm',
    'ra_armor': 'right_arm',
    'lt_armor': 'left_torso',
    'rt_armor': 'right_torso',
    'ct_armor': 'center_torso',
    'hd_armor': 'head',
    'll_armor': 'left_leg',
    'rl_armor': 'right_leg',
    'rtl_armor': 'left_torso',
    'rtr_armor': 'right_torso',
    'rtc_armor': 'center_torso',
}
# keys that should always be stored as strings,
# even if they can sometimes be numbers
string_keys = ['model']


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


def __extract_key_value(line: str) -> Tuple[str, str]:
    """
    Extract key and value from the given MTF line.
    The key is converted to our internal representation
    (all lower case, ' ' replaced by '_').
    """
    key, value = line.split(':', 1)
    key = key.strip().lower().replace(' ', '_')
    value = value.strip()
    return (key, value)


def __add_weapon(line: str, weapon_section: Dict[str, Dict[str, Dict[str, Union[str, int]]]]) -> None:
    """
    Add a weapon to the given `weapons` section dictionary.
    The MTF section starts with the key 'Weapons:', followed by the total nr. of weapons
    (which we don't store in JSON). The lines below the section start line each describe
    one weapon slot (until the next section starts). Each weapon slot line consists of:
    - the weapon quantity (optional), ended by ` `
    - the weapon name, ended by `,`
    - the location, ended either by `,`, end of line or `(R)`
    - if the location is followed by `(R)` on the same line, the `facing` of the weapon
      changes to `rear`, otherwise `facing` is always `front`
    - ammo quantity, consisting of the word `Ammo`, followed by `:` and the ammo quantity
    Here's an MTF example containing all of the described features (Atlas AS7-K):
        ```
        Weapons:6
        1 ISGaussRifle, Right Torso, Ammo:16
        1 ISLRM20, Left Torso, Ammo:12
        1 ISERLargeLaser, Left Arm
        1 ISERLargeLaser, Right Arm
        2 ISMediumPulseLaser, Center Torso (R)
        1 ISAntiMissileSystem, Left Arm, Ammo:12
        ```
    And here's how the JSON looks like (the key for each individual weapon entry
    is the slot number, which is simply increased, starting with `1`):
        ```
        "weapons": {
            "1": {
                "ISGaussRifle": {
                    "location": "right_torso",
                    "facing": "front",
                    "quantity": 1,
                    "ammo": 16
                }
            },
            "2": {
                "ISLRM20": {
                    "location": "left_torso",
                    "facing": "front",
                    "quantity": 1,
                    "ammo": 12
                }
            },
            "3": {
                "ISERLargeLaser": {
                    "location": "left_arm",
                    "facing": "front",
                    "quantity": 1
                }
            },
            "4": {
                "ISERLargeLaser": {
                    "location": "right_arm",
                    "facing": "front",
                    "quantity": 1
                }
            },
            "5": {
                "ISMediumPulseLaser": {
                    "location": "center_torso",
                    "facing": "rear",
                    "quantity": 2
                }
            },
            "6": {
                "ISAntiMissileSystem": {
                    "location": "left_arm",
                    "facing": "front",
                    "quantity": 1,
                    "ammo": 12
                }
            }
        },

        ```
    """
    slot_number = len(weapon_section) + 1
    weapon_data = {}

    # Extract weapon quantity if present
    quantity_match = re.match(r'(\d+)\s+', line)
    if quantity_match:
        quantity = int(quantity_match.group(1))
        line = line[quantity_match.end():]
    else:
        quantity = 1

    # Extract weapon name
    weapon_name, line = line.split(',', 1)
    weapon_name = weapon_name.strip()

    # Extract location and facing
    location_match = re.match(r'([^,]+)(,|$)', line)
    if location_match:
        location = location_match.group(1).strip()
        line = line[location_match.end():]
        facing = 'rear' if '(R)' in location else 'front'
        location = location.replace('(R)', '').strip()
    else:
        location = line.strip()
        facing = 'front'

    # Extract ammo quantity if present
    ammo_match = re.search(r'Ammo:(\d+)', line)
    if ammo_match:
        ammo = int(ammo_match.group(1))
    else:
        ammo = None

    # Populate weapon data
    weapon_data[weapon_name] = {
        'location': location.lower().replace(' ', '_'),
        'facing': facing,
        'quantity': quantity
    }
    if ammo is not None:
        weapon_data[weapon_name]['ammo'] = ammo

    # Add weapon data to the weapon section
    weapon_section[str(slot_number)] = weapon_data


def __add_armor(value: str, armor_section: Dict[str, Union[str, Dict[str, Any]]]) -> None:
    """
    Add the armor section.
    The MTF `Armor:` key in is a bit of a mess: it can contain a value that only describes
    the type of armor, e.g:
        ```
        Armor:Standard Armor
        ```
    or the type + tech base (delimited by `(...)`), e.g.:
        ```
        Armor:Standard(Inner Sphere)
        ```
    Furthermore the type description is not consistent. E.g. it can be `Standard` or
    `Standard Armor`. We try to clean up the mess a bit by storing all available
    information in the JSON 'armor' section, while also choosing a consistent type string:
        ```
        "armor": {
            "type": "Standard",
            "tech_base: "Inner Sphere"
            ...
        }
        ```
    Note that `tech_base` is optional (only added if there's a string in `(...)`) and
    that the term 'Armor' has been removed from the type string.
    """
    # Extract type and tech base if present
    if '(' in value and ')' in value:
        type_, tech_base = value.split('(', 1)
        tech_base = tech_base.rstrip(')')
    else:
        type_ = value
        tech_base = None

    # Clean up type string
    type_ = type_.replace(' Armor', '').strip()

    # Populate armor section
    armor_section['type'] = type_
    if tech_base:
        armor_section['tech_base'] = tech_base.strip()


def __add_armor_pips(key: str, value: str, armor_pips_section: Dict[str, Any]) -> None:
    """
    Add armor pips to the given `armor_pips` section dictionary.
    The armor pips are stored as individual keys in an MTF file:
        ```
        LA armor:21
        RA armor:21
        LT armor:30
        RT armor:30
        CT armor:40
        HD armor:9
        LL armor:26
        RL armor:26
        RTL armor:10
        RTR armor:10
        RTC armor:17
        ```
    We're structuring the values in the JSON 'armor' section like this:
        ```
        "armor": {
            ...
            "pips": {
                "left_arm": 21,
                "right_arm": 21,
                "left_torso": {
                  "front": 30,
                  "rear": 10
                },
                "right_torso": {
                  "front": 30,
                  "rear": 10
                },
                "center_torso": {
                  "front": 40,
                  "rear": 17
                },
                "head": 9,
                "left_leg": 26,
                "right_leg": 26
            },
        }
        ```
    """
    # center torso (front and rear)
    if key in ['ct_armor', 'rtc_armor']:
        if 'center_torso' not in armor_pips_section:
            armor_pips_section['center_torso'] = {}
        side = 'front' if key == 'ct_armor' else 'rear'
        armor_pips_section['center_torso'][side] = int(value)
    # right torso (front and rear)
    elif key in ['rt_armor', 'rtr_armor']:
        if 'right_torso' not in armor_pips_section:
            armor_pips_section['right_torso'] = {}
        side = 'front' if key == 'rt_armor' else 'rear'
        armor_pips_section['right_torso'][side] = int(value)
    # left torso (front and rear)
    elif key in ['lt_armor', 'rtl_armor']:
        if 'left_torso' not in armor_pips_section:
            armor_pips_section['left_torso'] = {}
        side = 'front' if key == 'lt_armor' else 'rear'
        armor_pips_section['left_torso'][side] = int(value)
    else:
        armor_pips_section[key] = int(value)


def __add_structure(value: str, structure_section: Dict[str, Any]) -> None:
    """
    Add the structure section.
    The MTF `Structure:` key has a value that either represents the structure type only, e.g.:
        ```
        Structure:Standard
        ```
    or the tech base + type (separated by the first ` `), e.g.:
        ```
        structure:IS Standard
        structure:IS Endo Steel
        structure:Clan Endo Steel
        ```
    Similar to the `armor` section, we store all information in the `structure` JSON section, e.g.:
        ```
        "structure": {
            ...
            "type": "Standard",
            "tech_base": "Inner Sphere"
        }
        ```
        Note that `tech_base` is optional and we convert 'IS' to 'Inner Sphere', in order to be
        consistent with the `armor` section names.
        ```
    """
    # Extract tech base and type if present
    parts = value.split(' ', 1)
    if parts[0] in ['IS', 'Clan']:
        tech_base = 'Inner Sphere' if parts[0] == 'IS' else parts[0]
        type_ = parts[1] if len(parts) > 1 else ''
    else:
        tech_base = None
        type_ = value

    # Populate structure section
    structure_section['type'] = type_.strip()
    if tech_base:
        structure_section['tech_base'] = tech_base.strip()


def __merge_weapons(mech_data: Dict[str, Any]) -> None:
    """
    Sometimes the MTF format contains individual entries for identical weapons in the
    same location, e.g.:
        ```
        Small Pulse Laser, Left Arm
        Small Pulse Laser, Left Arm
        Small Pulse Laser, Left Arm
        ```
    These will result in separate entries in the JSON file. This function merges all
    identical weapons in the same location to a single entry, so it looks like this:
        ```
        "1": {
            "Small Pulse Laser": {
                "location": "left_arm",
                "facing": "front",
                "quantity": 3
            }
        },
        ```
    """
    weapon_dict: Dict[Tuple[str, str, str], Dict[str, Union[str, int]]] = {}
    for weapon_data in mech_data.get('weapons', {}).values():
        for weapon_name, details in weapon_data.items():
            key = (weapon_name, details['location'], details['facing'])
            if key in weapon_dict and 'quantity' in weapon_dict[key]:
                weapon_dict[key]['quantity'] += details['quantity']
            else:
                weapon_dict[key] = details

    merged_weapons: Dict[str, Dict[str, Dict[str, Union[str, int]]]] = {}
    slot_number = 1
    for slot_number, ((weapon_name, location, facing), details) in enumerate(weapon_dict.items(), start=1):
        merged_weapons[str(slot_number)] = {weapon_name: details}

    mech_data['weapons'] = merged_weapons


def __add_biped_structure_pips(mech_data: Dict[str, Any]) -> None:
    """
    Add the structure pips for biped mechs based on the tonnage.
    The structure are not part of an MTF file. Instead, they are
    computed and added later (see 'Mech.java'). We add them to
    the JSON structure for convenience, like this:
        ```
        "structure": {
            ...
            "pips": {
                "left_arm": 17,
                "right_arm": 17,
                "left_torso": 21,
                "right_torso": 21,
                "center_torso": 31,
                "head": 3,
                "left_leg": 21,
                "right_leg": 21
            },
        }
        ```
    """
    # Static list of pips for each weight
    # The list order is: [Head, Center Torso, L/R Torso, L/R Arm, L/R Leg]
    biped_weight_pips = {
        10: [3, 4, 3, 1, 2],
        15: [3, 5, 4, 2, 3],
        20: [3, 6, 5, 3, 4],
        25: [3, 8, 6, 4, 6],
        30: [3, 10, 7, 5, 7],
        35: [3, 11, 8, 6, 8],
        40: [3, 12, 10, 6, 10],
        45: [3, 14, 11, 7, 11],
        50: [3, 16, 12, 8, 12],
        55: [3, 18, 13, 9, 13],
        60: [3, 20, 14, 10, 14],
        65: [3, 21, 15, 10, 15],
        70: [3, 22, 15, 11, 15],
        75: [3, 23, 16, 12, 16],
        80: [3, 25, 17, 13, 17],
        85: [3, 27, 18, 14, 18],
        90: [3, 29, 19, 15, 19],
        95: [3, 30, 20, 16, 20],
        100: [3, 31, 21, 17, 21],
        105: [4, 32, 22, 17, 22],
        110: [4, 33, 23, 18, 23],
        115: [4, 35, 24, 19, 24],
        120: [4, 36, 25, 20, 25],
        125: [4, 38, 26, 21, 26],
        130: [4, 39, 27, 21, 27],
        135: [4, 41, 28, 22, 28],
        140: [4, 42, 29, 23, 29],
        145: [4, 44, 31, 24, 31],
        150: [4, 45, 32, 25, 32],
        155: [4, 47, 33, 26, 33],
        160: [4, 48, 34, 26, 34],
        165: [4, 50, 35, 27, 35],
        170: [4, 51, 36, 28, 36],
        175: [4, 53, 37, 29, 37],
        180: [4, 54, 38, 30, 38],
        185: [4, 56, 39, 31, 39],
        190: [4, 57, 40, 31, 40],
        195: [4, 59, 41, 32, 41],
        200: [4, 60, 42, 33, 42],
    }
    if 'mass' not in mech_data:
        raise ConversionError("Mech data must contain 'mass' to calculate structure pips.")

    mass = mech_data['mass']
    if mass not in biped_weight_pips:
        raise ConversionError(f"Unsupported mech mass: {mass}")

    pips = biped_weight_pips[mass]
    mech_data['structure']['pips'] = {
        'head': pips[0],
        'center_torso': pips[1],
        'left_torso': pips[2],
        'right_torso': pips[2],
        'left_arm': pips[3],
        'right_arm': pips[3],
        'left_leg': pips[4],
        'right_leg': pips[4]
    }


def __add_crit_slot(line: str, crit_slots_section: Dict[str, Optional[str]]) -> None:
    """
    Add a critical slot entry.
    The MDF contains one critical slot section per location. Here's an example for the left arm:
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
    slot_number = len(crit_slots_section) + 1
    crit_slots_section[str(slot_number)] = line if line != '-Empty-' else None


def __remove_p_tags(text: str) -> str:
    """
    Remove <p> and </p> tags from the given text.
    """
    return text.replace('<p>', '').replace('</p>', '')


def __add_fluff(key: str, value: str, fluff_section: Dict[str, Union[str, List[str], Dict[str, str]]]) -> None:
    value = __remove_p_tags(value)
    """
    Add the given fluff key and value to the 'fluff section'.
    Some of the fluff keys can appear multiple times in an MTF file, e.g.:
        ```
        systemmanufacturer:CHASSIS:Star League
        systemmanufacturer:ENGINE:GM
        systemmanufacturer:ARMOR:Starshield
        systemmanufacturer:TARGETING:Dalban
        systemmanufacturer:COMMUNICATIONS:Dalban
        systemmode:ENGINE:380
        systemmode:CHASSIS:XT
        systemmode:TARGETING:HiRez-B
        systemmode:COMMUNICATIONS:Commline
        ```
    All fluff keys that appear more than once have "subkeys", i.e. the given
    value contains another key / value pair separated by `:`. We create
    a JSON subsection for each "primary" key and add the "subkey" entries to it,
    e.g.:
        ```
        "systemmanufacturer": {
            "chassis": "Star League",
            "engine": "GM",
            "armor": "Starshield"
            "targeting": "Dalban",
            "communication": "Dalban"
        },
        "systemmode": {
            "engine": "380",
            "chassis": "XT",
            "targeting": "HiRez-B",
            "communications": "Commline"
        },
        ...
    The following keys can contain lists as values (separated by `,`):
        ```
        manufacturer
        primaryfactory
        ```
    In this case we store the values as JSON lists, e.g.:
        ```
        "manufacturer": [
            "Defiance Industries",
            "Hegemony Research and Development Department",
            "Weapons Division"
        ],
        "primaryfactory": [
            "Hesperus II",
            "New Earth"
        ],
        ...
        ```
    All other keys and values are added verbatim.
    """
    # the key is already in the fluff section
    # -> it's a subsection
    if key in fluff_section:
        subkey, subvalue = value.split(':', 1)
        if isinstance(fluff_section[key], dict):
            cast(dict, fluff_section[key])[subkey.lower()] = subvalue.strip()
        else:
            raise ConversionError(f"Fluff key entry '{key}' is not a dictionary!")
    # the key is new
    else:
        # value contains a subkey
        # -> create a new subsection
        if ':' in value:
            subkey, subvalue = value.split(':', 1)
            # but ONLY if the subkey is all UPPERCASE, e.g.:
            # ```
            # systemmanufacturer:CHASSIS:Republic-R
            # ```
            # Otherwise we could turn some of the longer text strings
            # (that sometimes contain `:`) into dicts.
            if subkey.isupper():
                fluff_section[key] = {subkey.lower(): subvalue.strip()}
            else:
                fluff_section[key] = value
        # value contains a list
        elif key in ['manufacturer', 'primaryfactory']:
            fluff_section[key] = [item.strip() for item in value.split(',')]
        # simple value
        else:
            fluff_section[key] = value


def __add_rules_level_str(mech_data: Dict[str, Union[str, int]]) -> None:
    """
    Add a rules level string, to be used as the "Rules Level" record sheet entry.
    The string is determined based on the code in 'SimpleTechLevel.java', which
    converts the compound tech levels to simplified rules level.

    However, those levels are NOT always identical to those from the MUL.
    E.g. the 'Atlas II AS7-D-H (Devlin)' is listed as 'Experimental' in MUL,
    but has rules level 'Standard' in MegaMek.
    """
    introductory_levels = [0]
    standard_levels = [1, 2, 3, 4]
    advanced_levels = [5, 6]
    experimental_levels = [7, 8]
    unofficial_levels = [9, 10]

    # add rules level string based on 'rules_level' number
    if mech_data['rules_level'] in introductory_levels:
        mech_data['rules_level_str'] = 'Introductory'
    elif mech_data['rules_level'] in standard_levels:
        mech_data['rules_level_str'] = 'Standard'
    elif mech_data['rules_level'] in advanced_levels:
        mech_data['rules_level_str'] = 'Advanced'
    elif mech_data['rules_level'] in experimental_levels:
        mech_data['rules_level_str'] = 'Experimental'
    elif mech_data['rules_level'] in unofficial_levels:
        mech_data['rules_level_str'] = 'Unofficial'
    else:
        raise ConversionError(f"Found invalid rules_level: {mech_data['rules_level']}")


def __add_heat_sinks(value: str, heat_sinks_section: Dict[str, Union[int, str]]) -> None:
    """
    Add heat sinks section.
    Heat sinks are stored as a flat key:value pair in the MTF file, with the value containing
    both type and quantity of heat sinks, e.g.:
        ```
        heat sinks:10 IS Double
        ```
    We separate heat sink type and quantity, using the first ` ` as delimiter, and store them
    in a JSON section like this:
        ```
        "heat_sinks": {
            "quantity": 10,
            "type": "IS Double"
        }
        ```
    """
    quantity, type_ = value.split(' ', 1)
    heat_sinks_section['quantity'] = int(quantity)
    heat_sinks_section['type'] = type_.strip()


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


def read_mtf(path: Path) -> Dict[str, Any]:
    """
    Read given MTF file and return content as JSON.
    """
    mech_data: Dict[str, Any] = {}

    current_section = None
    with open(path, 'r') as file:
        __check_compat(file)
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # === a line with a key ===
            # -> exclude lines where `:` is preceded by `,`
            #    (see '__add_weapon()')
            if ':' in line and not re.search(r',[^,]*:', line):
                key, value = __extract_key_value(line)
                # = rules_level =
                # -> add a 'rules_level_str' for convenience
                if key == 'rules_level':
                    mech_data['rules_level'] = int(value)
                    __add_rules_level_str(mech_data)
                # = heat_sinks =
                elif key == 'heat_sinks':
                    mech_data['heat_sinks'] = {}
                    __add_heat_sinks(value, mech_data['heat_sinks'])
                # = walk_mp =
                # -> calculate and add 'run_mp' for convenience
                elif key == 'walk_mp':
                    mech_data[key] = int(value)
                    mech_data['run_mp'] = ceil(int(value) * 1.5)
                # = armor_pips =
                elif key == 'armor' or key in armor_pips_keys:
                    if 'armor' not in mech_data:
                        mech_data['armor'] = {}
                    if 'pips' not in mech_data['armor']:
                        mech_data['armor']['pips'] = {}
                    if key == 'armor':
                        __add_armor(value, mech_data['armor'])
                    elif key in armor_pips_keys:
                        __add_armor_pips(key, value, mech_data['armor']['pips'])
                # = structure =
                elif key == 'structure':
                    if 'structure' not in mech_data:
                        mech_data['structure'] = {}
                    __add_structure(value, mech_data['structure'])
                # = critical_slots : section start =
                # Section structure: starts with any of the keys in 'critical_slot_keys'
                # and contains one value per line below (until the next section starts)
                elif key in critical_slot_keys:
                    current_section = key
                    if 'critical_slots' not in mech_data:
                        mech_data['critical_slots'] = {}
                    mech_data['critical_slots'][current_section] = {}
                # = weapons : section start =
                elif key == 'weapons':
                    current_section = key
                    mech_data[current_section] = {}
                # = quirks =
                # The MTF file can contain multiple 'quirk' entries
                # that we merge in a single JSON 'quirks' section
                elif key == 'quirk':
                    if 'quirks' not in mech_data:
                        mech_data['quirks'] = []
                    mech_data['quirks'].append(value)
                # = fluff =
                elif key in fluff_keys:
                    if 'fluff' not in mech_data:
                        mech_data['fluff'] = {}
                    __add_fluff(key, value, mech_data['fluff'])
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
            # === a line without a key ===
            # a weapon entry
            elif current_section == 'weapons':
                if line:
                    __add_weapon(line, mech_data[current_section])
            # a critical slot entry
            elif current_section and current_section in critical_slot_keys:
                __add_crit_slot(line, mech_data['critical_slots'][current_section])

    # merge identical weapons
    __merge_weapons(mech_data)
    # add structure pips
    if __is_biped_mech(mech_data['config']):
        __add_biped_structure_pips(mech_data)
    # rename some keys before returning JSON data
    return __rename_keys(mech_data)


def write_json(data: Dict[str, Any], path: Path) -> None:
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
