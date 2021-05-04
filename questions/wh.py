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
    question = question.replace('to who', 'to whom')
    question = question.replace('of who', 'of whom')
    question = question.replace('with who', 'with whom')
    return Question(question, [entity.text], 0)

def when(sentence, entity):
    # question = "When " + adverb + subject + verb + compl ?
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
def flatten_tree(tree):
  return ''.join([token.text_with_ws for token in list(tree)]).strip()

def find_subj_of(verb_list):
  if (len(verb_list)==1):
    verb=verb_list[0]
  elif (len(verb_list)>=2):
    verb=verb_list[-1]
  for token in verb.lefts:
    if token.dep_ == "nsubj":
      nsubj_token=token
      return flatten_tree(nsubj_token.subtree)
      
  


def list_of_token_to_str(list_token):
  res=""
  for token in list_token:
    res=res+str(token)+" "
  return res

def find_obj_of(verb_list):
  if (len(verb_list)==1):
    verb=verb_list[0]
  elif (len(verb_list)>=2):
    verb=verb_list[-1]
  for token in verb.rights:
    if token.dep_ == "dobj":
      return token

def extract_Verb(token):
  verb_phrase=[]
  verb_phrase.append(token)
  left_phrase=[]
  for leftchild in token.lefts:
      if (leftchild.dep_=="auxpass" or leftchild.dep_=="aux"):
        left_phrase.insert(0,leftchild)
  verb_phrase=left_phrase+verb_phrase
  return verb_phrase

def generate_when(doc,token_date):
  parent= token_date.head
  while parent.pos_ !="VERB":
    parent=parent.head
  verb_list=extract_Verb(parent)
  if (len(verb_list)==2 and verb_list[0].pos_=="AUX" and verb_list[1].pos_=="VERB"):
    return Question("when "+str(verb_list[0])+" "+str(find_subj_of(verb_list))+" "+str(verb_list[1])+" "+str(find_obj_of(verb_list)),[" "],0)

def generate_where(doc,token_place):
  parent= token_place.head
  while parent.pos_ !="VERB":
    parent=parent.head
  verb_list=extract_Verb(parent)
  place_found=False
  for token in token_place.rights :
    if (token.pos_=="NOUN"):
      place_found=True
  if (token_place.head.pos_ =="VERB" and place_found==True):
    return Question("where do "+str(find_subj_of(verb_list))+" "+list_of_token_to_str(verb_list),[" "],0)

def generate_how(doc,token):
  parent= token.head
  #while (parent.pos_ !="VERB" and parent.pos_!="AUX"):
   # parent=parent.head
  if (parent.pos_ =="VERB" or parent.pos_=="AUX" ): 
    verb_list=extract_Verb(parent)
    if (len(verb_list)==1 and verb_list[0].pos_=="VERB" ): #au present
      if (verb_list[0].tag_=="VBZ"):
        return Question("how "+"does" +" "+str(find_subj_of(verb_list))+ " "+str(verb_list[0].lemma_),[" "],0)
      else :
        return Question("how "+"do" +" "+str(find_subj_of(verb_list))+ " "+str(verb_list[0].lemma_),[" "],0)
    elif (len(verb_list)==1 and verb_list[0].pos_=="AUX" ): #au present
      return Question("how "+str(verb_list[0])+" "+str(find_subj_of(verb_list)),[" "],0)
  

def generate_what(doc,token):
  parent= token.head
  while parent.pos_ !="VERB":
    parent=parent.head
  verb_list=extract_Verb(parent)
  if (len(verb_list)==2 and verb_list[0].pos_=="AUX" and verb_list[1].pos_=="VERB"):
    if ( verb_list[1].tag_=="VBG"):
      return Question("what "+str(verb_list[0])+" "+str(find_subj_of(verb_list))+" "+str(verb_list[1]) ,[" "],0)
  elif (len(verb_list)==1 and verb_list[0].pos_=="VERB" ):
    if ( verb_list[0].tag_=="VBD"): #passé
      return Question("what "+"did "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[" "],0)
    elif ( verb_list[0].tag_=="VBZ"): #3eme personne present
      return Question("what "+"does "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[" "],0)
    elif (verb_list[0].tag_=="VBP"): #present !=3eme personne
      return Question("what "+"do "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[" "],0)


def generate_wh(text):
    document = nlp(text)
    questions = set()
    for sentence in document.sents:
        for token in sentence:
            if (str(token) == "in"):
                question = generate_where(document,token)
                if( question is not None):
                    questions.add(question)
            if (token.ent_type_=="DATE"):
                question = generate_when(document,token)
                if( question is not None):
                    questions.add(question)
            if (token.dep_=="dobj"):
                question = generate_what(document,token)
                if( question is not None):
                    questions.add(question)
            if (token.pos_=="ADJ"):
                question = generate_how(document,token)
                if( question is not None):
                    questions.add(question)

    return questions

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

            question.stem = question.stem.replace('.', '?')
            question.stem = question.stem.capitalize()
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
ORG Companies, agencies, institutions, etc.

> Unsupported
ORDINAL “first”, “second”, etc.
CARDINAL Numerals that do not fall under another type.
EVENT Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART Titles of books, songs, etc.
LAW Named documents made into laws.
LANGUAGE Any named language.
TIME Times smaller than a day.
PERCENT Percentage, including ”%“.
"""