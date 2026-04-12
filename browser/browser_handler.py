import traceback

import psutil
from playwright.sync_api import Browser

from browser.brower_page_opener import BrowserPageOpener
from browser.config.config_reader import Config
from browser.page_handler import PageHandler
from utils.sounds import print_error, print_correct


class BrowserHandler:

    def __init__(self, browser: Browser, config: Config) -> None:
        self._browser: Browser = browser
        self._config = config
        self._page_handlers: dict[str, PageHandler] = {}
        self._opener = BrowserPageOpener(browser, config)

    def open_page(self, web_page_words: list[str]) -> None:
        page_handler = self._opener.open_page(web_page_words)
        if page_handler is not None:
            self._page_handlers[page_handler.page_type()] = page_handler

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
