
# !/usr/bin/env python3

import queue
import subprocess
from typing import Optional

from playwright.sync_api import sync_playwright

import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json

'''This script processes audio input from the microphone and displays the transcribed text.'''

# list all audio devices known to your system
print("Display input/output devices")
devices = sd.query_devices()
print(devices)

sd.default.device= "Blue Snowball"
# get the samplerate - this is needed by the Kaldi recognizer
device_info = sd.query_devices(sd.default.device, 'input')
samplerate = int(device_info['default_samplerate'])

# display the default input device
print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], device_info))

# setup queue and callback function
q = queue.Queue()


def recordCallback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


# build the model and recognizer objects.
print("===> Build the model and recognizer objects.  This will take a few minutes.")
MODEL_PATH = "vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, samplerate)
recognizer.SetWords(False)

print("===> Begin recording. Press Ctrl+C to stop the recording ")

def open_browser(web_pages: list[str]):
    web_page_name = web_pages[0]
    web_page_url = extract_web_page(web_page_name)
    if web_page_url is not None:
        with sync_playwright() as p:
            print(f"open {web_page_url}")
            browser = p.firefox.launch(headless=False)
            print(f"browser {browser}")
            page = browser.new_page()
            print(f"page {page}")
            page.goto(web_page_url)
            page.wait_for_timeout(100000)
            #browser.close()
    else:
        print(f"web page not recognized: {web_page_name}")


def extract_web_page(web_page: str) -> Optional[str]:
    match web_page:
        case "repubblica" | "republican":
            return "https://www.repubblica.it"
        case "netflix":
            return "https://www.netflix.com"
        case _:
            return None


def in_netflix(action: list[str]):
    pass


def do_something(command_words: list[str]):
    if len(command_words) > 0:
        match command_words[0]:
            case "browser":
                open_browser(command_words[1:])
            case "netflix":
                in_netflix(command_words[1:])
            case _:
                print(f"Command {command_words} not recognized")
    else:
        print("No command to run")


def do_something_if_requested(words: list[str]):
    words = [w for w in words if w not in   ["a", "and", "but"]]
    if len(words) > 0:
        first_word = words[0]
        if first_word == "max"  and len(words) >= 2:
            do_something(words[1:])
        elif first_word == "hi" and len(words) >= 3:
            do_something_if_requested(words[1:])
        else:
            print("Not a command")
    else:
        print("Nothing to do")


try:
    with sd.RawInputStream(dtype='int16', callback=recordCallback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result_text = recognizer.Result()
                # convert the recognizerResult string into a dictionary
                result_dict = json.loads(result_text)
                text = result_dict.get("text", "")
                if text != "":
                    print(f"Text from microphone: {text}")
                    do_something_if_requested(text.split(" "))
                else:
                    print("no input sound")

except KeyboardInterrupt:
    print('===> Finished Recording')
except Exception as e:
    print(str(e))