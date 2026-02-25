from playwright.sync_api import Page

class PageHandler:
    def __init__(self, page: Page) -> None:
        self._page: Page = page

    def in_page(self, action: list[str]) -> None:
        pass

    def page(self) -> Page:
        return self._page

    def is_valid(self):
        return not (self._page is None or self._page.is_closed())