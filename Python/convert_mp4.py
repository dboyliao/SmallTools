#!/usr/bin/env -S python3 -u
import argparse
import os
import sys

import cv2
from tqdm import tqdm


def convert_mp4(input_video):
    in_fname, ext = os.path.splitext(input_video)
    if ext.lower() == ".mp4":
        print(f"{input_video} is already mp4 file, abort")
        return 1
    out_fname = f"{in_fname}.mp4"
    in_cap = cv2.VideoCapture(input_video)
    if not in_cap.isOpened():
        print(f"fail to open {input_video}")
        return 1
    fps = in_cap.get(cv2.CAP_PROP_FPS)
    width = int(in_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(in_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    num_frames = int(in_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if sys.platform == "darwin":
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    else:
        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    writer = cv2.VideoWriter(out_fname, fourcc, fps, (width, height))
    for _ in tqdm(range(num_frames)):
        ret, frame = in_cap.read()
        if not ret:
            break
        writer.write(frame)
    in_cap.release()
    writer.release()
    return 0


def main(input_videos):
    ok = True
    for input_video in input_videos:
        print(f"converting {input_video}")
        ok = convert_mp4(input_video) == 0 and ok
        print("\n")
    return 0 if ok else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_videos", nargs="+", help="the input video file")
    kwargs = vars(parser.parse_args())
    sys.exit(main(**kwargs))
