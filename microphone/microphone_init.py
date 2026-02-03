import sounddevice as sd
from vosk import KaldiRecognizer, Model


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
