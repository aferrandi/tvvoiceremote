from playsound import playsound


def play_correct() -> None:
    playsound(r'sounds/correct.wav')

def play_error() -> None:
    playsound(r'sounds/error.wav')

def print_error(text: str) -> None:
    print(text)
    play_error()

def print_correct(text: str) -> None:
    print(text)
    play_correct()
