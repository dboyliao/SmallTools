#!/usr/bin/env python3
import datetime as dt
import argparse
from pathlib import Path
import sys
import os
import subprocess
from shutil import copyfile


def pyscript_run(py_script, script_args):
    run_time = dt.datetime.now().isoformat(timespec="seconds").replace(":", "-")
    script_name, ext = os.path.splitext(py_script)
    if ext != ".py":
        print(f"expecting a python script, get {py_script}")
        return 1
    log_dir = (Path("~") / ".pyscript_run" / script_name / run_time).expanduser()
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
        try:
            file_path = Path(script_arg).expanduser()
            if not file_path.is_file():
                continue
            copyfile(str(file_path), str(log_dir / file_path.name))
        except Exception:
            ...
    return complete_proc.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("py_script", help="the python script to run")
    args, script_args = parser.parse_known_args()
    sys.exit(pyscript_run(args.py_script, script_args))
