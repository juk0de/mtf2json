from pathlib import Path
import pytest
import json
from mtf2json.mtf2json import read_mtf
from typing import Dict, Any


def validate_data_vs_reference(json_data: Dict[str, Any], json_reference: Dict[str, Any]) -> None:
    """
    Compares every key in the given data and reference (type and value) and asserts that the data
    in `json_data` is identical to the one in the `json_reference` reference data.
    """
    def compare_dicts(d1: Dict[str, Any], d2: Dict[str, Any], path: str = "") -> None:
        for key in d1:
            if key not in d2:
                raise AssertionError(f"Key '{path + key}' not found in reference data.")
            if isinstance(d1[key], dict):
                if not isinstance(d2[key], dict):
                    raise AssertionError(f"Type mismatch at '{path + key}': expected dict, found {type(d2[key])}.")
                compare_dicts(d1[key], d2[key], path + key + ".")
            elif isinstance(d1[key], list):
                if not isinstance(d2[key], list):
                    raise AssertionError(f"Type mismatch at '{path + key}': expected list, found {type(d2[key])}.")
                if len(d1[key]) != len(d2[key]):
                    raise AssertionError(f"Length mismatch at '{path + key}': expected {len(d1[key])}, found {len(d2[key])}.")
                for index, (item1, item2) in enumerate(zip(d1[key], d2[key])):
                    if isinstance(item1, dict):
                        compare_dicts(item1, item2, path + key + f"[{index}].")
                    else:
                        if item1 != item2:
                            raise AssertionError(f"Value mismatch at '{path + key}[{index}]': expected {item1}, found {item2}.")
            else:
                if d1[key] != d2[key]:
                    raise AssertionError(f"Value mismatch at '{path + key}': expected {d1[key]}, found {d2[key]}.")

    compare_dicts(json_data, json_reference)


@pytest.mark.parametrize('mtf_file, json_file', [('./mtf/biped/Banshee_BNC-3E.mtf', './json/biped/Banshee_BNC-3E.json')])
def test_specific_biped(mtf_file: str, json_file: str) -> None:
    """
    Reads the given MTF and JSON files from the parameter list and compares them using `validate_data_vs_reference()`.
    """
    mtf_path = Path(mtf_file)
    json_path = Path(json_file)

    # Read MTF file and convert to JSON data
    json_data = read_mtf(mtf_path)

    # Read JSON reference file
    with open(json_path, 'r') as file:
        json_reference = json.load(file)

    # Validate data
    validate_data_vs_reference(json_data, json_reference)
