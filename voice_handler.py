
# !/usr/bin/env python3

import json
import queue
import re
import sys
from typing import Optional, Any

import sounddevice as sd
from _cffi_backend import buffer
from playwright.sync_api import sync_playwright
from vosk import Model, KaldiRecognizer




def open_browser(web_pages: list[str]):
    web_page_name = web_pages[0]
    web_page_url = extract_web_page(web_page_name)
    if web_page_url is not None:
        with sync_playwright() as p:
            print(f"open {web_page_url}")
            browser = p.chromium.launch(headless=False)
            print(f"browser {browser}")
            page = browser.new_page()
            print(f"page {page}")
            page.goto(web_page_url)
            try:
                page.wait_for_timeout(100000)
            except:
                print("Browser closed")
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


def in_netflix(action: list[str]) -> None:
    with sync_playwright() as p:
        try:
            # Connect to a running Chrome instance via CDP
            browser = p.chromium.connect("http://localhost:9222")  # Replace 9222 with the actual debugging port
            default_context = browser.contexts[0]
            page = default_context.pages[0]  # Get the first page in the context
            if "netflix" in page.url:
                title = action[0]
                regex = re.compile(f".*{title}.*", re.IGNORECASE)
                anchor = page.get_by_role('link').get_by_label(regex)
                print(f"Netflix click {anchor}")
                anchor.click()
                print(f"clicked on {title}")
            else:
                print(f"The page is not netflix but {page.title()}")
        except Exception as e:
            print(f"Executing netflix command {action} got {e}")


def do_something(command_words: list[str]) -> None:
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


def do_something_if_requested(words: list[str]) -> None:
    words = [w for w in words if w not in   ["a", "and", "but"]]
    if len(words) > 0:
        first_word = words[0]
        if first_word == "max"  and len(words) >= 2:
            do_something(words[1:])
        elif first_word == "hi" and len(words) >= 3:
            do_something_if_requested(words[1:])
        else:
            print(f"Not a command: {words}")
    else:
        print("No command, nothing to do")


def read_from_microphone(recognizer: KaldiRecognizer, data: Any) -> None:
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

def init_recognizer() -> KaldiRecognizer:
    # list all audio devices known to your system
    print("Display input/output devices")
    devices = sd.query_devices()
    print(devices)
    sd.default.device = "Blue Snowball"
    # get the samplerate - this is needed by the Kaldi recognizer
    device_info = sd.query_devices(sd.default.device, 'input')
    samplerate = int(device_info['default_samplerate'])
    # build the model and recognizer objects.
    print("===> Build the model and recognizer objects.  This will take a few minutes.")
    MODEL_PATH = "vosk-model-small-en-us-0.15"
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, samplerate)
    recognizer.SetWords(False)
    # display the default input device
    print(f"===> Initial Default Device Number:{sd.default.device[0]} Description: {device_info}")
    return recognizer

class RecordCallbackHandler:
    def __init__(self, q: queue.Queue[Any]):
        self._q = q
    def recordCallback(self, indata: buffer, frames: int, time: None, status: sd.CallbackFlags) -> None:
        if status:
            print(status, file=sys.stderr)
        self._q.put(bytes(indata))

def recording_loop(q: queue.Queue[Any], recognizer: KaldiRecognizer):
    print("===> Begin recording. Press Ctrl+C to stop the recording ")
    callback_handler = RecordCallbackHandler(q)
    try:
        with sd.RawInputStream(dtype='int16', callback=callback_handler.recordCallback):
            while True:
                data = q.get()
                read_from_microphone(recognizer, data)
    except KeyboardInterrupt:
        print('===> Finished Recording')
    except Exception as e:
        print(str(e))

def main():
    '''This script processes audio input from the microphone and displays the transcribed text.'''
    recognizer = init_recognizer()
    # setup queue and callback function
    q = queue.Queue()
    recording_loop(q, recognizer)

if __name__ == "__main__":
    main()