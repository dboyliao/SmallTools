#!/usr/bin/env python3
import datetime as dt
import argparse
from pathlib import Path
import sys
import os
import subprocess
from shutil import copyfile, rmtree, copy


_LOG_DIR = "~/.pyscript_run"


def clear(py_script: str):
    print(f"clear log for {py_script}")
    log_path = Path(_LOG_DIR) / py_script
    if log_path.exists():
        rmtree(str(log_path))
    return 0


def pyscript_run(py_script, script_args, copy_dir=False):
    run_time = dt.datetime.now().isoformat(timespec="seconds").replace(":", "-")
    script_name, ext = os.path.splitext(py_script)
    if ext != ".py":
        print(f"expecting a python script, get {py_script}")
        return 1
    log_dir = (Path(_LOG_DIR) / script_name / run_time).expanduser()
    log_dir.mkdir(parents=True, exist_ok=True)
    with (log_dir / py_script).open("w") as fid, open(py_script) as ori_fid:
        content = ori_fid.read()
        fid.write(content)
    complete_proc = subprocess.run(
        [sys.executable, py_script] + script_args,
        capture_output=True,
    )
    if complete_proc.stdout:
        print(complete_proc.stdout.decode("utf8"), file=sys.stdout, end="")
    if complete_proc.stderr:
        print(complete_proc.stderr.decode("utf8"), file=sys.stderr, end="")
    with (log_dir / "command.txt").open("w") as fid:
        fid.write(" ".join([py_script] + script_args) + "\n")
    with (log_dir / "log.txt").open("w") as fid:
        if complete_proc.stdout:
            fid.write(complete_proc.stdout.decode("utf8"))
        if complete_proc.stderr:
            fid.write(complete_proc.stderr.decode("utf8"))
    for script_arg in script_args:
        arg_path = Path(script_arg).expanduser()
        if arg_path.is_file():
            copyfile(str(arg_path), str(log_dir / arg_path.name))
        elif arg_path.is_dir() and copy_dir:
            copy(str(arg_path), str(log_dir / arg_path.name))
    return complete_proc.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("py_script", help="the python script to run")
    parser.add_argument(
        "--clear", help="clear running log of given python script", action="store_true"
    )
    parser.add_argument(
        "--copy-dir",
        action="store_true",
        help="if to copy directory given in the script aruguments",
    )
    args, script_args = parser.parse_known_args()
    if args.clear:
        sys.exit(clear(args.py_script))
    else:
        sys.exit(pyscript_run(args.py_script, script_args, copy_dir=args.copy_dir))
