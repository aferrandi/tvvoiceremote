from typing import Optional

from playwright.sync_api import Locator

from browser.netflix.closest_title_finder import ClosestTitleFinder, PossibleMatch
from config_reader import Config
from utils.sounds import print_correct, print_error


class NetflixMovieFinder:
    def __init__(self, config: Config) -> None:
        self._config =  config

    def in_netflix_movie_with_title(self, locator_movie_links: Locator, title_to_search: str) -> None:
        possible_matches =  [self._possible_match_from_locator(l) for l in locator_movie_links.all()]
        print(f"Possible matches: {[p.text for p in possible_matches]}")
        closest = ClosestTitleFinder[Locator].fuzzy_search_of_text(possible_matches, title_to_search)
        if closest.match_probability > self._config.minimal_movie_match_probability:
            print(f"Netflix click {closest}")
            closest.possible_match.source.click()
            print_correct(f"clicked on {title_to_search}")
        else:
            print_error(f"Probability too low for {closest}")

    def _possible_match_from_locator(self, locator: Locator) -> Optional[PossibleMatch[Locator]]:
        text_content = locator.text_content().strip()
        if text_content != '':
            return PossibleMatch[Locator](locator, text_content)
        else:
            return None