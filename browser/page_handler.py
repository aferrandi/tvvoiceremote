from playwright.sync_api import Page

class PageHandler:
    def __init__(self, page: Page) -> None:
        self._page: Page = page

    def in_page(self, action: list[str]) -> None:
        pass

    def page(self) -> Page:
        return self._page
