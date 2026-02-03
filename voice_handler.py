
# !/usr/bin/env python3

import queue

from microphone.microphone_init import init_recognizer
from microphone.microphone_loop import recording_loop


def main():
    '''This script processes audio input from the microphone and displays the transcribed text.'''
    recognizer = init_recognizer()
    # setup queue and callback function
    q = queue.Queue()
    recording_loop(q, recognizer, "/snap/bin/chromium")

if __name__ == "__main__":
    main()