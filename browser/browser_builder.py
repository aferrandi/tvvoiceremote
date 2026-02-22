import os
import time
from typing import Optional

from playwright.sync_api import sync_playwright, Browser

from browser.browser_handler import BrowserHandler
from config_reader import Config


class BrowserBuilder:
    def __init__(self, config: Config) -> None:
        self._config =  config
        self._playwright = sync_playwright().start()

    def open_browser(self) -> BrowserHandler:
        os.system(f"{self._config.chromium_path} --remote-debugging-port=9222 &")
        browser = self.connect_to_browser_when_available()
        return BrowserHandler(browser, self._config.sites)

    def connect_to_browser_if_available(self) -> Optional[Browser]:
        try:
            return self._playwright.chromium.connect_over_cdp("http://localhost:9222")
        except:
            return None

    def connect_to_browser_when_available(self) -> Optional[Browser]:
        for i in range(0, 10):
            browser = self.connect_to_browser_if_available()
            if browser is not None:
                return browser
            time.sleep(1)
        return None
