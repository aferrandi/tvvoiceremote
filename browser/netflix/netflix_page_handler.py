from playwright.sync_api import Page

from browser.netflix.netflix_movie_finder import NetflixMovieFinder
from browser.page_handler import PageHandler
from config_reader import Config
from utils.sounds import print_error, print_correct


class NetflixPageHandler(PageHandler):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page)
        self._finder = NetflixMovieFinder(config)

    def in_page(self, action: list[str]) -> None:
        if "netflix" in self.page().url:
            title = action[0]
            match title:
                case "close":
                    self._close()
                case "start":
                    self._start()
                case "stop":
                    self._stop()
                case "play":
                    self._play()
                case "wait":
                    self._wait()
                case "back":
                    self._back()
                case "down":
                    self._down()
                case "up":
                    self._up()
                case _:
                    self._netflix_movie(title)
        else:
            print_error(f"The page is not netflix but {self.page().title()}")

    def _netflix_movie(self, title: str) -> None:
        if not self._watching_video():
            locator_movie_links = self.page().locator('[id^="title-card"]').get_by_role('link')
            self._finder.in_netflix_movie_with_title(locator_movie_links, title)
        else:
            print_error("Please stop the movie first")

    def _wait(self) -> None:
        if self._watching_video():
            print("Pause movie")
            self._make_buttons_visible()
            self.page().get_by_role("button").locator('[data-uia="control-play-pause-pause"]:scope').click()
            print_correct("Movie paused")
        else:
            print_error("Not watching a movie")

    def _play(self) -> None:
        if self._watching_video():
            print("Play movie")
            self._make_buttons_visible()
            self.page().get_by_role("button").locator('[data-uia="control-play-pause-play"]:scope').click()
            print_correct("Movie played")
        else:
            print_error("Not watching a movie")

    def _stop(self) -> None:
        if self._watching_video():
            print("Stop movie")
            self._make_buttons_visible()
            self.page().get_by_role("button").locator('[data-uia="control-nav-back"]:scope').click()
            print_correct("Movie stopped")
        else:
            print_error("Not watching a movie")

    def _start(self) -> None:
        if not self._watching_video():
            print("Start movie")
            self.page().get_by_role("dialog").get_by_role("link").locator('[data-uia="play-button"]:scope').click()
            print_correct("Movie started")
        else:
            print_error("Please stop the movie first")

    def _close(self) -> None:
        if not self._watching_video():
            print("Close movie")
            self.page().get_by_role("dialog").get_by_role("button").locator(
                '[data-uia="previewModal-closebtn"]:scope').click()
            print_correct("Movie closed")
        else:
            print_error("Please stop the movie first")

    def _make_buttons_visible(self) -> None:
        if self._watching_video():
            self.page().locator("video").hover()

    def _watching_video(self) -> bool:
        return self.page().locator("video").count() > 0

    def _back(self) -> None:
        self._make_buttons_visible()
        self.page().get_by_role("button").locator('[data-uia="control-navigate-back"]:scope').click()
        print_correct("Navigated back")

    def _down(self):
        if not self._watching_video():
            print("scrolling down")
            self.page().keyboard.press("PageDown")
            print_correct("Scrolled down")
        else:
            print_error("Please stop the movie first")

    def _up(self):
        if not self._watching_video():
            print("scrolling up")
            self.page().keyboard.press("PageUp")
            print_correct("Scrolled up")
        else:
            print_error("Please stop the movie first")



