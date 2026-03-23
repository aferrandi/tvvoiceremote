from typing import Optional

from browser.config.config_reader import Config, YoutubeSite, Site


class ConfigExtraction:
    def __init__(self, config: Config) -> None:
       self._config = config

    def extract_site_defintion_from_key(self, key: str) -> Optional[Site]:
        sites = [s for s in self._config.sites if s.key == key]
        return sites[0] if len(sites) > 0 else None


    def extract_youtube_site_defintion_from_key(self, key: str) -> Optional[YoutubeSite]:
        sites = [s for s in self._config.youtube_sites if s.key == key]
        return sites[0] if len(sites) > 0 else None