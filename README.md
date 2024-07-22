# mtf2json

`mtf2json` converts [MegaMek](https://github.com/MegaMek/)'s MTF file format to JSON.

## Project Goals and Features

- Simplify the parsing of MTF files across all modern programming languages by
  utilizing a widely-recognized and well-documented format (JSON).
- Provide a comprehensive JSON structure that includes all data from the MTF
  files, ensuring it is well-organized and clearly arranged.
- Address common issues with the MTF format, such as duplicate keys,
  inconsistent delimiters, and varying encodings.

## Why mtf2json?

MegaMek is a great project, but the MTF format is difficult to work with. It is
not standardized and there is no official specification (at least none that I
could find). Additionally, MTF files do not contain all the information
required to create an actual record sheet.

`mtf2json` does not simply create a 1:1 JSON version of the MTF data but
restructures the data and adds some information, such as structure pips. The
examples below illustrate the differences between various sections in the MTF
and JSON formats.

## Current State
### Conversion Rates

| Chassis Type | Conversion Rate |
|--------------|---------------|
| Biped | 100% (3954 / 3954) |
| Quad | Not supported |
| Tripod | Not supported |
| LAM | Not supported |

### Latest Supported MegaMek Commit

The most recent commit of the [MegaMek](https://github.com/MegaMek/megamek)
repository that `mtf2json` has been tested with can be displayd by running
`mtf2json --mm-commit`.

### Limitations

The MTF files are missing important information that is currenty not available in JSON either:
- Weapon damage, heat and ranges
- Ammunition quantity per slot

While it makes sense not to duplicate this data in each MTF file, I hoped that
it would be available in some easy-to-import format, e.g. CSV files. However,
I have not been able to find anything like that. It seems that much of this
information is hardcoded in JAVA.

### Testing

Testing mtf2json is challenging, primarily because the MTF format is so loosely
specified. I'm still not sure if I've encountered all possible keys and
understood all supported value syntaxes. Since there are over 4000 MTF files in
MegaMek, I cannot manually verify all conversion results. If you encounter
trouble converting an MTF file, please create a GitHub issue and attach the
file so I can verify and fix the issue.

## JSON Structure and Examples

Here are some comparisons of sections from an MTF file and their JSON counterparts:

### The Basic Stuff

MTF:
```
chassis:Atlas
model:AS7-K
mul id:144
```

JSON:
```json
"chassis": "Atlas",
"model": "AS7-K",
"mul_id": 144,
```

Most of the "flat" `key:value` pairs are also stored as `key:value` pairs in
JSON. However, numeric values are stored as `int` if appropriate (they remain
strings if they are used as names or model designation).

### Rules Level
MTF:
```
Rules Level:2
```

JSON:
```json
"rules_level": 2,
"rules_level_str": "Standard",
```

A string version of the rules level is automatically added. It's intended to be used in record sheets and determined using the same algorithm
as [MegaMek](https://github.com/juk0de/megamek/blob/78fb6e4616dd469dcb781c7da37d1bae748c45ce/megamek/src/megamek/common/SimpleTechLevel.java#L92).

### Quirks
MTF:
```
quirk:battle_fists_la
quirk:battle_fists_ra
quirk:command_mech
quirk:distracting
quirk:imp_com
```
JSON:
```json
"quirks": [
    "battle_fists_la",
    "battle_fists_ra",
    "command_mech",
    "distracting",
    "imp_com"
],
```
No more dealing with multiple identical keys - just a simple JSON list.

### Heat Sinks
MTF:
```
Heat Sinks:20 Single
```
JSON:
```json
"heat_sinks": {
    "quantity": 20,
    "type": "Single"
},
```

The type and quantity of heat sinks are separate keys, eliminating the need for additional parsing.

### Movement Points
MTF:
```
Walk MP:3
Jump MP:0
```
JSON:
```json
"walk_mp": 3,
"run_mp": 5,
"jump_mp": 0,
```

The movement points for running are calculated automatically for your convenience.

### Armor
MTF:
```  
armor:Standard(Inner Sphere)
LA armor:34
RA armor:34
LT armor:32
RT armor:32
CT armor:47
HD armor:9
LL armor:41
RL armor:41
RTL armor:10
RTR armor:10
RTC armor:14
```
JSON:
```json
"armor": {
    "type": "Standard",
    "left_arm": {
        "pips": 34
    },
    "right_arm": {
        "pips": 34
    },
    "left_torso": {
        "front": {
            "pips": 32
        },
        "rear": {
            "pips": 10
        }
    },
    "right_torso": {
        "front": {
            "pips": 32
        },
        "rear": {
            "pips": 10
        }
    },
    "center_torso": {
        "front": {
            "pips": 47
        },
        "rear": {
            "pips": 14
        }
    },
    "head": {
        "pips": 9
    },
    "left_leg": {
        "pips": 41
    },
    "right_leg": {
        "pips": 41
    }
},
```

Armor type, tech base (if available) and pips are stored in the `armor`
section. In case of patchwork armor, each location will have a `type` key:

```json
"armor": {
    "type": "Patchwork",
    "left_arm": {
        "pips": 26,
        "type": "Reactive(Inner Sphere)"
    },
}
```

Note that the tech base is not always available in the MTF file (i.e. sometimes
it's "Standard Armor", sometimes "Standard(Inner Sphere))".  Maybe "Standard"
always means "Inner Sphere", but I'm not sure, so I leave out the `tech_base`
entry in that case.

### Weapons
MTF:
```
Weapons:3
1 ISGaussRifle, Right Torso, Ammo:16
1 ISERLargeLaser, Left Arm
2 ISMediumPulseLaser, Center Torso (R)
```
JSON:
```json
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
        "ISERLargeLaser": {
            "location": "left_arm",
            "facing": "front",
            "quantity": 1
        }
    },
    "3": {
        "ISMediumPulseLaser": {
            "location": "center_torso",
            "facing": "rear",
            "quantity": 2
        }
    },
},
```

Location, facing, quantity and ammo are all individual keys for each weapon.
Additionally, each weapon has a slot number that represents its order in the
MTF file (and on the record sheet). Some MTF files contain individual entries
for identical weapons in the same location (i.e., no quantity at the beginning
of the line). These entries are automatically merged.

### Structure
MTF:
```
structure:IS Standard
```
JSON:
```json
"structure": {
    "type": "Standard",
    "head": {
        "pips": 3
    },
    "center_torso": {
        "pips": 31
    },
    "left_torso": {
        "pips": 21
    },
    "right_torso": {
        "pips": 21
    },
    "left_arm": {
        "pips": 17
    },
    "right_arm": {
        "pips": 17
    },
    "left_leg": {
        "pips": 21
    },
    "right_leg": {
        "pips": 21
    }
},
```

The structure type and tech base (if available) are stored in the `structure`
section. The pips are added afterward, based on the mech's tonnage. "IS" is
converted to "Inner Sphere" to maintain consistency with the tech base naming
in the `armor` section. Note that the tech base is not always available in the
MTF file (e.g. sometimes it's "IS Standard," sometimes just "Standard"). Maybe
"Standard" always means "Inner Sphere," but I'm not sure, so I leave out the
`tech_base` entry in that case.

### Critical Slots
MTF:
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
JSON:
```json
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
    "10": null,
    "11": null,
    "12": null
  },
}
```

All critical slot data is stored in the `critical_slots` section, with a separate
section for each location. Each slot uses its slot number as the key, making it
very easy to check the content of each slot directly. The `-Empty-` string is
replaced by an actual `null` (Python `None`).

### Fluff
MTF:
```
overview:The Banshee, introduced in 2445 by the Terran Hegemony, is a 'Mech that was designed specifically for close-assault operations during the early years of BattleMech warfare.
capabilities:A contemporary of the Mackie and Emperor, the Banshee is undeniably fast for one of the heaviest 'Mechs ever produced, and with fifteen tons of armor it is better protected than most other assault 'Mechs. However the use of a massive GM 380 fusion engine left little room for weaponry, and even at the time of its introduction the Banshee was considered undergunned compared to its privately-built competition. As critics noted, what use was impressive armor and mobility if a better-armed enemy could overwhelm and destroy it? The result was a mediocre 'Mech which even the lowly Rifleman could beat as long as it prevented the Banshee's mass from coming into play.
deployment:The two primary weapons on the Banshee, a Magna Hellstar PPC matched up with an Imperator-A Autocannon/5 with one ton of ammo, are mounted in the right and left sides of its torso. The two systems complement each other with similar range profiles and would provide good firepower for a 'Mech weighing at half the tonnage of the Banshee. Perversely for a close-combat 'Mech their minimum ranges means both weapons present targeting difficulties as the Banshee closes in on its enemy, and a Magna Mk I Small Laser mounted in its head appears to have been installed as an afterthought. Sixteen heat sinks help keep the 'Mech cool though, and thanks to its prodigious size the Banshee can turn lighter 'Mechs to scrap in hand-to-hand fighting.
history: The Hegemony soldiered on though, producing five thousand Banshees in a decade before its poor combat performance finally forced them to stop production in 2455 and the 'Mech was relegated to training and militia units for the next few centuries. Even during the Succession Wars the 'Mech's poor reputation meant many commanders saw it as a liability rather than an asset; unless they were fighting on a backwater Periphery world or as part of a poorly-equipped outfit, most Banshees were placed in second-line reserves to provide fire support or fulfill the role of brawlers so that better-armed 'Mechs need not engage in hand-to-hand combat. In this way fully a third of the original Banshee production run remained operational by the dawn of the thirty-first century and could be found throughout the Inner Sphere and Periphery, with the lion's share residing within the Lyran Commonwealth. Though a few attempts had been made over the years to improve the Banshee, Defiance Industries was the first to produce a variant which markedly improved on the original and was suggested by many of its original critics. With help from the Federated Suns and access to blueprints from the original Hesperus II factories, the BNC-3S proved to be such a success the Lyrans began fielding them in front line units, surprising their enemies who ignored them to focus on "real" threats with thoroughly unexpected firepower. Under the Federated Commonwealth improvements would continue to be made, though not at the same priority level as other projects, and the much-improved BNC-5S was active in time to meet the Clan Invasion.
manufacturer:Diplass BattleMechs,Witten Industries,Defiance Industries,Star League Weapons Research
primaryfactory:Apollo,Hesperus II,Hesperus II,New Earth
systemmanufacturer:CHASSIS:Star League
systemmode:CHASSIS:XT
systemmanufacturer:ENGINE:GM
systemmode:ENGINE:380
systemmanufacturer:ARMOR:Starshield
systemmanufacturer:COMMUNICATIONS:Dalban
systemmode:COMMUNICATIONS:Commline
systemmanufacturer:TARGETING:Dalban
systemmode:TARGETING:HiRez-B
```
JSON:
```json
"fluff": {
  "overview": "The Banshee, introduced in 2445 by the Terran Hegemony, is a 'Mech that was designed specifically for close-assault operations during the early years of BattleMech warfare.",
  "capabilities": "A contemporary of the Mackie and Emperor, the Banshee is undeniably fast for one of the heaviest 'Mechs ever produced, and with fifteen tons of armor it is better protected than most other assault 'Mechs. However the use of a massive GM 380 fusion engine left little room for weaponry, and even at the time of its introduction the Banshee was considered undergunned compared to its privately-built competition. As critics noted, what use was impressive armor and mobility if a better-armed enemy could overwhelm and destroy it? The result was a mediocre 'Mech which even the lowly Rifleman could beat as long as it prevented the Banshee's mass from coming into play.",
  "deployment": "The two primary weapons on the Banshee, a Magna Hellstar PPC matched up with an Imperator-A Autocannon/5 with one ton of ammo, are mounted in the right and left sides of its torso. The two systems complement each other with similar range profiles and would provide good firepower for a 'Mech weighing at half the tonnage of the Banshee. Perversely for a close-combat 'Mech their minimum ranges means both weapons present targeting difficulties as the Banshee closes in on its enemy, and a Magna Mk I Small Laser mounted in its head appears to have been installed as an afterthought. Sixteen heat sinks help keep the 'Mech cool though, and thanks to its prodigious size the Banshee can turn lighter 'Mechs to scrap in hand-to-hand fighting.",
  "history": "The Hegemony soldiered on though, producing five thousand Banshees in a decade before its poor combat performance finally forced them to stop production in 2455 and the 'Mech was relegated to training and militia units for the next few centuries. Even during the Succession Wars the 'Mech's poor reputation meant many commanders saw it as a liability rather than an asset; unless they were fighting on a backwater Periphery world or as part of a poorly-equipped outfit, most Banshees were placed in second-line reserves to provide fire support or fulfill the role of brawlers so that better-armed 'Mechs need not engage in hand-to-hand combat. In this way fully a third of the original Banshee production run remained operational by the dawn of the thirty-first century and could be found throughout the Inner Sphere and Periphery, with the lion's share residing within the Lyran Commonwealth. Though a few attempts had been made over the years to improve the Banshee, Defiance Industries was the first to produce a variant which markedly improved on the original and was suggested by many of its original critics. With help from the Federated Suns and access to blueprints from the original Hesperus II factories, the BNC-3S proved to be such a success the Lyrans began fielding them in front line units, surprising their enemies who ignored them to focus on \"real\" threats with thoroughly unexpected firepower. Under the Federated Commonwealth improvements would continue to be made, though not at the same priority level as other projects, and the much-improved BNC-5S was active in time to meet the Clan Invasion.",
  "manufacturer": [
    "Diplass BattleMechs",
    "Witten Industries",
    "Defiance Industries",
    "Star League Weapons Research"
  ],
  "primaryfactory": [
    "Apollo",
    "Hesperus II",
    "Hesperus II",
    "New Earth"
  ],
  "systemmanufacturer": {
    "chassis": "Star League",
    "engine": "GM",
    "armor": "Starshield",
    "communications": "Dalban",
    "targeting": "Dalban"
  },
  "systemmode": {
    "chassis": "XT",
    "engine": "380",
    "communications": "Commline",
    "targeting": "HiRez-B"
  }
}
```

I created a new section `fluff` that contains all the additional information
usually not required for playing or creating record sheets.  As you can
see, the MTF keys `systemmanufacturer` and `systemmode` can appear multiple
times in an MTF file and contain a "subkey" (i.e. a nested `key:value` pair
within the value). I separated all these "subkeys" into individual
`key:value` pairs and organized them neatly. Also, the `manufacturer` and
`primaryfactory` values are always lists, as they often contain multiple
values.

## Installation

### PyPi

```sh
pip install mtf2json
```

### Manual
Clone the repository and install the dependencies:

```sh
git clone https://github.com/juk0de/mtf2json.git
cd mtf2json
pip install .
```

## Usage

### CLI
To convert a single MTF file to JSON, use the following command:

```sh
mtf2json --mtf-file <path_to_mtf_file> [--convert] [--json-file <path_to_json_file>]
```

To query JSON data in the terminal (e.g. armor pips of left arm), pipe the output into `jq`:
```sh
mtf2json --mtf-file <path_to_mtf_file> | jq .armor.left_arm.pips
```

To convert all MTF files in a directory, including subdirectories, use the following command:

```sh
mtf2json --mtf-dir <path_to_mtf_dir> --recursive [--json-dir <path_to_json_dir>]
```

If you mant to convert all current MTF files, use the MegaMek Github repository
with the latest supported commit. You can clone it like this:

```
git clone git@github.com:MegaMek/megamek.git && cd megamek && git reset --hard $(mtf2json --mm-commit)
```

The use `mtf2json` with the `--mtf-dir` option as described above.

### Library
```python
from mtf2json import read_mtf
from pathlib import Path
json_data = read_mtf(Path('/my/file.mtf'))
```

## Development
* Install [poetry](https://python-poetry.org/docs/)
* Clone repository and `cd` into it
* Execute `poetry install`
* To run tests, execute `poetry run pytest`
* To run `mtf2json`, execute `poetry run mtf2json`

## License

All source code in this project is licensed under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
The included MTF files are part of the MegaMek project and are, therefore, licensed under the GPLv2 license (see
https://github.com/MegaMek/#current-project-status). These files are provided unmodified and solely for testing purposes.
