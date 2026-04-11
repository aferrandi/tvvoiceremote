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
        extraction = ConfigExtraction(self._config)
        match page_type:
            case "netflix":
                web_page_url = "https://www.netflix.com"
                print(f"Opening page with url {web_page_url} in netflix")
                page = self._open_page_in_browser(web_page_url)
                self._page_handlers[page_type] = NetflixPageHandler(page, self._config)
                print_correct(f"Opened page with url {web_page_url}")
            case "tube":
                definition = extraction.extract_youtube_site_defintion_from_key(web_page_words[1])
                if definition is not None:
                    web_page_url = f"https://www.youtube.com/{definition.path}"
                    print(f"Opening page with url {web_page_url} in yoptube")
                    page = self._open_page_in_browser(web_page_url)
                    self._page_handlers[page_type] = YoutubePageHandler(page, self._config)
                    print_correct(f"Opened page with url {web_page_url}")
                else:
                    print_error(f"Definition not found for  {page_type}")
            case _:
                definition = extraction.extract_site_defintion_from_key(web_page_words[0])
                if definition is not None:
                    web_page_url = definition.url
                    print(f"Opening page with url {web_page_url} as simple site")
                    page = self._open_page_in_browser(web_page_url)
                    print_correct(f"Opened page with url {web_page_url}")
                else:
                    print_error(f"Definition not found for  {page_type}")

    def _open_page_in_browser(self, web_page_url: str) -> Page:
        default_context = self._browser.contexts[0]
        page = default_context.pages[0]
        page.goto(web_page_url)
        page.set_default_timeout(2000)
        return page

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
