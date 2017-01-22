#!/usr/bin/env python
from __future__ import print_function
import argparse
import os

def is_executable(path):
    return os.access(path, os.X_OK) and not os.path.isdir(path)

def remove_file(path, run_dry = False, verbose = False):
    if is_executable(path):
        if verbose:
            print("Removing {}".format(path))
        if not run_dry:
            os.remove(path)

def main(root_path, run_dry = False, recursive = False, verbose = False):
    if recursive:
        for current_dir, dirs, files in os.walk(root_path):
            for path in map(lambda s: os.path.join(current_dir, s), files):
                remove_file(path, run_dry, verbose)
    else:
        for fname in os.listdir(root_path):
            remove_file(fname, run_dry, verbose)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("root_path", metavar = "ROOT_DIR",
                        help = "root directory where to start with.")
    parser.add_argument("-r", "--recursive", dest = "recursive",
                        help = "remove executable recursively (default: false)",
                        action = "store_true")
    parser.add_argument("-v", "--verbose", dest = "verbose",
                        help = "run in verbose mode.",
                        action = "store_true")
    parser.add_argument("-n", "--dry-run", dest = "run_dry",
                        help = "dry run mode",
                        action = "store_true")
    args = parser.parse_args()

    main(args.root_path, args.run_dry, args.recursive, args.verbose)
