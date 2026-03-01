class TextUtils:
    @staticmethod
    def remove_stopwords(words: list[str]) -> list[str]:
        stop_words = ["hi", "how", "and", "but", "the", "that", "huh", "you", "yes", "her", "next", "when", "yeah", "what"]
        return [w for w in words if (len(w) > 2 or w == "up") and w not in stop_words]