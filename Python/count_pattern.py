#!/usr/bin/env python
# Simple counting program
from __future__ import print_function
import re
import argparse

def count_pattern(fname, pattern, verbose = False):
    count = 0
    pattern = re.compile(pattern)
    with open(fname) as rf:
        l = rf.readline()
        while not l == "":
            match = pattern.findall(l)
            if verbose:
                print(match)
            count += len(match)
            l = rf.readline()
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "count the number of matched pattern in the file.")
    parser.add_argument("fname", metavar = "FILE", help = "file name")
    parser.add_argument("-e", "--pattern", metavar = "PATTERN", default = "[^\s]",
                        help = "regular expression pattern", dest = "pattern")
    parser.add_argument("-v", "--verbose", action = "store_true",
                        help = "run in verbose mode", dest = "verbose")
    args = parser.parse_args()
    count = count_pattern(args.fname, args.pattern, args.verbose)
    print(count)

