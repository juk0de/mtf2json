#! /bin/env python3
import sys
import json
import argparse
from pathlib import Path
import os
from .mtf2json import read_mtf, write_json, ConversionError, version, mm_version
from typing import Optional


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
            description="Convert MegaMek MTF files to JSON.")
    # options
    parser.add_argument('--mtf-file', '-m',
                        type=str,
                        nargs='+',
                        help="The MTF file(s) to convert.",
                        metavar="MTF_FILE")
    parser.add_argument('--convert', '-c',
                        action='store_true',
                        help="Convert the MTF file to a JSON file (use same filename with suffix '.json').")
    parser.add_argument('--json-file', '-j',
                        type=str,
                        nargs='+',
                        help="The destination file(s) for JSON conversion (instead of default filename).",
                        metavar="JSON_FILE")
    parser.add_argument('--version', '-V',
                        action='store_true',
                        help="Print version")
    return parser


def convert_dir(mtf_dir: Path,
                json_dir: Optional[Path] = None,
                recursive: bool = True,
                ignore_errors: bool = False) -> None:
    """
    Convert all MTF files in the `mtf_dir` folder to JSON (and subfolders if `recursive` is True).
    The JSON files have the same name but suffix '.json' instead of '.mtf'.
    If `json_dir` is given, write the JSON file to that directory.
    If 'ignore_errors' is True, continue with the next file in case of a ConversionError.
    """
    if not mtf_dir.is_dir():
        raise ValueError(f"'{mtf_dir}' is not a directory.")

    if json_dir:
        if not json_dir.exists():
            json_dir.mkdir(parents=True, exist_ok=True)
        elif not json_dir.is_dir():
            raise ValueError(f"'{json_dir}' is not a directory.")

    for root, _, files in os.walk(mtf_dir):
        for file in files:
            if file.endswith('.mtf'):
                mtf_path = Path(root) / file
                if json_dir:
                    relative_path = mtf_path.relative_to(mtf_dir)
                    json_path = json_dir / relative_path.with_suffix('.json')
                    json_path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    json_path = mtf_path.with_suffix('.json')
                try:
                    data = read_mtf(mtf_path)
                    write_json(data, json_path)
                    print(f"Successfully converted '{mtf_path}' to '{json_path}'.")
                except ConversionError as e:
                    if ignore_errors:
                        print(f"Failed to convert '{mtf_path}': {e}")
                    else:
                        raise e
        if not recursive:
            break


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    # print version
    if args.version:
        print(f"{version} (MM: {mm_version})")
        sys.exit(0)

    # check params
    if not args.mtf_file or (args.json_file and len(args.mtf_file) != len(args.json_file)):
        if args.json_file and len(args.mtf_file) != len(args.json_file):
            print("\nError: The number of JSON files must match the number of MTF files.")
        parser.print_help()
        sys.exit(1)

    # set convert to True if json_file is specified
    if args.json_file:
        args.convert = True

    # read MTF
    for i, mtf_file in enumerate(args.mtf_file):
        path = Path(mtf_file)
        if not path.exists():
            print(f"File {path} does not exist!")
            sys.exit(1)
        try:
            data = read_mtf(path)
        except ConversionError as e:
            print(f"Failed to convert '{path}': {e}")
            sys.exit(1)

        # convert to JSON and print or write to file
        if args.convert:
            json_path = Path(args.json_file[i]) if args.json_file else path.with_suffix('.json')
            try:
                write_json(data, json_path)
                print(f"Successfully saved JSON file '{json_path}'.")
            except Exception as e:
                print(f"Error: writing '{json_path}' failed with '{e}'")
                sys.exit(1)
        else:
            print(json.dumps(data))


if __name__ == "__main__":
    main()
