from thefuzz import fuzz
from dataclasses import dataclass

@dataclass(frozen=True)
class PossibleMatch[T]:
    source: T
    text: str

@dataclass(frozen=True)
class WordWithMatchProbability[T]:
    possible_match: PossibleMatch[T]
    match_probability: float

class ClosestTitleFinder[T]:
    @classmethod
    def fuzzy_search_of_text(cls, possible_matches: list[PossibleMatch[T]], title_to_search: str) -> WordWithMatchProbability[T]:
        locators_with_probabilities = [cls.build_word_with_match_probability(p, title_to_search) for p in possible_matches]
        closest = max(locators_with_probabilities, key=lambda item: item.match_probability)
        return closest

    @classmethod
    def build_word_with_match_probability(cls, possible_match: PossibleMatch[T], title_to_search: str) -> WordWithMatchProbability[T]:
        text_content_words = possible_match.text.split(" ")
        return WordWithMatchProbability(possible_match, max([fuzz.ratio(title_to_search, one_word) for one_word in text_content_words]))