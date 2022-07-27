#!/usr/bin/env -S python3 -u
import argparse
import os
import sys
from pathlib import Path


def create_symlinks(files, to: Path):
    to.mkdir(parents=True, exist_ok=True)
    for file_path in map(Path, files):
        if not file_path.is_file():
            continue
        link_path = to / file_path.name
        os.symlink(str(file_path), str(link_path))
        print(f"creating symlink: {link_path} -> {file_path}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="files to move")
    parser.add_argument(
        "--to", "-t", type=Path, help="move to directory", required=True
    )
    kwargs = vars(parser.parse_args())
    sys.exit(create_symlinks(**kwargs))
