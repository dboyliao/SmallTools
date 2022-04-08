#!/usr/bin/env -S python3 -u
import argparse
import re
from pathlib import Path

import cv2
import tqdm


def imgs2mov(
    input_dir: Path, movie_name="movie", fps=20, numerical=False, flip_channels=False
):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_fname = f"{movie_name}.mov"
    img_names = []
    for ext in ["png", "jpg"]:
        img_names.extend(
            [str(p.expanduser().absolute()) for p in input_dir.glob(f"*.{ext}")]
        )
    if numerical:

        def key(fname):
            pat = re.compile(r"[0-9]+")
            return tuple(map(int, pat.findall(fname)))

    else:
        key = lambda v: v
    img_names = sorted(img_names, key=key)
    print(f"reading frames from {input_dir}")
    frames = []
    for name in tqdm.tqdm(img_names):
        frames.append(cv2.imread(name, cv2.IMREAD_COLOR))
    if flip_channels:
        if frames[0].shape[-1] == 4:
            shuffle_idxs = [2, 1, 0, 3]
        else:
            shuffle_idxs = [2, 1, 0]
        frames = [frame[:, :, shuffle_idxs] for frame in frames]
    print(f"reading frames done ({len(frames)} frames)")
    writer = cv2.VideoWriter(out_fname, fourcc, fps, frames[0].shape[:2][::-1])
    print("writing frames")
    for frame in tqdm.tqdm(frames):
        writer.write(frame)
    writer.release()
    print(f"movie saved: {out_fname} (fps: {fps})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_dir",
        help="the directory where to find input images",
        type=Path,
        default=Path("."),
    )
    parser.add_argument(
        "-o",
        "--movie-name",
        help="the output movie name (default: %(default)s)",
        default="movie",
    )
    parser.add_argument(
        "--fps",
        help="output frame per second (default: %(default)s)",
        default=20,
        type=int,
    )
    parser.add_argument(
        "-n",
        "--numerical",
        action="store_true",
        help="interpret the file name numerically, sort it accordingly",
    )
    parser.add_argument(
        "-f", "--flip-channels", help="flip B and R channel", action="store_true"
    )
    kwargs = vars(parser.parse_args())
    imgs2mov(**kwargs)
