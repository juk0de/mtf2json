#! /bin/env python3
import sys
import json
import argparse
from pathlib import Path
import os
from .mtf2json import read_mtf, write_json, ConversionError, version, mm_commit
from typing import Optional, List, Tuple


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
    parser.add_argument('--mm-commit', '-C',
                        action='store_true',
                        help="Print latest supported MegaMek commit")
    parser.add_argument('--mtf-dir', '-M',
                        type=str,
                        help="Convert all MTF files in the given directory.",
                        metavar="MTF_DIR")
    parser.add_argument('--json-dir', '-J',
                        type=str,
                        help="Store all JSON files in the given directory.",
                        metavar="JSON_DIR")
    parser.add_argument('--recursive', '-r',
                        action='store_true',
                        help="Recursively convert MTF files in subdirectories.")
    parser.add_argument('--ignore-errors', '-i',
                        action='store_true',
                        help="Ignore errors during conversion (continue with next file). Print statistics afterwards.")
    return parser


def convert_dir(mtf_dir: Path,
                json_dir: Optional[Path] = None,
                recursive: bool = True,
                ignore_errors: bool = False) -> int:
    """
    Convert all MTF files in the `mtf_dir` folder to JSON (and subfolders if `recursive` is True).
    The JSON files have the same name but suffix '.json' instead of '.mtf'.
    If `json_dir` is given, write the JSON file to that directory.
    If 'ignore_errors' is True, continue with the next file in case of an exception.
    """
    if not mtf_dir.is_dir():
        raise ValueError(f"'{mtf_dir}' is not a directory.")

    if json_dir:
        if not json_dir.exists():
            json_dir.mkdir(parents=True, exist_ok=True)
        elif not json_dir.is_dir():
            raise ValueError(f"'{json_dir}' is not a directory.")

    num_files = num_success = 0
    error_files: List[Tuple[str, str]] = []
    error_occured = False
    for root, _, files in os.walk(mtf_dir):
        files.sort()
        for file in files:
            if file.endswith('.mtf'):
                num_files += 1
                mtf_path = Path(root) / file
                if json_dir:
                    relative_path = mtf_path.relative_to(mtf_dir)
                    json_path = json_dir / relative_path.with_suffix('.json')
                    json_path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    json_path = mtf_path.with_suffix('.json')
                try:
                    print(f"'{mtf_path}' -> '{json_path}' ...  ", end='')
                    data = read_mtf(mtf_path)
                    write_json(data, json_path)
                    num_success += 1
                    print("SUCCESS")
                except Exception as ex:
                    error_occured = True
                    error_files.append((str(mtf_path), str(ex)))
                    print(f"ERROR: {ex}")
                    if not ignore_errors:
                        return 1
        if not recursive:
            break
    if ignore_errors:
        # print statistics
        print(f"> Converted {num_success} of {num_files} files.")
        if len(error_files) > 0:
            print("> Failed to convert:")
            for f, e in error_files:
                print(f"  {f} ({e})")
    return 1 if error_occured else 0


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    # print version
    if args.version:
        print(f"{version}")
        sys.exit(0)
    if args.mm_commit:
        print(f"{mm_commit}")
        sys.exit(0)

    # either file conversion or directory conversion is allowed, but not both simultaneously
    if (args.mtf_file and args.mtf_dir) or (args.json_file and args.json_dir):
        print("\nError: Specify either --mtf-file or --mtf-dir, and either --json-file or --json-dir, but not both.")
        parser.print_help()
        sys.exit(1)
    # either --mtf-file or --mtf-dir is required
    if not args.mtf_file and not args.mtf_dir:
        print("\nError: Either --mtf-file or --mtf-dir must be specified.")
        parser.print_help()
        sys.exit(1)
    #  nr. of arguments for --mtf-file and --json-file must match
    if args.json_file and len(args.mtf_file) != len(args.json_file):
        print("\nError: The number of JSON files must match the number of MTF files.")
        parser.print_help()
        sys.exit(1)
    # set convert to True if --json-file or --json-dir are specified (or multiple MTF files)
    if args.json_file or args.json_dir or (args.mtf_file and len(args.mtf_file) > 1):
        args.convert = True

    # convert given MTF file(s)
    if args.mtf_file:
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

    # convert all MTF files in given directory
    if args.mtf_dir:
        mtf_dir = Path(args.mtf_dir)
        json_dir = Path(args.json_dir) if args.json_dir else None
        sys.exit(convert_dir(mtf_dir, json_dir, args.recursive, args.ignore_errors))


if __name__ == "__main__":
    main()
