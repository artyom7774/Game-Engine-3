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
        if len(word) == 0:
            return ""

        point = False

        if word[0] == "-":
            word = word[1:]

            point = True

        spaces = 0

        while word[0] == " ":
            word = word[1:]

            spaces += 1

        if not os.path.exists(f"src/files/bundles/{self.lang.lower()}.hjson") and self.lang == "EN":
            return word

        if self.lang not in self.out:
            self.out[self.lang] = hjson.load(open(f"src/files/bundles/{self.lang.lower()}.hjson", encoding="utf-8"))

        if " " * spaces + word in self.out[self.lang]:
            return self.out[self.lang][" " * spaces + word]

        elif word in self.out[self.lang]:
            answer = self.out[self.lang][word]

        else:
            answer = word

        return ("•" if point else "") + " " * spaces + answer
