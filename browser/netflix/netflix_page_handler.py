from playwright.sync_api import Page, Locator

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
            self._make_button_visible_and_click('[data-uia="control-play-pause-pause"]:scope')
            print_correct("Movie paused")
        else:
            print_error("Not watching a movie")

    def _play(self) -> None:
        if self._watching_video():
            print("Play movie")
            self._make_button_visible_and_click('[data-uia="control-play-pause-play"]:scope')
            print_correct("Movie played")
        else:
            print_error("Not watching a movie")

    def _stop(self) -> None:
        if self._watching_video():
            print("Stop movie")
            self._make_button_visible_and_click('[data-uia="control-nav-back"]:scope')
            print_correct("Movie stopped")
        else:
            print_error("Not watching a movie")

    def _button_locator(self, locator: str) -> Locator:
        return self.page().get_by_role("button").locator(locator)

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

    def _make_button_visible_and_click(self, locator: str) -> None:
        if self._watching_video():
            if self._until_button_is_visible(locator):
                print("Clicking button")
                self._button_locator(locator).click()
                print("Button clicked")
            else:
                print_error("Not possible to click button")

    def _until_button_is_visible(self, locator: str) -> bool:
        for i in range(0, 30):
            button = self._button_locator(locator)
            if self._is_enabled(button):
                print("Making buttons visible")
                return True
            else:
                print("Making buttons visible")
                # '[data-uia="video-canvas"]:scope'
                self.page().mouse.move(100+i*20, 100+i*20)
        return False


    def _is_enabled(self, locator: Locator) -> bool:
        try:
            enabled = locator.is_enabled(timeout=300)
            if not enabled:
                print("Not enabled")
            return enabled
        except Exception as ex:
            print(f"not enabled error {ex}")
            return False

    def _is_visible(self, locator: Locator) -> bool:
        try:
            visible = locator.is_visible(timeout=300)
            if not visible:
                print("not visible")
            return visible
        except Exception as ex:
            print(f"not visible error {ex}")
            return False


    def _watching_video(self) -> bool:
        return self.page().locator("video").count() > 0

    def _back(self) -> None:
        self._make_button_visible_and_click('[data-uia="control-navigate-back"]')
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



