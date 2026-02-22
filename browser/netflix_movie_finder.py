from typing import Optional

from playwright.sync_api import Locator

from browser.closest_title_finder import ClosestTitleFinder, PossibleMatch


class NetflixMovieFinder:
    @classmethod
    def in_netflix_movie_with_title(cls, locator_movie_links: Locator, title_to_search: str) -> None:
        possible_matches =  [cls._possible_match_from_locator(l) for l in locator_movie_links.all()]
        print(f"Possible matches: {[p.text for p in possible_matches]}")
        closest = ClosestTitleFinder[Locator].fuzzy_search_of_text(possible_matches, title_to_search)
        print(f"Netflix click {closest}")
        closest.possible_match.source.click()
        print(f"clicked on {title_to_search}")

    @classmethod
    def _possible_match_from_locator(cls, locator: Locator) -> Optional[PossibleMatch[Locator]]:
        text_content = locator.text_content().strip()
        if text_content != '':
            return PossibleMatch[Locator](locator, text_content)
        else:
            return None