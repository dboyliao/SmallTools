#!/usr/bin/env -S python3 -u
# https://github.com/nikhilkumarsingh/terminal-image-viewer/blob/master/img-viewer.py
from black import get_gitignore
import cv2
import numpy as np
import argparse

from os import get_terminal_size
import sys

TERM_WIDTH = get_terminal_size().columns
TERM_HEIGHT = get_terminal_size().lines


def convert_ansci_color(img):
    if img.ndim == 3 and img.shape[-1] == 1:
        img = np.squeeze(img)
    assert img.dtype == np.uint8, "incorrect image data type"
    ansi_img = np.zeros_like(img, shape=img.shape[:2])
    if img.ndim < 3:
        # gray scale
        idx_under_8 = np.where(img < 8)
        idx_over_248 = np.where(img > 248)
        ansi_img[:] = np.round(((img - 8) / 247) * 24) + 232
        ansi_img[idx_under_8] = 16
        ansi_img[idx_over_248] = 231
    else:
        # color image
        img_f = img.astype(np.float64)
        b, g, r = img_f[:, :, 0], img_f[:, :, 1], img_f[:, :, 2]
        ansi_img[:] = (
            16
            + (36 * np.round(r / 255 * 5))
            + (6 * np.round(g / 255 * 5))
            + np.round(b / 255 * 5)
        ).astype(np.uint8)
    return ansi_img


@np.vectorize
def to_color_str(v):
    return f"\x1b[48;5;{v}m \x1b[0m"


def show_img_term(img_path: str, adjust_to_height=False):
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    if img is None:
        print(f"fail to read {img_path}")
        return 1
    scale = TERM_WIDTH / img.shape[1]
    if adjust_to_height:
        scale = TERM_HEIGHT / img.shape[0]
    if scale < 1:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    ansi_img = convert_ansci_color(img)
    print(
        "\n".join(["".join(row) for row in to_color_str(ansi_img)]),
    )
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", help="the path to the image")
    parser.add_argument(
        "--adjust-to-height",
        action="store_true",
        help="adjust the image to fit the terminal height",
    )
    kwargs = vars(parser.parse_args())
    sys.exit(show_img_term(**kwargs))
