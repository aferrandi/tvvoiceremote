from typing import Optional

from playwright.sync_api import Browser

from browser.config.config_extraction import ConfigExtraction
from browser.config.config_reader import Config
from browser.netflix.netflix_page_handler import NetflixPageHandler
from browser.page_handler import PageHandler
from browser.youtube.youtube_page_handler import YoutubePageHandler
from utils.sounds import print_error, print_correct


class BrowserPageOpener:
    def __init__(self, browser: Browser, config: Config) -> None:
        self._browser: Browser = browser
        self._config = config

    def open_page(self, web_page_words: list[str]) -> Optional[PageHandler]:
        page_type = web_page_words[0]
        extraction = ConfigExtraction(self._config)
        match page_type:
            case "netflix":
                return self._open_page_nextflix()
            case "tube":
                return self._open_page_youtube(extraction, web_page_words)
            case _:
                return self._open_page_web(extraction, web_page_words)

    def _open_page_web(self, extraction: ConfigExtraction, web_page_words: list[str]) -> Optional[PageHandler]:
        web_key = web_page_words[0]
        definition = extraction.extract_site_defintion_from_key(web_key)
        if definition is not None:
            web_page_url = definition.url
            print(f"Opening page with url {web_page_url} as simple site")
            page = self._open_page_in_browser(web_page_url)
            print_correct(f"Opened page with url {web_page_url}")
            return None
        else:
            print_error(f"Definition not found for  {web_key}")
            return None

    def _open_page_youtube(self, extraction: ConfigExtraction, web_page_words: list[str]) -> Optional[PageHandler]:
        definition = extraction.extract_youtube_site_defintion_from_key(web_page_words[1])
        if definition is not None:
            web_page_url = f"https://www.youtube.com/{definition.path}"
            print(f"Opening page with url {web_page_url} in yoptube")
            page = self._open_page_in_browser(web_page_url)
            print_correct(f"Opened page with url {web_page_url}")
            return YoutubePageHandler(page, self._config)
        else:
            print_error(f"Definition not found for tube")
            return None

    def _open_page_nextflix(self) -> Optional[PageHandler]:
        web_page_url = "https://www.netflix.com"
        print(f"Opening page with url {web_page_url} in netflix")
        page = self._open_page_in_browser(web_page_url)
        print_correct(f"Opened page with url {web_page_url}")
        return NetflixPageHandler(page, self._config)

    def _open_page_in_browser(self, web_page_url: str) -> Page:
        default_context = self._browser.contexts[0]
        page = default_context.pages[0]
        page.goto(web_page_url)
        page.set_default_timeout(2000)
        return page
