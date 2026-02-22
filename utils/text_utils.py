class TextUtils:
    @staticmethod
    def remove_stopwords(words: list[str]) -> list[str]:
        return [w for w in words if len(w) > 2 and w not in ["and", "but", "the", "that", "huh"]]