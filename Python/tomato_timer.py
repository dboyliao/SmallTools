#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Pomodoro_Technique
from __future__ import print_function
from time import sleep
from datetime import datetime
import sys
import subprocess as sp
import argparse

if sys.version_info.major < 3:
    input = raw_input

class _Talker(object):
    """
    _Talker: object responsible for playing voice message.

    Support Platform
    ================
    - MacOS: via 'say'.
    """

    def __init__(self):

        if sys.platform == "darwin":
            self._cmd = sp.check_output(["which", "say"]).strip()
        else:
            raise NotImplementedError("Unsupport platform: ".format(sys.platform))

    def say(self, msg, options):
        """
        say void messsage

        params
        ======
        - msg (str): message to say.
        - options (list or tuple): options to pass to shell command that will play the voice message.
        """
        sp.call([self._cmd] + list(options) + [msg])

def simple_log(msg, dest = sys.stdout, wait = False):
    d = datetime.now()
    log_msg = "{}: {}".format(d, msg)
    if wait:
        input(log_msg)
    else:
        print(log_msg, file = dest)

def main(num_cycles = 4, minutes = 25.0, break_time = 5.0, talker_options = ""):
    """
    main function

    params
    ======
    - num_cycles (int): number of cycles (default: 4)
    - minutes (float): time for each cycles in minutes (default: 25.0)
    - break_time (float): time for break after each cycle in minutes (default: 5.0)
    - talker_options (str): option string to pass to the voice message player (ex: '-v Fred' on MacOS)
    """
    # try to initiate a talker.
    try:
        talker = _Talker()
    except NotImplementedError as e:
        simple_log(e, dest = sys.stderr)
        sys.exit(1)

    options = talker_options.split(" ")
    cycle_seconds = int(minutes * 60)
    break_seconds = int(break_time * 60)

    # start clock
    talker.say("start clock", options)
    simple_log("start clock")
    while num_cycles > 0:

        # wait for one cycle
        sleep(cycle_seconds)

        # take a inter-cycle break
        ## setup break message
        if break_seconds > 60:
            m = int(break_time)
            s = int(60*(break_time - m))
            msg = "break time {} minutes {} seconds".format(m, s)
        else:
            msg = "break time {} seconds".format(cycle_seconds)

        ## playing inter-cycle break start message (except for the last cycle)
        if num_cycles > 1:
            talker.say(msg, options)
            simple_log("{} (press return/enter to continue the clock)".format(msg), wait = True)
            simple_log("timer continue")

            ## wait for inter-cycle break
            sleep(break_seconds)

            ## playing inter-cycle break over message (except for the last cycle)
            msg = "break time over, get back to work"
            talker.say(msg, options)
            simple_log("{} (press return/enter to continue the clock)".format(msg), wait = True)
            simple_log("timer continue")

        num_cycles -= 1 # count down.

    # all cycles done. Taking long break.
    msg = "take a long break"
    talker.say(msg, options)
    simple_log(msg, wait = True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "simple tomato timer: https://en.wikipedia.org/wiki/Pomodoro_Technique")
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
                        help = "options for the talker (ex: -t '-v Fred' for Mac)",
                        default = "")
    args = parser.parse_args()

    main(args.num_cycles,
         args.minutes,
         args.break_time,
         args.talker_options)
