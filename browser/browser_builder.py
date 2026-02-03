import os
import time
from typing import Optional

from playwright.sync_api import sync_playwright, Browser

from browser.browser_handler import BrowserHandler


class BrowserBuilder:
    def __init__(self) -> None:
        self.playwright = sync_playwright().start()

    def open_browser(self) -> BrowserHandler:
        os.system("/snap/bin/chromium --remote-debugging-port=9222 &")
        browser = self.connect_to_browser_when_available()
        return BrowserHandler(browser)

    def connect_to_browser_if_available(self) -> Optional[Browser]:
        try:
            return self.playwright.chromium.connect_over_cdp("http://localhost:9222")
        except:
            return None

    def connect_to_browser_when_available(self) -> Optional[Browser]:
        for i in range(0, 10):
            browser = self.connect_to_browser_if_available()
            if browser is not None:
                return browser
            time.sleep(1)
        return None
