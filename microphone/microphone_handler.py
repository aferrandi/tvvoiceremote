import json
import traceback
from typing import Optional, Any

from playwright._impl._errors import TargetClosedError
from vosk import KaldiRecognizer

from browser.browser_builder import BrowserBuilder
from browser.browser_handler import BrowserHandler
from config_reader import Config
from utils.sounds import print_error
from utils.text_utils import TextUtils


class MicrophoneHandler:
    def __init__(self, config: Config) -> None:
        self.browser_builder = BrowserBuilder(config)
        self.browser_handler: Optional[BrowserHandler] = None
        self._config = config

    def _do_something(self, command_words: list[str]) -> None:
        if len(command_words) > 0:
            try:
                match command_words[0]:
                    case "browser" | "browse":
                        self._do_something_with_browser(command_words)
                    case "netflix":
                        self._do_something_with_netflix(command_words)
                    case _:
                        print_error(f"Command {command_words} not recognized")
            except TargetClosedError:
                self.browser_handler = None
                print_error(f"Error executing {command_words}:{traceback.format_exc()}. Use new browser instance")
            except Exception:
                print_error(f"Error executing {command_words}:{traceback.format_exc()}")
        else:
            print_error("No command to run")

    def _do_something_with_netflix(self, command_words: list[str]):
        if self.browser_handler is not None and self.browser_handler.is_valid():
            if len(command_words) > 1:
                self.browser_handler.in_page("netflix", command_words[1:])
            else:
                print_error("Not enough words after netflix")
        else:
            print_error("No open browser")

    def _do_something_with_browser(self, command_words: list[str]):
        if len(command_words) > 1:
            if self.browser_handler is None or not self.browser_handler.is_valid():
                self.browser_handler = self.browser_builder.open_browser()
                print(f"Crated browser handler {self.browser_handler}")
            self.browser_handler.open_page(command_words[1:])
        else:
            print_error("Not enough words after browser")

    def do_something_if_requested(self, words: list[str]) -> None:
        words = TextUtils.remove_stopwords(words)
        if len(words) > 0:
            first_word = words[0]
            if first_word == self._config.auditor_name and len(words) >= 2:
                self._do_something(words[1:])
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
