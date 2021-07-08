#!/usr/bin/env -S python3 -u
from PIL import Image

import argparse


def size_parser(value_str):
    if value_str is None:
        return value_str
    values = value_str.split(",")
    if len(values) > 1:
        return map(int, [v.strip() for v in values[:2]])
    else:
        return float(values[0])


def main(img_path, new_size, out_img):
    img = Image.open(img_path)
    if isinstance(new_size, float):
        new_size = tuple(map(lambda v: int(new_size * v), img.size))
    elif new_size is None:
        print(f"original image size: {img.size}")
        new_size = (
            int(input("Enter the new width: ")),
            int(input("Enter the new height: ")),
        )
    new_img = img.resize(new_size)
    new_img.save(out_img)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", metavar="IMAGE")
    parser.add_argument(
        "--to-size",
        dest="new_size",
        type=size_parser,
        metavar="SIZE",
        default=None,
        help="the target size. Can be either size seperated by comma or a float",
    )
    parser.add_argument("--out-fname", dest="out_img", default="resized_img.png")
    args = vars(parser.parse_args())
    try:
        main(**args)
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")