
# !/usr/bin/env python3

import queue
import sys

from microphone.microphone_init import init_recognizer
from microphone.microphone_loop import recording_loop


def main():
    '''This script processes audio input from the microphone and displays the transcribed text.'''
    recognizer = init_recognizer()
    # setup queue and callback function
    q = queue.Queue()
    browser_path = get_argument(sys.argv, 0, "/snap/bin/chromium")
    recording_loop(q, recognizer, browser_path)

def get_argument(argv: list[str], index: int,  default_value: str) -> str:
    if len(argv) > index + 1:
        return argv[index + 1]
    else:
        return default_value


if __name__ == "__main__":
    main()