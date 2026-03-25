import traceback
from typing import Optional

import psutil
from playwright.sync_api import Browser, Page

from browser.config.config_extraction import ConfigExtraction
from browser.netflix.netflix_page_handler import NetflixPageHandler
from browser.page_handler import PageHandler
from browser.youtube.youtube_page_handler import YoutubePageHandler
from browser.config.config_reader import Config, Site, YoutubeSite
from utils.sounds import print_error, print_correct


class BrowserHandler:
    def __init__(self, browser: Browser, config: Config) -> None:
        self._browser: Browser = browser
        self._config = config
        self._page_handlers: dict[str, PageHandler] = {}

    def open_page(self, web_page_words: list[str]) -> None:
        page_type = web_page_words[0]
        print(f"Opening page {page_type}")
        web_page_url = self._extract_web_page(page_type, web_page_words)
        if web_page_url is not None:
            print(f"Opening page with url {web_page_url}")
            default_context = self._browser.contexts[0]
            page = default_context.pages[0]
            page.goto(web_page_url)
            page.set_default_timeout(2000)
            self._page_handlers[page_type] = self._create_handler(page_type, page)
            print_correct(f"Opened page with url {web_page_url}")
        else:
            print_error(f"Url not found for page {page_type}")


    def _create_handler(self, page_type: str, page: Page) -> Optional[PageHandler]:
        match page_type:
            case "netflix":
                return NetflixPageHandler(page, self._config)
            case "tube":
                return YoutubePageHandler(page, self._config)
            case _:
                return None

    def _extract_web_page(self, web_page_key: str, wbe_page_additional_infos: list[str]) -> Optional[str]:
        extraction = ConfigExtraction(self._config)
        match web_page_key:
            case "netflix":
                return "https://www.netflix.com"
            case "tube":
                definition = extraction.extract_youtube_site_defintion_from_key(web_page_key)
                return f"https://www.youtube.com/{definition.path}" if definition is not None else None
            case _:
                definition = extraction.extract_site_defintion_from_key(web_page_key)
                return definition.url if definition is not None else None


    def in_page(self, page_type: str, action: list[str]) -> None:
        page_handler = self._page_handlers.get(page_type)
        if page_handler is not None and page_handler.is_valid():
            page_handler.in_page(action)
        else:
            print_error(f"Page handler not found or invalid for action {action}")

    def close(self) -> None:
        print("Closing the browser")
        self._browser.close()
        browser_procs = [proc for proc in psutil.process_iter(['name']) if proc.info['name'] == "chromium"]
        print(f"Found {len(browser_procs)} chromium processes")
        for proc in browser_procs:
            try:
                print(f"Stopping {proc.pid}")
                proc.terminate()
            except Exception:
                print_error(f"Error terminating process {traceback.format_exc()}")
        print_correct("Browser closed")

    def is_valid(self):
        return self._browser is not None and self._browser.is_connected()
