import re
import os
from shutil import which
from subprocess import PIPE, Popen, run
from typing import Optional
import shlex

# Module to determine the length of video.
# The length is found by the FFmpeg, the output of video_duration is in seconds.


def video_duration(video_path: str, ffmpeg_path: Optional[str] = None) -> float:
    """
    Retrieve the exact video duration as echoed by the FFmpeg and return
    the duration in seconds. Maximum duration supported is 999 hours, above
    which the regex is doomed to fail(no match).

    :param video_path: Absolute path of the video file.

    :param ffmpeg_path: Path of the FFmpeg software if not in path.

    :return: Video length(duration) in seconds.

    :rtype: float
    """

    if not ffmpeg_path:
        ffmpeg_path = str(which("ffmpeg"))

    command = [
        ffmpeg_path,
        '-i', video_path
    ]
    output = run(command, capture_output=True)

    match = re.search(
        r"Duration\:(\s\d?\d\d\:\d\d\:\d\d\.\d\d)\,",
        (output.stdout.decode(errors='ignore') + output.stderr.decode(errors='ignore')),
    )

    if match:
        duration_string = match.group(1)
        hours, minutes, seconds = duration_string.strip().split(":")
        return float(hours) * 60.00 * 60.00 + float(minutes) * 60.00 + float(seconds)
    else:
        return None