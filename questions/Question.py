class Question:
    
    # Constructor
    def __init__(self, stem, options, answer):
        self.stem = stem
        self.options = options
        self.answer = answer

    def to_aiken(self):
        aiken = self.stem + '\n'
        for i in range(len(self.options)):
            aiken += chr(ord('A')+i) + '. ' + self.options[i] + '\n'
        aiken += 'ANSWER: '+chr(ord('A') + self.answer) + '\n\n'
        return aiken