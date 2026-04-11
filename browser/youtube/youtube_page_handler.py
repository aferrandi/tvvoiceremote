from playwright.sync_api import Page, Locator

from browser.page_handler import PageHandler
from browser.video.movie_finder import MovieFinder
from browser.config.config_reader import Config
from utils.sounds import print_error, print_correct


class YoutubePageHandler(PageHandler):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page)
        self._finder = MovieFinder(config)

    def in_page(self, action: list[str]) -> None:
        if "youtube" in self.page().url:
            title = action[0]
            match title:
                case "stop":
                    self._stop()
                case "play":
                    self._play()
                case "wait":
                    self._wait()
                case "down":
                    self._down()
                case "up":
                    self._up()
                case _:
                    self._youtube_movie(title)
        else:
            print_error(f"The page is not youtube but {self.page().title()}")

    def _youtube_movie(self, title: str) -> None:
        if not self._watching_video():
            locator_movie_links = self.page().locator('[id="video-title"]').get_by_role('link')
            self._finder.in_page_movie_with_title(locator_movie_links, title)
        else:
            print_error("Please stop the movie first")

    def _wait(self) -> None:
        if self._watching_video():
            print("Pause movie")
            self.page().keyboard.press("k")
            print_correct("Movie paused")
        else:
            print_error("Not watching a movie")

    def _play(self) -> None:
        if self._watching_video():
            print("Play movie")
            self.page().keyboard.press("k")
            print_correct("Movie played")
        else:
            print_error("Not watching a movie")

    def _stop(self) -> None:
        if self._watching_video():
            print("Stop movie")
            self.page().go_back()
            print_correct("Movie stopped")
        else:
            print_error("Not watching a movie")

    def _button_locator(self, locator: str) -> Locator:
        return self.page().get_by_role("button").locator(locator)

    def _watching_video(self) -> bool:
        return self.page().locator("div.html5-video-container: has(video)").count() > 0

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



