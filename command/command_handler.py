import subprocess

from config_reader import Config
from utils.sounds import print_error, print_correct


class CommandHandler:
    def __init__(self, config: Config):
        self._config = config

    def run_command(self, command_words: list[str]) -> None:
        command_key = command_words[0]
        matching_commands = [c.text for c in self._config.commands if c.key == command_key]
        if len(matching_commands) > 0:
            command_text = f"{matching_commands[0]} {' '.join(command_words[1:])}"
            result = subprocess.run(command_text, shell=True, capture_output=True, text=True)
            print_correct(f"Command {command_text}result {result.stdout.strip()}")
        else:
            print_error(f"Command with key {command_key} not found")


