import re

class Question:

    def __init__(self, stem, options, answer):
        self.stem = re.sub(r"\s+", " ", stem.capitalize()) # What color is the sky?
        self.options = options # ["Blue", "Green", "Red"]
        self.answer = answer # 0

    def to_aiken(self):
        aiken = self.stem + "\n"
        for i in range(len(self.options)):
            aiken += f"{chr(ord('A')+i)}. {self.options[i]}\n"
        aiken += f"ANSWER: {chr(ord('A')+self.answer)}\n\n"
        return aiken

    def __hash__(self):
      return hash(str(self.stem))

    def __eq__(self, other):
        return self.stem==other.stem