from pathlib import Path
from mtf2json.mtf2json import read_mtf
from typing import Any, Dict, Union, List


def validate_json_structure(json_data: Dict[str, Any]) -> None:
    def check_keys(data: Dict[str, Any], expected_keys: List[str]) -> None:
        for key in expected_keys:
            assert key in data, f"Missing key: {key}"

    def check_type(value: Any, expected_type: Union[type, str]) -> None:
        if isinstance(expected_type, str):
            assert isinstance(value, eval(expected_type)), f"Expected type {expected_type} but got {type(value)}"
        else:
            assert isinstance(value, expected_type), f"Expected type {expected_type} but got {type(value)}"

    def check_str_value(value: str, expected_value: str) -> None:
        assert value == expected_value, f"Wrong value: '{value}' (expected '{expected_value}')"

    check_keys(json_data, ["chassis", "model", "mul_id", "config", "techbase", "era", "source", "rules_level", "rules_level_str",
                           "role", "quirks", "mass", "engine", "structure", "myomer", "heat_sinks", "walk_mp", "run_mp",
                           "jump_mp", "armor", "weapons", "critical_slots", "fluff"])

    check_keys(json_data["fluff"], ["overview", "capabilities", "deployment", "history", "manufacturer",
                                    "primaryfactory", "systemmanufacturer"])
    check_type(json_data["fluff"]["overview"], str)
    check_type(json_data["fluff"]["capabilities"], str)
    check_type(json_data["fluff"]["deployment"], str)
    check_type(json_data["fluff"]["history"], str)
    check_type(json_data["fluff"]["manufacturer"], list)
    for item in json_data["fluff"]["manufacturer"]:
        check_type(item, str)
    check_type(json_data["fluff"]["primaryfactory"], list)
    for item in json_data["fluff"]["primaryfactory"]:
        check_type(item, str)
    check_type(json_data["fluff"]["systemmanufacturer"], dict)
    check_keys(json_data["fluff"]["systemmanufacturer"], ["chassis", "engine", "armor", "communications", "targeting"])
    for key in json_data["fluff"]["systemmanufacturer"]:
        check_type(json_data["fluff"]["systemmanufacturer"][key], str)

    check_type(json_data["chassis"], str)
    check_type(json_data["model"], str)
    check_type(json_data["mul_id"], int)
    check_type(json_data["config"], str)
    check_type(json_data["techbase"], str)
    check_type(json_data["era"], int)
    check_type(json_data["source"], str)
    check_type(json_data["rules_level"], int)
    check_type(json_data["rules_level_str"], str)
    check_type(json_data["role"], str)
    check_type(json_data["quirks"], list)
    check_type(json_data["mass"], int)
    check_type(json_data["engine"], str)
    check_type(json_data["structure"], dict)
    # these models have tech_base "IS" encoded in the "Structure:" value
    if json_data['model'] in ["AS7-K-DC", "BNC-3E"]:
        check_keys(json_data["structure"], ["type", "tech_base"])
        check_type(json_data["structure"]["tech_base"], str)
        # "IS" is translated to "Inner Sphere"
        check_str_value(json_data["structure"]["tech_base"], "Inner Sphere")
    # Amarok 3 has "Clan Endo Steel" structure
    # -> check correct separation of type and tech base
    elif json_data['chassis'] == "Amarok" and json_data["model"] == "3":
        check_keys(json_data["structure"], ["type", "tech_base"])
        check_type(json_data["structure"]["tech_base"], str)
        check_str_value(json_data["structure"]["tech_base"], "Clan")
        check_str_value(json_data["structure"]["type"], "Endo Steel")
    check_type(json_data["structure"]["type"], str)
    check_keys(json_data["structure"], ["type", "head", "center_torso", "left_torso", "right_torso",
                                        "left_arm", "right_arm", "left_leg", "right_leg"])
    for key in json_data["structure"]:
        if key in ["head", "center_torso", "left_torso", "right_torso", "left_arm", "right_arm", "left_leg", "right_leg"]:
            check_type(json_data["structure"][key], dict)
            check_type(json_data["structure"][key]["pips"], int)
    check_type(json_data["myomer"], str)
    check_type(json_data["heat_sinks"], dict)
    check_keys(json_data["heat_sinks"], ["quantity", "type"])
    check_type(json_data["heat_sinks"]["quantity"], int)
    check_type(json_data["heat_sinks"]["type"], str)
    check_type(json_data["walk_mp"], int)
    check_type(json_data["run_mp"], int)
    check_type(json_data["jump_mp"], int)
    check_type(json_data["armor"], dict)
    check_keys(json_data["armor"], ["left_arm", "right_arm", "left_torso", "right_torso",
                                    "center_torso", "head", "left_leg", "right_leg"])
    check_type(json_data["armor"]["type"], str)
    check_keys(json_data["armor"], ["left_arm", "right_arm", "left_torso", "right_torso",
                                    "center_torso", "head", "left_leg", "right_leg"])
    for key, value in json_data["armor"].items():
        if isinstance(value, dict):
            if "pips" in value:
                check_type(value["pips"], int)
            if "front" in value:
                check_type(value["front"], dict)
            if "rear" in value:
                check_type(value["rear"], dict)
        else:
            check_type(value, str)
    check_type(json_data["weapons"], dict)
    check_type(json_data["critical_slots"], dict)
    check_type(json_data["fluff"], dict)


def validate_mtf_conversion(mtf_file: Path):
    print(f"=== Validating '{mtf_file}' ===")
    json_data = read_mtf(mtf_file)
    expected_keys = {"chassis", "model", "mul_id", "config",
                     "techbase", "era", "source", "rules_level",
                     "rules_level_str", "role", "quirks", "mass", "engine",
                     "structure", "myomer", "heat_sinks", "walk_mp",
                     "run_mp", "jump_mp", "armor", "weapons",
                     "critical_slots", "fluff"}
    assert expected_keys.issubset(json_data.keys()), f"Missing keys in {mtf_file.name}: {expected_keys - json_data.keys()}"
    validate_json_structure(json_data)


def test_biped_examples():
    mtf_folder = Path(__file__).parent / 'mtf/biped'
    mtf_files = mtf_folder.glob('*.mtf')
    for mtf_file in mtf_files:
        validate_mtf_conversion(Path(mtf_file))
