#!/usr/bin/env -S python3 -u

from pathlib import Path
import cv2
import sys
import argparse
from os import get_terminal_size
from time import sleep

sys.path[:1] = [str(Path(__file__).parent)]

from show_img_term import convert_ansci_color, to_color_str

TERM_HIGHT = get_terminal_size().lines


def clear_screen():
    print(chr(27) + "[2j")
    print("\033c")
    print("\x1bc")


def show_video_term(video_path):
    video = cv2.VideoCapture(video_path)
    if video is None:
        print(f"fail to read {video_path}")
        return 1
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    sleep_secs = 1 / fps
    print(f"number of frames: {num_frames}")
    scale = None
    try:
        for frame_idx in range(num_frames):
            ok, frame = video.read()
            if not ok:
                print(f"failure on reading frame {frame_idx}")
                break
            if frame_idx == 0:
                scale = TERM_HIGHT / frame.shape[0]
            if scale < 1:
                frame = cv2.resize(frame, None, fx=scale, fy=scale)
            ansi_img = convert_ansci_color(frame)
            print(
                "\n".join(["".join(row) for row in to_color_str(ansi_img)]),
            )
            sleep(sleep_secs)
            clear_screen()
    except KeyboardInterrupt:
        ...
    clear_screen()
    print(f"number of frames played: {frame_idx}")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path", help="the of video to show")
    kwargs = vars(parser.parse_args())
    sys.exit(show_video_term(**kwargs))