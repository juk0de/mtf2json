#! /bin/env python3
import sys
import json
import argparse
from pathlib import Path
from .mtf2json import read_mtf, write_json, ConversionError, version, mm_version


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
