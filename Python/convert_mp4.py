#!/usr/bin/env -S python3 -u
import argparse
import os
import sys
from math import ceil
from time import time

import cv2


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
    num_digits = len(str(num_frames))
    fmt_str = f"[{{i:0{num_digits}d}}/{{num_frames}} {{percent:0.2f}}%] {{it_per_sec:0.2f}} it/s, eta {{eta:0.2f}} seconds"
    time_start = time()
    log_period = int(ceil(num_frames / 10))
    for i in range(1, num_frames + 1):
        ret, frame = in_cap.read()
        if not ret:
            break
        writer.write(frame)
        if i % log_period == 0:
            time_end = time()
            total_time = time_end - time_start
            time_start = time_end
            it_per_sec = total_time / log_period
            eta = (num_frames - i) * it_per_sec
            print(
                fmt_str.format(
                    i=i,
                    num_frames=num_frames,
                    percent=i * 100 / num_frames,
                    it_per_sec=it_per_sec,
                    eta=eta,
                )
            )
    print(
        fmt_str.format(
            i=num_frames,
            num_frames=num_frames,
            percent=100.0,
            it_per_sec=it_per_sec,
            eta=0.0,
        )
    )
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
