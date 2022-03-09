#!/usr/bin/env python3
import argparse
from subprocess import call as _call


def cmake_find_package(
    package_name, language="CXX", mode="EXIST", compiler_id="GNU", print_cmake_cmd=False
):
    cmd = [
        "cmake",
        f"-DNAME={package_name}",
        f"-DLANGUAGE={language}",
        f"-DMODE={mode}",
        f"-DCOMPILER_ID={compiler_id}",
        "--find-package",
    ]
    if print_cmake_cmd:
        print("Running CMake command:", " ".join(cmd))
        print()
    return _call(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("package_name", help="the package name")
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