#!/usr/bin/python
# -*- encode: utf-8 -*-

from __future__ import print_function
import sys, os
import shutil

def copy_file(src, dest, file_surfixs = ["jpg", "png"]):
    count = 0
    for rel_path, dirs, files in os.walk(src):
        for file_name in files:
            if sum(map(file_name.endswith, file_surfixs)) > 0:
                count += 1
                shutil.copy2(os.path.abspath(os.path.join(rel_path, file_name)), os.path.join(dest, file_name))
    print("Total number of files copied: {count}".format(count = count), file = sys.stdout)

if __name__ == "__main__":

    import argparse

    desc = "Walk throuhg `src` to find all files with surfix in `surfixs` and copy it to `dest`"

    epilog = "Example: find_files -f ~ -t ~/temp -s txt c cpp md"
    parser = argparse.ArgumentParser(description=desc, epilog = epilog)
    parser.add_argument("-f", dest='from_dir', metavar = 'from',
                         required = True,
                         help= "source directory")
    parser.add_argument("-t", dest='dest_dir', metavar = 'to',
                         required = True,
                         help = "destination directory")
    parser.add_argument("-s", '--surfixs', dest = "surfixs",
                        action = "store",
                        nargs = '*',
                        default = ['jpg', 'gif', 'png', 'jpeg'],
                        metavar = 'surfixs', help = "file surfixs to match. Default are 'jpg', 'gif', 'png' and 'jepg'.")
    try:
        args = parser.parse_args()
        print("Begin process....")
        copy_file(args.from_dir, args.dest_dir, file_surfixs = args.surfixs)
    except Exception as e:
        print(e)
        print(parser.format_help())
