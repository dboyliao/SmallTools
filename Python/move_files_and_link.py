#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from shutil import move


def move_files_and_link(files, to: Path):
    to.mkdir(parents=True, exist_ok=True)
    for file_path in map(Path, files):
        if not file_path.is_file():
            print(f"skipping {file_path} for not being a file")
            continue
        new_path = to / file_path.name
        move(str(file_path), str(new_path))
        os.symlink(str(new_path), str(file_path))
        print(f"creating symlink for {file_path} and move it to {new_path}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="files to move")
    parser.add_argument(
        "--to", "-t", type=Path, help="move to directory", required=True
    )
    kwargs = vars(parser.parse_args())
    sys.exit(move_files_and_link(**kwargs))
