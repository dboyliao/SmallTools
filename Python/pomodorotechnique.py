#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep
import sys
import subprocess as sp
import argparse

class _Talker(object):

    def __init__(self):

        if sys.platform == "darwin":
            self._cmd = sp.check_output(["which", "say"]).strip()
        else:
            raise NotImplementedError("Unsupport platform: ".format(sys.platform))

    def say(self, msg, options):
        sp.call([self._cmd] + list(options) + [msg])

def main(num_cycles = 4, minutes = 25, break_time = 5, talker_options = ""):

    try:
        talker = _Talker()
    except NotImplementedError as e:
        print(e)
        sys.exit(1)

    options = talker_options.split(" ")
    cycle_seconds = int(minutes * 60)
    break_seconds = int(break_time * 60)

    talker.say("start clock", options)
    while num_cycles > 0:
        sleep(cycle_seconds)
        if break_seconds > 60:
            m = int(break_time)
            s = int(60*(break_time - m))
            msg = "break time {} minutes {} seconds".format(m, s)
        else:
            msg = "break time {} seconds".format(cycle_seconds)
        talker.say(msg, options)

        sleep(break_seconds)
        msg = "break time over, get back to work"
        talker.say(msg, options)
        num_cycles -= 1

    talker.say("take a long break", options)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number-cycles", dest = "num_cycles",
                        metavar = "INTEGER", type = int,
                        help = "number of cycles (default: 4)",
                        default = 4)
    parser.add_argument("-m", "--minutes-per-cycle", dest = "minutes",
                        metavar = "FLOAT", type = float,
                        help = "minutes for each cycle (default: 25)",
                        default = 25.0)
    parser.add_argument("-b", "--minutes-per-break", dest = "break_time",
                        metavar = "FLOAT", type = float,
                        help = "minutes for break after each cycle (default: 5)",
                        default = 5.0)
    parser.add_argument("-t", "--talker-options", dest = "talker_options",
                        metavar = "STRING",
                        help = "options for the talker (ex: '-v Fred' for Mac)",
                        default = "")
    args = parser.parse_args()

    main(args.num_cycles,
         args.minutes,
         args.break_time,
         args.talker_options)
