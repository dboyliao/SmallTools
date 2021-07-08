#!/usr/bin/env -S python3 -u
import argparse
import os
import sys

import pyheif
from PIL import Image


def convert_heif(heif_names, to_format="png"):
    for heif_name in heif_names:
        img_name, ext = os.path.splitext(os.path.basename(heif_name))
        if ext.lower() not in [".heif", ".heic"]:
            print(f"expecting heif image file, get {heif_name}")
            return 1
        heif = pyheif.read(heif_name)
        img = Image.frombytes(
            heif.mode,  # mode
            heif.size,  # size
            heif.data,  # data
            "raw",  # decoder_name
            heif.mode,
            heif.stride,
        )
        out_fname = f"{img_name}.{to_format}"
        img.save(out_fname)
        print(f"{out_fname} saved")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--to-format", dest="to_format", default="png", help="the output image format"
    )
    parser.add_argument(
        "heif_names", metavar="IMAGE.heif", nargs="+", help="the input heif image"
    )
    kwargs = vars(parser.parse_args())
    sys.exit(convert_heif(**kwargs))