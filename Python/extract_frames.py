#!/usr/bin/env -S python3 -u
import argparse
import re
from pathlib import Path

import cv2


def parse_time(time_spec, fps):
    pattern = re.compile(r"(\d+h)?(\d+m)?(\d+s)?")
    match = pattern.match(time_spec)
    if match is None or match.group(0) == "":
        return -1
    hour = match.group(1)
    minute = match.group(2)
    second = match.group(3)
    frame_cnt = 0.0
    if hour:
        frame_cnt += fps * 3600 * float(hour.replace("h", ""))
    if minute:
        frame_cnt += fps * 60 * float(minute.replace("m", ""))
    if second:
        frame_cnt += fps * float(second.replace("s", ""))
    return int(frame_cnt)


def extract_frames(
    video_name, frame_indices=None, out_dir="frames", start_time=None, end_time=None
):
    video = cv2.VideoCapture(video_name)
    print("reading frames")
    frames = [video.read()[1] for _ in range(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))]
    print("reading frames done")
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    if frame_indices is None:
        start_frame_idx = 0
        end_frame_idx = len(frames)
        if start_time:
            start_frame_idx = parse_time(start_time, fps)
        if start_frame_idx < 0:
            print(f"invalid start time spec: {start_time}")
            return 1
        if end_time:
            end_frame_idx = parse_time(end_time, fps)
        if end_frame_idx < 0:
            print(f"invalid end time spec: {end_time}")
            return 1
        frame_indices = [i for i in range(start_frame_idx, end_frame_idx)]
    out_path = Path(out_dir)
    out_path.mkdir(exist_ok=True, parents=True)
    for idx in frame_indices:
        if idx >= len(frames):
            print(f"invalid frame index detected, skipped: {idx}")
            continue
        img_path = out_path / f"{idx:04d}.png"
        if cv2.imwrite(str(img_path), frames[idx]):
            print(f"image saved: {img_path}")
        else:
            print(f"fail to save image: {img_path}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_name", help="the input video file", metavar="VIDEO")
    parser.add_argument(
        "--frame-indices",
        "-i",
        type=lambda arg_str: map(int, arg_str.strip().split(",")),
        metavar="IDX[,IDX,...]",
        default=None,
        help="the frame indices to save",
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        metavar="DIR",
        help="the output directory of extracted frames (default: %(default)s)",
        default="frames",
    )
    parser.add_argument("--start-time", help="the start time")
    parser.add_argument("--end-time", help="the end time")
    kwargs = vars(parser.parse_args())
    extract_frames(**kwargs)
