import sounddevice as sd
from vosk import KaldiRecognizer, Model

from browser.config.config_reader import Config


def init_recognizer(config: Config) -> KaldiRecognizer:
    # list all audio devices known to your system
    print("Display input/output devices")
    devices = sd.query_devices()
    print(devices)
    sd.default.device = config.microphone_name
    # get the samplerate - this is needed by the Kaldi recognizer
    device_info = sd.query_devices(sd.default.device, 'input')
    samplerate = int(device_info['default_samplerate'])
    # build the model and recognizer objects.
    print("===> Build the model and recognizer objects.  This will take a few minutes.")
    model = Model(config.vosk_model_path)
    recognizer = KaldiRecognizer(model, samplerate)
    recognizer.SetWords(False)
    # display the default input device
    print(f"===> Initial Default Device Number:{sd.default.device[0]} Description: {device_info}")
    return recognizer
