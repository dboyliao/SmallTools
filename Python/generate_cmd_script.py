#!/usr/bin/env -S python3 -u
import argparse
import sys
import re
from pathlib import Path
import os

TEMPLAE = """\
#!/usr/bin/env -S python3 -u
import argparse
import sys

def {script_name}(**kwargs):
    # enter your code here
    ...

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # setup the parser here
    kwargs = vars(parser.parse_args())
    sys.exit({script_name}(**kwargs))
"""


def generate_cmd_script(script_name):
    fname = f"{script_name}.py"
    with Path(fname).open("w", encoding="utf8") as fid:
        fid.write(TEMPLAE.format(script_name=script_name))
    os.chmod(fname, 0o744)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "script_name",
        type=lambda name: re.sub(r"[-\.]", "_", name),
        help="the script name",
        metavar="NAME",
    )
    kwargs = vars(parser.parse_args())
    sys.exit(generate_cmd_script(**kwargs))
