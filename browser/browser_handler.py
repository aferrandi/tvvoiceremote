from typing import Optional

from playwright.sync_api import Browser, Page

from browser.netflix.netflix_page_handler import NetflixPageHandler
from browser.page_handler import PageHandler
from config_reader import Config
from utils.sounds import print_error, print_correct


class BrowserHandler:
    def __init__(self, browser: Browser, config: Config) -> None:
        self._browser: Browser = browser
        self._config = config
        self._page_handlers: dict[str, PageHandler] = {}

    def open_page(self, web_pages: list[str]) -> None:
        web_page_name = web_pages[0]
        print(f"Opening page {web_page_name}")
        web_page_url = self._extract_web_page(web_page_name)
        if web_page_url is not None:
            print(f"Opening page with url {web_page_url}")
            default_context = self._browser.contexts[0]
            page = default_context.pages[0]
            page.goto(web_page_url)
            page.set_default_timeout(2000)
            self._page_handlers[web_page_name] = self._create_handler(web_page_name, page)
            print_correct(f"Opened page with url {web_page_url}")
        else:
            print_error(f"Url not found for page {web_page_name}")


    def _create_handler(self, page_type: str, page: Page) -> Optional[PageHandler]:
        match page_type:
            case "netflix":
                return NetflixPageHandler(page, self._config)
            case _:
                return None

    def _extract_web_page(self, web_page: str) -> Optional[str]:
        match web_page:
            case "netflix":
                return "https://www.netflix.com"
            case _:
                matching_web_pages = [s for s in self._config.sites if s.key == web_page]
                if len(matching_web_pages) > 0:
                    return matching_web_pages[0].url
                else:
                    return None

    def in_page(self, page_type: str, action: list[str]) -> None:
        page_handler = self._page_handlers.get(page_type)
        if page_handler is not None and page_handler.is_valid():
            page_handler.in_page(action)
        else:
            print_error(f"Page handler not found or invalid for action {action}")

    def close(self) -> None:
        self._browser.close()

    def is_valid(self):
        return self._browser is not None and self._browser.is_connected()
