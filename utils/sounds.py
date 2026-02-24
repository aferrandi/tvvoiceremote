from preferredsoundplayer import soundplay


def play_correct() -> None:
    soundplay(r'sounds/correct.mp3')

def play_error() -> None:
    soundplay(r'sounds/error.mp3')

def print_error(text: str) -> None:
    print(text)
    play_error()

def print_correct(text: str) -> None:
    print(text)
    play_correct()
