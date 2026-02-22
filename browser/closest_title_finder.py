from thefuzz import fuzz
from dataclasses import dataclass

from utils.text_utils import TextUtils


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
        words = possible_match.text.split(" ")
        words_no_stopwords = TextUtils.remove_stopwords(words)
        words_with_probabilities = [fuzz.ratio(title_to_search, one_word) for one_word in words_no_stopwords]
        whole_sentence_with_probability = fuzz.ratio(title_to_search, " ".join(words_no_stopwords))
        return WordWithMatchProbability(possible_match, max(words_with_probabilities + [whole_sentence_with_probability]))