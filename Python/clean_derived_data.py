#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import subprocess
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", dest = "root", default = ".", metavar = "PATH",
                    help = "root directory to start with. (default:.)")
parser.add_argument("-n", "--dry", dest = "dry",
                    help = "running in dry mode.(Print out message only)",
                    action = "store_true")

def main(args):
    root_dir = args.root
    dry = args.dry
    for current_dir, dirnames, filenames in os.walk(root_dir):
        if "DerivedData" in current_dir:
            if dry:
                print "would remove {}".format(current_dir)
            else:
                subprocess.call("rm -rf {}".format(current_dir), shell = True)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
