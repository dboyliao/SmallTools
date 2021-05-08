#!/usr/bin/env python3
import subprocess
import sys
import datetime as dt
from pathlib import Path


def _print_usage():
    print("Usage:")
    print("Running command: run-it.py <command> args...")
    print("Print log: run-it.py --print-log")
    print("Clear log: run-it.py --clear")


def main(cmd, log_file):
    run_time = dt.datetime.now().isoformat("T", "seconds")
    try:
        ret_code = subprocess.call(cmd)
        print(
            f"[run-it {run_time}] running {' '.join(cmd)!r}",
            file=log_file,
        )
        return ret_code
    except Exception:
        _print_usage()
        return 1


if __name__ == "__main__":
    cmd = sys.argv[1:]
    if cmd[0] in ["-h", "--help"]:
        _print_usage()
    elif cmd[0] == "--print-log":
        try:
            with Path("~/.run-it.log").expanduser().open("r") as fid:
                print(fid.read())
        except FileNotFoundError:
            print("No log file to print")
    elif cmd[0] == "--clear":
        print("removing ~/.run-it.log")
        Path("~/.run-it.log").expanduser().unlink(missing_ok=True)
    else:
        with Path("~/.run-it.log").expanduser().open("a") as fid:
            main(cmd, fid)
