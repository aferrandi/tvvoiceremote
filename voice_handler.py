
# !/usr/bin/env python3

import json
import os
import queue
import sys
import time
import traceback
from dataclasses import dataclass
from typing import Optional, Any

import sounddevice as sd
from _cffi_backend import buffer
from playwright._impl._errors import TargetClosedError
from playwright.sync_api import sync_playwright, Page, Playwright, Locator, Browser
from thefuzz import fuzz
from vosk import Model, KaldiRecognizer


@dataclass(frozen=True)
class WordWithMatchProbability:
    locator: Locator
    text: str
    match_probability: float


class PageHandler:
    def __init__(self, page: Page) -> None:
        self.page: Page = page

    def in_netflix(self, action: list[str]) -> None:
        if "netflix" in self.page.url:
            title = action[0]
            match title:
                case "close":
                    print("Close movie")
                    self.page.get_by_role("dialog").get_by_role("button").locator('[data-uia="previewModal-closebtn"]:scope').click()
                case "start":
                    print("Start movie")
                    self.page.get_by_role("dialog").get_by_role("link").locator('[data-uia="play-button"]:scope').click()
                case _:
                    self.in_netflix_movie_with_title(title)
        else:
            print(f"The page is not netflix but {self.page.title()}")

    def in_netflix_movie_with_title(self, title: str) -> None:
        lst = self.page.get_by_role('link')
        locators_with_probabilities = [self.build_word_with_match_probability(el, title) for el in lst.all()]
        closest = max(locators_with_probabilities, key=lambda item: item.match_probability)
        print(f"Netflix click {closest}")
        closest.locator.click()
        print(f"clicked on {title}")

    def build_word_with_match_probability(self, el: Locator, title: str) -> WordWithMatchProbability:
        text_content = el.text_content()
        text_content_words = text_content.split(" ")
        return WordWithMatchProbability(el, text_content, max([fuzz.ratio(title,  one_word) for one_word in text_content_words]))

    def is_valid(self):
        return not self.page.is_closed()

class BrowserHandler:
    def __init__(self, browser: Browser) -> None:
        self.browser: Browser = browser
        self.page_handler: Optional[PageHandler] = None

    def open_page(self, web_pages: list[str]):
        web_page_name = web_pages[0]
        print(f"Opening page {web_page_name}")
        web_page_url = self.extract_web_page(web_page_name)
        if web_page_url is not None:
            print(f"Opening page with url {web_page_url}")
            default_context = self.browser.contexts[0]
            page = default_context.pages[0]
            page.goto(web_page_url)
            self.page_handler = PageHandler(page)
        else:
            print(f"Url not found for page {web_page_name}")


    @classmethod
    def extract_web_page(cls, web_page: str) -> Optional[str]:
        match web_page:
            case "repubblica" | "republican":
                return "https://www.repubblica.it"
            case "netflix":
                return "https://www.netflix.com"
            case _:
                return None

    def in_netflix(self, action: list[str]) -> None:
        if self.page_handler is not None and self.page_handler.is_valid():
            self.page_handler.in_netflix(action)
        else:
            print(f"Page handler not found or invalid for action {action}")

    def is_valid(self):
        return self.browser.is_connected()

class BrowserBuilder:
    def __init__(self) -> None:
        self.playwright = sync_playwright().start()

    def open_browser(self) -> BrowserHandler:
        os.system("/snap/bin/chromium --remote-debugging-port=9222 &")
        browser = self.connect_to_browser_when_available()
        return BrowserHandler(browser)

    def connect_to_browser_if_available(self) -> Optional[Browser]:
        try:
            return self.playwright.chromium.connect_over_cdp("http://localhost:9222")
        except:
            return None

    def connect_to_browser_when_available(self) -> Optional[Browser]:
        for i in range(0, 10):
            browser = self.connect_to_browser_if_available()
            if browser is not None:
                return browser
            time.sleep(1)
        return None



class MicrophoneHandler:
    def __init__(self) -> None:
        self.browser_builder = BrowserBuilder()
        self.browser_handler: Optional[BrowserHandler] = None

    def do_something(self, command_words: list[str]) -> None:
        if len(command_words) > 0:
            try:
                match command_words[0]:
                    case "browser" | "browse":
                        if len(command_words) > 1:
                            if self.browser_handler is None or not self.browser_handler.is_valid():
                                self.browser_handler = self.browser_builder.open_browser()
                                print(f"Crated browser handler {self.browser_handler}")
                            self.browser_handler.open_page(command_words[1:])
                        else:
                            print("Not enough words after browser")
                    case "netflix":
                        if self.browser_handler is not None and self.browser_handler.is_valid():
                            if len(command_words) > 1:
                                self.browser_handler.in_netflix(command_words[1:])
                            else:
                                print("Not enough words after netflix")
                        else:
                            print("No open browser")
                    case _:
                        print(f"Command {command_words} not recognized")
            except TargetClosedError:
                self.browser_handler = None
                print(f"Error executing {command_words}:{traceback.format_exc()}. Use new browser instance")
            except Exception:
                print(f"Error executing {command_words}:{traceback.format_exc()}")
        else:
            print("No command to run")



    def do_something_if_requested(self, words: list[str]) -> None:
        words = [w for w in words if w not in   ["a", "and", "but", "the", "that"]]
        if len(words) > 0:
            first_word = words[0]
            if first_word == "max"  and len(words) >= 2:
                self.do_something(words[1:])
            elif first_word == "hi" and len(words) >= 3:
                self.do_something_if_requested(words[1:])
            else:
                print(f"Not a command: {words}")
        else:
            print("No command, nothing to do")


    def read_from_microphone(self, recognizer: KaldiRecognizer, data: Any) -> None:
        if recognizer.AcceptWaveform(data):
            result_text = recognizer.Result()
            # convert the recognizerResult string into a dictionary
            result_dict = json.loads(result_text)
            text = result_dict.get("text", "")
            if text != "":
                print(f"Text from microphone: {text}")
                self.do_something_if_requested(text.split(" "))
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
    microphone_handler = MicrophoneHandler()
    try:
        with sd.RawInputStream(dtype='int16', callback=callback_handler.recordCallback):
            while True:
                data = q.get()
                microphone_handler.read_from_microphone(recognizer, data)
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