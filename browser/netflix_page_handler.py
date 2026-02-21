from playwright.sync_api import Page

from browser.netflix_movie_finder import NetflixMovieFinder
from browser.page_handler import PageHandler


class NetflixPageHandler(PageHandler):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def in_page(self, action: list[str]) -> None:
        if "netflix" in self.page().url:
            title = action[0]
            match title:
                case "close":
                    if not self._watching_video():
                        print("Close movie")
                        self.page().get_by_role("dialog").get_by_role("button").locator('[data-uia="previewModal-closebtn"]:scope').click()
                    else:
                        print("Please stop the movie first")
                case "start":
                    if not self._watching_video():
                        print("Start movie")
                        self.page().get_by_role("dialog").get_by_role("link").locator('[data-uia="play-button"]:scope').click()
                    else:
                        print("Please stop the movie first")
                case "stop":
                    if self._watching_video():
                        print("Stop movie")
                        self._make_buttons_visible()
                        self.page().get_by_role("button").locator('[data-uia="control-nav-back"]:scope').click()
                    else:
                        print("Not watching a movie")
                case "play":
                    if self._watching_video():
                        print("Play movie")
                        self._make_buttons_visible()
                        self.page().get_by_role("button").locator('[data-uia="control-play-pause-play"]:scope').click()
                    else:
                        print("Not watching a movie")
                case "wait":
                    if self._watching_video():
                        print("Pause movie")
                        self._make_buttons_visible()
                        self.page().get_by_role("button").locator('[data-uia="control-play-pause-pause"]:scope').click()
                    else:
                        print("Not watching a movie")
                case _:
                    if not self._watching_video():
                        locator_movie_links = self.page().get_by_role('link')
                        NetflixMovieFinder.in_netflix_movie_with_title(locator_movie_links, title)
                    else:
                        print("Please stop the movie first")
        else:
            print(f"The page is not netflix but {self.page().title()}")

    def is_valid(self):
        return not self.page().is_closed()

    def _make_buttons_visible(self):
        self.page().locator("video").hover()

    def _watching_video(self) -> bool:
        return self.page().locator("video").count() > 0





