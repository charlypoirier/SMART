import spacy

def who(sentence, entity, start):
    if start == 0:
        question = sentence.replace(entity.text, 'Who')
    else:
        question = sentence.replace(entity.text, 'whom')
    question = question.replace('.', '?')
    question = question.replace('Who\'s', 'Whose')
    print(question, "("+entity.text+")")

def when(sentence, entity, start):
    question = sentence.replace(entity.text, 'when')
    if start == 0:
        question[0] = question[0].upper()
    question = question.replace('.', '?')
    print(question, "("+entity.text+")")

def where(sentence, entity, start):
    question = sentence.replace(entity.text, 'where')
    if start == 0:
        question[0] = question[0].upper()
    question = question.replace('.', '?')
    print(question, "("+entity.text+")")
    
def what(sentence, entity, start):
    question = sentence.replace(entity.text, 'what')
    if start == 0:
        question[0] = question[0].upper()
    question = question.replace('.', '?')
    print(question, "("+entity.text+")")

def how_many(sentence, entity, start):
    question = sentence.replace(entity.text, 'how many')
    if start == 0:
        question[0] = question[0].upper()
    question = question.replace('.', '?')
    print(question, "("+entity.text+")")

def how_much(sentence, entity, start):
    question = sentence.replace(entity.text, 'how much')
    if start == 0:
        question[0] = question[0].upper()
    question = question.replace('.', '?')
    print(question, "("+entity.text+")")

nlp = spacy.load('en_core_web_sm')
doc = nlp(open('inputs/short.txt').read())
print('---------- INPUT ----------')
print(doc.text)
print('---------------------------\n')

for sentence in doc.sents:
    for entity in sentence.ents:
        if entity.label_ in ['PERSON']:
            who(sentence.text, entity, sentence.text.index(entity.text))
        elif entity.label_ in ['DATE']: # 'TIME'
            when(sentence.text, entity, sentence.text.index(entity.text))
        elif entity.label_ in ['GPE', 'LOC']:
            where(sentence.text, entity, sentence.text.index(entity.text))
        elif entity.label_ in ['PRODUCT']:
            what(sentence.text, entity, sentence.text.index(entity.text))
        elif entity.label_ in ['QUANTITY']:
            how_many(sentence.text, entity, sentence.text.index(entity.text))
        elif entity.label_ in ['MONEY']:
            how_much(sentence.text, entity, sentence.text.index(entity.text))
print()

"""
> Others...
ORDINAL “first”, “second”, etc.
CARDINAL Numerals that do not fall under another type.
EVENT Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART Titles of books, songs, etc.
LAW Named documents made into laws.
LANGUAGE Any named language.
ORG Companies, agencies, institutions, etc.
FAC Buildings, airports, highways, bridges, etc.

> Who ?
PERSON People, including fictional. NORP Nationalities or religious or political groups.

> When ?
DATE Absolute or relative dates or periods.

> How long ?
TIME Times smaller than a day.

> Where ?
GPE Countries, cities, states.
LOC Non-GPE locations, mountain ranges, bodies of water.

> What ?
PRODUCT Objects, vehicles, foods, etc. (Not services.)

> How much ?
MONEY Monetary values, including unit.

> How many ?
QUANTITY Measurements, as of weight or distance.

> What percentage ?
PERCENT Percentage, including ”%“.
"""