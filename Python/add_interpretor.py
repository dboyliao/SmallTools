#!/usr/bin/env python3

"""
This small tool will automatic add proper '#!' line
at the begining of your scripts.
"""

import os
import argparse

_supported_interpretor = {
        "swift_xc": ("#!/usr/bin/env xcrun swift\n", ".swift"),
        "swift": ("#!/usr/bin/env swift\n", ".swift"),
        "pytohn": ("#!/usr/bin/env python\n", ".py"),
        "python2": ("#!/usr/bin/env python2\n", ".py"),
        "python3": ("#!/usr/bin/env python3\n", ".py"),
        "bash": ("#!/usr/bin/env bash", ".sh"),
        "sh": ("#!/usr/bin/env sh", ".sh")
        }


def main(args):
    """
    main program
    """
    # parsing arguments
    interpretor, target_ext = _supported_interpretor[args.interpretor]
    where = args.where
    overwrite = args.overwrite

    # walk through the directory tree.
    for current_dir, dirs, fnames in os.walk(where):
        for fname in fnames:
            _, ext = os.path.splitext(fname)
            if ext == target_ext:
                fpath = os.path.join(current_dir, fname)
                with open(fpath, "r") as rf:
                    # Read contents.
                    lines = rf.readlines()
                    try:
                        first_line = lines[0]
                    except IndexError:
                        # Empty file. Skip.
                        continue

                # Skip if there is already one which we desire.
                if first_line == interpretor:
                    continue
                elif first_line.startswith("#!"):
                    # Found existing interpretor. Overwrite it or not.
                    if not overwrite:
                        print("[Warning] Detecting other interpretor in file: {}".format(fpath))
                        print("Skipping.")
                        continue
                    lines = lines[1:]

                with open(fpath, "w") as wf:
                    content = "".join(lines)
                    wf.seek(0)
                    wf.write(interpretor)
                    wf.write(content)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="add_interpretor")
    parser.add_argument("-i", "--interpretor",
                        dest="interpretor", help="interpretor to be used. ex: python",
                        metavar="INTERPRETOR",
                        required=True)
    parser.add_argument("-w", "--where",
                        dest="where", help="where to find the files.",
                        metavar="PATH",
                        required=True)
    parser.add_argument("-o", "--overwrite",
                        dest="overwrite", help="overwrite interpretor if there is any.",
                        action="store_true")

    args = parser.parse_args()
    main(args)
