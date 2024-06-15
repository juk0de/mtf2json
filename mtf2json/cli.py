#! /bin/env python3
import sys
import json
import argparse
from pathlib import Path
from .mtf2json import read_mtf, write_json, ConversionError


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
            description="Convert MegaMek MTF files to JSON.")
    # options
    parser.add_argument('--mtf-file', '-m',
                        type=str,
                        help="The MTF file to print or convert.",
                        required=True,
                        metavar="MTF_FILE")
    parser.add_argument('--convert', '-c',
                        action='store_true',
                        help="Convert the MTF file to a JSON file (to same filename with suffix '.json').")
    parser.add_argument('--json-file', '-j',
                        type=str,
                        help="The destination file for JSON conversion (instead of default filename).",
                        metavar="JSON_FILE")
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    path = Path(args.mtf_file)
    if not path.exists():
        print(f"File {path} does not exist!")
        sys.exit(1)
    try:
        data = read_mtf(path)
    except ConversionError as e:
        print(f"Failed to convert '{path}': {e}")
        sys.exit(1)

    if args.convert:
        json_path = Path(args.json_file) if args.json_file else path.with_suffix('.json')
        try:
            write_json(data, json_path)
            print(f"Successfully saved JSON file '{json_path}'.")
        except Exception as e:
            print(f"Error: writing 'json_path' failed with '{e}'")
            sys.exit(1)
    else:
        print(json.dumps(data))


if __name__ == "__main__":
    main()
