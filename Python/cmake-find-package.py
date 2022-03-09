#!/usr/bin/env python3
import argparse
from subprocess import run as _run
from tempfile import TemporaryDirectory


def cmake_find_package(
    package_names,
    language="CXX",
    mode="EXIST",
    compiler_id="GNU",
    print_cmake_cmd=False,
):
    ok_flags = []
    with TemporaryDirectory(prefix="cmake_find_package_") as tmp_dir:
        for name in package_names:
            cmd = [
                "cmake",
                f"-DNAME={name}",
                f"-DLANGUAGE={language}",
                f"-DMODE={mode}",
                f"-DCOMPILER_ID={compiler_id}",
                "--find-package",
            ]
            if print_cmake_cmd:
                print("Running CMake command:", " ".join(cmd))
                print()
            comp_proc = _run(cmd, cwd=tmp_dir, check=False, capture_output=True)
            print(comp_proc.stdout.decode("utf8").strip())
            ok_flags.append(comp_proc.returncode == 0)
    ret_code = 0 if all(ok_flags) else 1
    return ret_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("package_names", nargs="+", help="the package name")
    parser.add_argument("--language", default="CXX", help="the language id for CMake")
    parser.add_argument(
        "-m",
        "--mode",
        default="EXIST",
        choices=["EXIST", "COMPILE", "LINK"],
        help="the configure mode",
    )
    parser.add_argument(
        "-c", "--compiler-id", default="GNU", help="the compiler id for CMake"
    )
    parser.add_argument(
        "--print-cmake-cmd",
        action="store_true",
        help="print the CMake command if given",
    )
    kwargs = vars(parser.parse_args())
    cmake_find_package(**kwargs)