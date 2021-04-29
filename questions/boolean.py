from questions.Question import Question
import spacy

nlp = spacy.load("en_core_web_sm")

"""
Boolean questions
1) Negate the sentence
2) Replace an adjective with its synonym or antonym (https://pypi.org/project/spacy-wordnet/)
3) Replace pronouns with subject from last sentence
4) Extract subject-verb-complement
"""

def generate(text):

    # Split into sentences
    document = nlp(text)
    sentences = document.sents

    # Generate questions
    questions = set()
    for sentence in sentences:
        question = Question(sentence.text, "True", ["False"])
        questions.add(question)

    return questions