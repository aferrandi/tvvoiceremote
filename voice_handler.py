
# !/usr/bin/env python3

import queue
import sys
from dataclasses import dataclass

from config_reader import Config, read_config
from microphone.microphone_init import init_recognizer
from microphone.microphone_loop import recording_loop

@dataclass(frozen=True)

def main():
    config = read_config()
    '''This script processes audio input from the microphone and displays the transcribed text.'''
    recognizer = init_recognizer()
    # setup queue and callback function
    q = queue.Queue()
    recording_loop(q, recognizer, config)



if __name__ == "__main__":
    main()