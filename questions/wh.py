import spacy
from classes.question import Question

"""
Questions à réponses courtes

Ce qui serait bien, ce serait de générer un résumé du
texte (Aziz?) et utiliser le résumé comme entrée pour
générer des questions avec le code ci-dessous.
"""

nlp = spacy.load('en_core_web_sm')

def who(sentence, entity):
    question = sentence.text.replace(entity.text, 'who')
    question = question.replace('who\'s', 'whose')
    return Question(question, [entity.text], 0)

def when(sentence, entity):
    question = sentence.text.replace(entity.text, 'when')
    return Question(question, [entity.text], 0)

def where(sentence, entity):
    question = sentence.text.replace(entity.text, 'where')
    return Question(question, [entity.text], 0)
    
def what(sentence, entity):
    question = sentence.text.replace(entity.text, 'what')
    return Question(question, [entity.text], 0)

def how_many(sentence, entity):
    question = sentence.text.replace(entity.text, 'how many')
    return Question(question, [entity.text], 0)

def how_much(sentence, entity):
    question = sentence.text.replace(entity.text, 'how much')
    return Question(question, [entity.text], 0)

def generate(text):

    document = nlp(text)
    questions = set()

    for sentence in document.sents:
        for entity in sentence.ents:
            label = entity.label_
            start = sentence.text.index(entity.text)
            if label in ['PERSON']:
                question = who(sentence, entity)
            elif label in ['DATE']:
                question = when(sentence, entity)
            elif label in ['GPE', 'LOC', 'FAC']:
                question = where(sentence, entity)
            elif label in ['PRODUCT', 'ORG']:
                question = what(sentence, entity)
            elif label in ['QUANTITY']:
                question = how_many(sentence, entity)
            elif label in ['MONEY']:
                question = how_much(sentence, entity)
            else: continue # Go to the next iteration
            
            question.replace('.', '?')
            question = question.capitalize()
            questions.add(question)

    return questions

"""
> Supported
PERSON People, including fictional. NORP Nationalities or religious or political groups.
DATE Absolute or relative dates or periods.
GPE Countries, cities, states.
LOC Non-GPE locations, mountain ranges, bodies of water.
FAC Buildings, airports, highways, bridges, etc.
PRODUCT Objects, vehicles, foods, etc. (Not services.)
MONEY Monetary values, including unit.
QUANTITY Measurements, as of weight or distance.

> Unsupported
ORDINAL “first”, “second”, etc.
CARDINAL Numerals that do not fall under another type.
EVENT Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART Titles of books, songs, etc.
LAW Named documents made into laws.
LANGUAGE Any named language.
ORG Companies, agencies, institutions, etc.
TIME Times smaller than a day.
PERCENT Percentage, including ”%“.
"""