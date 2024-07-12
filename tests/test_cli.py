import subprocess
import tempfile
import json
from pathlib import Path


def test_convert_to_stdout() -> None:
    """
    Executes `mtf2json --mtf-file <FILE>` and checks if the output is valid JSON.
    """
    mtf_file = Path("tests/mtf/biped/Amarok_3.mtf")
    result = subprocess.run(
        ["poetry", "run", "mtf2json", "--mtf-file", str(mtf_file)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Process failed with return code {result.returncode}"
    try:
        json_data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        assert False, f"Output is not valid JSON: {e}"
    assert isinstance(json_data, dict), "Output JSON is not a dictionary"


def test_convert() -> None:
    """
    Executes `mtf2json --mtf-file <FILE> --convert` and checks if:
    - a JSON file with the same name but suffix `.json` is created
    - the JSON file contains valid json
    """
    mtf_file = Path("tests/mtf/biped/Banshee_BNC-3E.mtf")
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_mtf_file = Path(tmpdir) / mtf_file.name
        temp_json_file = temp_mtf_file.with_suffix('.json')
        temp_mtf_file.write_text(mtf_file.read_text())

        result = subprocess.run(
            ["poetry", "run", "mtf2json", "--mtf-file", str(temp_mtf_file), "--convert"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Process failed with return code {result.returncode}"
        assert temp_json_file.exists(), f"JSON file {temp_json_file} was not created"
        try:
            with open(temp_json_file, 'r') as f:
                json_data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Output file is not valid JSON: {e}"
        assert isinstance(json_data, dict), "Output JSON is not a dictionary"


def test_convert_to_specified_file() -> None:
    """
    Executes `mtf2json --mtf-file <FILE> --json-file <FILE>` and checks if
    the JSON file contains valid JSON.
    NOTE: `--convert` should be set automatically when `--json-file` is specified.
    """
    mtf_file = Path("tests/mtf/biped/Atlas_AS7-K.mtf")
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = Path(tmpdir) / "Amarok_3.json"
        result = subprocess.run(
            ["poetry", "run", "mtf2json", "--mtf-file", str(mtf_file), "--json-file", str(json_file)],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        assert result.returncode == 0, f"Process failed with return code {result.returncode}"
        assert json_file.exists(), f"JSON file {json_file} was not created"
        try:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Output file is not valid JSON: {e}"
        assert isinstance(json_data, dict), "Output JSON is not a dictionary"
