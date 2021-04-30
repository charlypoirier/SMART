class Question:
    
    def __init__(self, stem, options, answer):
        self.stem = stem
        self.options = options
        self.answer = answer

    def to_aiken(self):
        aiken = self.stem + "\n"
        for i in range(len(self.options)):
            aiken += f"{chr(ord('A')+i)}. {self.options[i]}\n"
        aiken += f"ANSWER: {chr(ord('A')+self.answer)}\n\n"
        return aiken