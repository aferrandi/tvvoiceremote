import tomllib
from dataclasses import dataclass


@dataclass(frozen=True)
class Site:
    key: str
    url: str

@dataclass(frozen=True)
class Config:
    microphone_name: str
    chromium_path: str
    auditor_name: str
    sites: list[Site]

def read_config() -> Config:
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        data["sites"] = [Site(**s) for s in data["sites"]]
        config = Config(**data)
        print(f"Configuration: {config}")
        return config
