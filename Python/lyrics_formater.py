#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

def combine_two(fname1, fname2 = None, max_line_length = 75):

    if fname2 is None:
        with open(fname1) as rf:
            content = rf.read()

        return content

    content = ""
    line_format = "{0:<" + str(max_line_length) + "}{1}"
    with open(fname1) as rf1:
        with open(fname2) as rf2:
            line1 = rf1.readline()
            line2 = rf2.readline()
            while len(line1) > 0 or len(line2) > 0:
                if len(line2) > 0:
                    line1 = line1.strip()
                else:
                    line2 = "\n"
                content += line_format.format(line1, line2)
                line1 = rf1.readline().strip()
                line2 = rf2.readline()

    return content

def main(files, max_line_length):

    if not len(files) % 2 == 0:
        files.append(None)

    with open("lyrics.txt", "w") as wf:
        for i in range(len(files)/2):
            file1 = files[2*i]
            file2 = files[2*i+1]
            content = combine_two(file1, file2, max_line_length)
            wf.write(content)
            wf.write("\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar = "TXT_FILE", nargs = "+",
                        help = "lyrics files to be aligned")
    parser.add_argument("-l", "--max-line-length", default = 75, dest = "line_length", metavar = "INTEGER",
                        help = "maximum line length (default: 75)")
    args = parser.parse_args()

    main(args.files, args.line_length)
