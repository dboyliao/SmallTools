#!/usr/bin/env -S python3 -u
import argparse
import sys
from pathlib import Path


def copy_file(files, in_place=False):
    for file in files:
        print(f"copy {file}")
        file_path = Path(file)
        with file_path.open("rb") as fid:
            bin_content = fid.read()
        if in_place:
            out_fname = file_path.name
        else:
            out_fname = f"copied_{file_path.name}"
        to_path = file_path.parent / out_fname
        if in_place and to_path.exists():
            to_path.unlink()
        with to_path.open("wb") as fid:
            fid.write(bin_content)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # setup the parser here
    parser.add_argument("files", metavar="FILE", help="the file to copy", nargs="+")
    parser.add_argument(
        "--in-place", action="store_true", help="copy the file IN PLACE"
    )
    kwargs = vars(parser.parse_args())
    sys.exit(copy_file(**kwargs))
