import tomllib
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Site:
    key: str
    url: str

@dataclass(frozen=True)
class Config:
    chromium_path: str
    auditor_name: str
    sites: list[Site]

def read_config() -> Config:
    with open("config_example.toml", "rb") as f:
        data = tomllib.load(f)
        print(f"Configuration: {data}")
        return Config(**data)
