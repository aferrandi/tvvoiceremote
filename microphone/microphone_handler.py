import json
import traceback
from typing import Optional, Any

from playwright._impl._errors import TargetClosedError
from vosk import KaldiRecognizer

from browser.browser_builder import BrowserBuilder
from browser.browser_handler import BrowserHandler


class MicrophoneHandler:
    def __init__(self, chromium_path: str) -> None:
        self.browser_builder = BrowserBuilder(chromium_path)
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
                                self.browser_handler.in_page("netflix", command_words[1:])
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
        words = [w for w in words if len(w) > 2 and w not in ["and", "but", "the", "that"]]
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
