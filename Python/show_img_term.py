#!/usr/bin/env -S python3 -u
# https://github.com/nikhilkumarsingh/terminal-image-viewer/blob/master/img-viewer.py
from PIL import Image
import numpy as np
import argparse

from os import get_terminal_size
import sys

_term_size = get_terminal_size()
TERM_WIDTH = _term_size.columns
TERM_HEIGHT = _term_size.lines


def convert_ansci_color(img):
    if img.ndim == 3:
        if img.shape[-1] == 1:
            img = np.squeeze(img).astype(np.float64)
        elif img.shape[-1] == 4:
            # RGBA
            alpha = img[:, :, 3].reshape(img.shape[:2] + (1,))
            img = (img[:, :, :3] * (alpha / 255)).astype(np.float64)
    ansi_img = np.zeros_like(img, shape=img.shape[:2], dtype=np.uint8)
    if img.ndim == 2:
        # gray scale
        ansi_img[:] = np.round(((img - 8) / 247) * 24) + 232
        ansi_img[np.where(img < 8)] = 16
        ansi_img[np.where(img > 248)] = 231
    else:
        # color image
        ansi_img[:] = 16 + np.round(img * (5 / 255)) @ [36, 6, 1]
    return ansi_img


@np.vectorize
def to_color_str(v):
    return f"\x1b[48;5;{v}m \x1b[0m"


def show_img_term(img_paths, adjust_to_height=False):
    ret = 0
    try:
        for img_path in img_paths:
            try:
                img = Image.open(img_path)
            except FileNotFoundError:
                print(f"fail to read {img_path}")
                ret = 1
                continue
            scale = TERM_WIDTH / img.width
            if adjust_to_height:
                scale = TERM_HEIGHT / img.height
            if scale < 1:
                img = img.resize((int(scale * img.width), int(scale * img.height)))
            img = np.array(img, copy=False)
            ansi_img = convert_ansci_color(img)
            print(f"image: {img_path}")
            print(
                "\n".join(["".join(row) for row in to_color_str(ansi_img)]),
            )
            print()
    except KeyboardInterrupt:
        ...
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "img_paths", nargs="+", metavar="IMG_PATH", help="the path to the image"
    )
    parser.add_argument(
        "--adjust-to-height",
        action="store_true",
        help="adjust the image to fit the terminal height",
    )
    kwargs = vars(parser.parse_args())
    sys.exit(show_img_term(**kwargs))
