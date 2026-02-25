import nava

def play_correct() -> None:
    nava.play((r'sounds/correct.wav')

def play_error() -> None:
    nava.play((r'sounds/error.wav')

def print_error(text: str) -> None:
    print(text)
    play_error()

def print_correct(text: str) -> None:
    print(text)
    play_correct()
