from dataclasses import dataclass

from playwright.sync_api import Page, Locator
from thefuzz import fuzz

from browser.page_handler import PageHandler


@dataclass(frozen=True)
class WordWithMatchProbability:
    locator: Locator
    text: str
    match_probability: float


class NetflixPageHandler(PageHandler):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def in_page(self, action: list[str]) -> None:
        if "netflix" in self.page().url:
            title = action[0]
            match title:
                case "close":
                    if not self.watching_video():
                        print("Close movie")
                        self.page().get_by_role("dialog").get_by_role("button").locator('[data-uia="previewModal-closebtn"]:scope').click()
                    else:
                        print("Please stop the movie first")
                case "start":
                    if not self.watching_video():
                        print("Start movie")
                        self.page().get_by_role("dialog").get_by_role("link").locator('[data-uia="play-button"]:scope').click()
                    else:
                        print("Please stop the movie first")
                case "stop":
                    if self.watching_video():
                        print("Stop movie")
                        self.make_buttons_visible()
                        self.page().get_by_role("button").locator('[data-uia="control-nav-back"]:scope').click()
                    else:
                        print("Not watching a movie")
                case "play":
                    if self.watching_video():
                        print("Play movie")
                        self.make_buttons_visible()
                        self.page().get_by_role("button").locator('[data-uia="control-play-pause-play"]:scope').click()
                    else:
                        print("Not watching a movie")
                case "wait":
                    if self.watching_video():
                        print("Pause movie")
                        self.make_buttons_visible()
                        self.page().get_by_role("button").locator('[data-uia="control-play-pause-pause"]:scope').click()
                    else:
                        print("Not watching a movie")
                case _:
                    if not self.watching_video():
                        self.in_netflix_movie_with_title(title)
                    else:
                        print("Please stop the movie first")
        else:
            print(f"The page is not netflix but {self.page().title()}")

    def make_buttons_visible(self):
        self.page().locator("video").hover()

    def watching_video(self) -> bool:
        return self.page().locator("video").count() > 0

    def in_netflix_movie_with_title(self, title: str) -> None:
        lst = self.page().get_by_role('link')
        locators_with_probabilities = [self.build_word_with_match_probability(el, title) for el in lst.all()]
        closest = max(locators_with_probabilities, key=lambda item: item.match_probability)
        print(f"Netflix click {closest}")
        closest.locator.click()
        print(f"clicked on {title}")

    def build_word_with_match_probability(self, el: Locator, title: str) -> WordWithMatchProbability:
        text_content = el.text_content()
        text_content_words = text_content.split(" ")
        return WordWithMatchProbability(el, text_content, max([fuzz.ratio(title,  one_word) for one_word in text_content_words]))

    def is_valid(self):
        return not self.page().is_closed()

