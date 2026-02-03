import queue
import sys
from typing import Any

import sounddevice as sd
from _cffi_backend import buffer
from vosk import KaldiRecognizer

from microphone.microphone_handler import MicrophoneHandler


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

