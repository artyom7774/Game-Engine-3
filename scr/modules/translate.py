import hjson
import os


class Translate:
    def __init__(self, lang: str) -> None:
        self.lang = lang

        self.out = {}

    def __call__(self, *args) -> None:
        return self.translate(args[0])

    def update(self, lang: str) -> None:
        self.lang = lang

    def translate(self, word: str) -> str:
        if not os.path.exists(f"scr/files/bundles/{self.lang.lower()}.hjson") and self.lang == "EN":
            return word

        if self.lang not in self.out:
            self.out[self.lang] = hjson.load(open(f"scr/files/bundles/{self.lang.lower()}.hjson", encoding="utf-8"))

        if word in self.out[self.lang]:
            return self.out[self.lang][word]

        else:
            return word
