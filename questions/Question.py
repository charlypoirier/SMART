class Question:
    
    # Constructor
    def __init__(self, proposition, answer, distractors):
        self.proposition = proposition
        self.answer = answer
        self.distractors = distractors

    def toAiken(self):
        string = self.proposition + "\n"
        letter = "A"
        string += letter + ". " + self.answer + "\n"
        for distractor in self.distractors:
            letter = chr(ord(letter) + 1)
            string += letter + ". " + distractor + "\n"
        string += "ANSWER: A\n\n"
        return string