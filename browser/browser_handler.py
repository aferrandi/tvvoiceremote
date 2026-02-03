from typing import Optional

from playwright.sync_api import Browser

from browser.page_handler import PageHandler


class BrowserHandler:
    def __init__(self, browser: Browser) -> None:
        self.browser: Browser = browser
        self.page_handler: Optional[PageHandler] = None

    def open_page(self, web_pages: list[str]):
        web_page_name = web_pages[0]
        print(f"Opening page {web_page_name}")
        web_page_url = self.extract_web_page(web_page_name)
        if web_page_url is not None:
            print(f"Opening page with url {web_page_url}")
            default_context = self.browser.contexts[0]
            page = default_context.pages[0]
            page.goto(web_page_url)
            page.set_default_timeout(2000)
            self.page_handler = PageHandler(page)
        else:
            print(f"Url not found for page {web_page_name}")


    @classmethod
    def extract_web_page(cls, web_page: str) -> Optional[str]:
        match web_page:
            case "repubblica" | "republican":
                return "https://www.repubblica.it"
            case "netflix":
                return "https://www.netflix.com"
            case _:
                return None

    def in_netflix(self, action: list[str]) -> None:
        if self.page_handler is not None and self.page_handler.is_valid():
            self.page_handler.in_netflix(action)
        else:
            print(f"Page handler not found or invalid for action {action}")

    def is_valid(self):
        return self.browser.is_connected()
