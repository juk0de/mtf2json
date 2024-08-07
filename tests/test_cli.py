import subprocess
import tempfile
import json
from pathlib import Path
import shutil


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
    print(result.stdout)
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
        shutil.copy(mtf_file, temp_mtf_file)

        result = subprocess.run(
            ["poetry", "run", "mtf2json", "--mtf-file", str(temp_mtf_file), "--convert"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        assert result.returncode == 0, f"Process failed with return code {result.returncode}"
        assert temp_json_file.exists(), f"JSON file {temp_json_file} was not created"
        try:
            with open(temp_json_file, 'r') as f:
                json_data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Output file is not valid JSON: {e}"
        assert isinstance(json_data, dict), "Output JSON is not a dictionary"


def test_convert_to_json_file() -> None:
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


def test_convert_directory() -> None:
    """
    Executes `mtf2json --mtf-dir` and checks if:
    - JSON files are created for each MTF file (with suffix '.json')
    - all JSON files contain valid JSON data
    """
    mtf_dir = Path("tests/mtf/biped")
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_mtf_dir = Path(tmpdir) / "biped"
        temp_mtf_dir.mkdir(parents=True, exist_ok=True)
        for mtf_file in mtf_dir.glob("*.mtf"):
            temp_mtf_file = temp_mtf_dir / mtf_file.name
            shutil.copy(mtf_file, temp_mtf_file)

        result = subprocess.run(
            ["poetry", "run", "mtf2json", "--mtf-dir", str(temp_mtf_dir)],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        assert result.returncode == 0, f"Process failed with return code {result.returncode}"
        # check JSON files
        for mtf_file in temp_mtf_dir.glob("*.mtf"):
            json_file = mtf_file.with_suffix('.json')
            assert json_file.exists(), f"JSON file {json_file} was not created"
            try:
                with open(json_file, 'r') as f:
                    json_data = json.load(f)
            except json.JSONDecodeError as e:
                assert False, f"Output file {json_file} is not valid JSON: {e}"
            assert isinstance(json_data, dict), f"Output JSON in {json_file} is not a dictionary"


def test_convert_directory_recursive() -> None:
    """
    Similar to `test_convert_directory`, but creates a temporary directory with subdirectories,
    places at least 1 MTF file in each subdirectory and uses the `--recursive` flag.
    """
    # only use MTF files for biped mechs
    mtf_dir = Path("tests/mtf/biped")
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_mtf_dir = Path(tmpdir) / "mtf"
        temp_mtf_dir.mkdir(parents=True, exist_ok=True)
        subdirs = ["a", "b"]
        for subdir in subdirs:
            (temp_mtf_dir / subdir).mkdir(parents=True, exist_ok=True)
            # copy the same files into all subdirs (no problem for this testcase)
            for mtf_file in mtf_dir.glob("*.mtf"):
                temp_mtf_file = temp_mtf_dir / subdir / mtf_file.name
                shutil.copy(mtf_file, temp_mtf_file)

        result = subprocess.run(
            ["poetry", "run", "mtf2json", "--mtf-dir", str(temp_mtf_dir), "--recursive"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        assert result.returncode == 0, f"Process failed with return code {result.returncode}"
        # check JSON files
        for subdir in subdirs:
            temp_mtf_subdir = temp_mtf_dir / subdir
            for mtf_file in temp_mtf_subdir.glob("*.mtf"):
                json_file = mtf_file.with_suffix('.json')
                assert json_file.exists(), f"JSON file {json_file} was not created"
                try:
                    with open(json_file, 'r') as f:
                        json_data = json.load(f)
                except json.JSONDecodeError as e:
                    assert False, f"Output file {json_file} is not valid JSON: {e}"
                assert isinstance(json_data, dict), f"Output JSON in {json_file} is not a dictionary"


def test_convert_directory_recursive_to_json_dir() -> None:
    """
    Similar to `test_convert_directory_recursive`, but specifies `--json-dir`.
    """
    mtf_dir = Path("tests/mtf/biped")
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_mtf_dir = Path(tmpdir) / "mtf"
        temp_json_dir = Path(tmpdir) / "json"
        temp_mtf_dir.mkdir(parents=True, exist_ok=True)
        temp_json_dir.mkdir(parents=True, exist_ok=True)
        subdirs = ["a", "b"]
        for subdir in subdirs:
            (temp_mtf_dir / subdir).mkdir(parents=True, exist_ok=True)
            for mtf_file in mtf_dir.glob("*.mtf"):
                temp_mtf_file = temp_mtf_dir / subdir / mtf_file.name
                shutil.copy(mtf_file, temp_mtf_file)

        result = subprocess.run(
            ["poetry", "run", "mtf2json", "--mtf-dir", str(temp_mtf_dir), "--json-dir", str(temp_json_dir), "--recursive"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        assert result.returncode == 0, f"Process failed with return code {result.returncode}"
        for subdir in subdirs:
            temp_json_subdir = temp_json_dir / subdir
            assert temp_json_subdir.is_dir(), f"Subdirectory {temp_json_subdir} was not created"
            for mtf_file in (temp_mtf_dir / subdir).glob("*.mtf"):
                json_file = temp_json_subdir / mtf_file.with_suffix('.json').name
                assert json_file.exists(), f"JSON file {json_file} was not created"
                try:
                    with open(json_file, 'r') as f:
                        json_data = json.load(f)
                except json.JSONDecodeError as e:
                    assert False, f"Output file {json_file} is not valid JSON: {e}"
                assert isinstance(json_data, dict), f"Output JSON in {json_file} is not a dictionary"
