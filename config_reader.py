import tomllib
from dataclasses import dataclass


@dataclass(frozen=True)
class Site:
    key: str
    url: str

@dataclass(frozen=True)
class Command:
    key: str
    text: str

@dataclass(frozen=True)
class Config:
    microphone_name: str
    chromium_path: str
    auditor_name: str
    minimal_movie_match_probability: float
    sites: list[Site]
    commands: list[Command]

def read_config() -> Config:
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        data["sites"] = [Site(**s) for s in data["sites"]]
        data["commands"] = [Command(**s) for s in data["commands"]]
        config = Config(**data)
        print(f"Configuration: {config}")
        return config
