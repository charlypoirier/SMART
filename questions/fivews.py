import spacy
from classes.question import Question
from libs.language import *

"""
Questions à réponses courtes

Ce qui serait bien, ce serait de générer un résumé du
texte (Aziz?) et utiliser le résumé comme entrée pour
générer des questions avec le code ci-dessous.
"""

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
    if token.dep_ == "dobj" or (token.dep_=="attr" and token.pos_=="NOUN"):
      dobj_token=token
      return flatten_tree(dobj_token.subtree)

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
  while (parent.pos_ !="VERB" and parent.pos_!= "AUX"):
    parent=parent.head
  verb_list=extract_Verb(parent)
  if (len(verb_list)==2 and verb_list[0].pos_=="AUX" and verb_list[1].pos_=="VERB"):
    return Question("when "+str(verb_list[0])+" "+str(find_subj_of(verb_list))+" "+str(verb_list[1])+" "+str(find_obj_of(verb_list)),[token_date.text],0)

def generate_where(doc,token_place):
  parent= token_place.head
  while (parent.pos_ !="VERB" and parent.pos_!= "AUX"):
    parent=parent.head
  verb_list=extract_Verb(parent)
  place_found=False
  for token in token_place.rights :
    if (token.pos_=="NOUN"):
      place_found=True
  if (token_place.head.pos_ =="VERB" and place_found==True):
    if (len(verb_list)==2 and verb_list[0].pos_=="AUX" and verb_list[1].pos_=="VERB"):
      if ( verb_list[1].tag_=="VBG"):
        return Question("where "+str(verb_list[0])+" "+str(find_subj_of(verb_list))+" "+str(verb_list[1]),[token_place],0)
    elif (len(verb_list)==1 and (verb_list[0].pos_=="VERB" or verb_list[0].lemma_=="have") ):
      if ( verb_list[0].tag_=="VBD"): #passé
        return Question("where "+"did "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[token_place.text],0)
      elif ( verb_list[0].tag_=="VBZ"): #3eme personne present
        return Question("where "+"does "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[token_place.text],0)
      elif (verb_list[0].tag_=="VBP"): #present !=3eme personne
        return Question("where "+"do "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[token_place.text],0)

def generate_how(doc,token):
  parent= token.head
  #while (parent.pos_ !="VERB" and parent.pos_!="AUX"):
   # parent=parent.head
  if (parent.pos_ =="VERB" or parent.pos_=="AUX" ): 
    verb_list=extract_Verb(parent)
    if (len(verb_list)==1 and verb_list[0].pos_=="VERB" ): #au present
      if (verb_list[0].tag_=="VBZ"):
        return Question("how "+"does" +" "+str(find_subj_of(verb_list))+ " "+str(verb_list[0].lemma_),[token.text],0)
      else :
        return Question("how "+"do" +" "+str(find_subj_of(verb_list))+ " "+str(verb_list[0].lemma_),[token.text],0)
    elif (len(verb_list)==1 and verb_list[0].pos_=="AUX" ): #au present
      return Question("how "+str(verb_list[0])+" "+str(find_subj_of(verb_list)),[" "],0)
  
def generate_who(doc,token):
  parent= token.head
  #while (parent.pos_ !="VERB" and parent.pos_!="AUX"):
   # parent=parent.head
  if (parent.pos_ =="VERB" or parent.pos_=="AUX" ): 
    verb_list=extract_Verb(parent)
    if (len(verb_list)==1 ): 
        return Question("who "+str(verb_list[0])+ " "+str(find_obj_of(verb_list)),[token.text],0)

def generate_what(doc,token):
  parent= token.head
  stop_cpt=0
  while (parent.pos_ !="VERB" and parent.pos_!= "AUX" and stop_cpt<5):
    parent=parent.head
    stop_cpt=stop_cpt+1
  verb_list=extract_Verb(parent)
  if (len(verb_list)==2 and verb_list[0].pos_=="AUX" and verb_list[1].pos_=="VERB"):
    if ( verb_list[1].tag_=="VBG"):
      return Question("what "+str(verb_list[0])+" "+str(find_subj_of(verb_list))+" "+str(verb_list[1]),[token.text],0)
  elif (len(verb_list)==1 and (verb_list[0].pos_=="VERB" or verb_list[0].lemma_=="have")  ):
    if ( verb_list[0].tag_=="VBD"): #passé
      return Question("what "+"did "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[token.text],0)
    elif ( verb_list[0].tag_=="VBZ"): #3eme personne present
      return Question("what "+"does "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[token.text],0)
    elif (verb_list[0].tag_=="VBP"): #present !=3eme personne
      return Question("what "+"do "+str(find_subj_of(verb_list))+" "+str(verb_list[0].lemma_),[token.text],0)
  elif (len(verb_list)==1 and verb_list[0].pos_=="AUX" ):
      return Question("what "+str(verb_list[0])+" "+str(find_subj_of(verb_list)),[token.text],0)

def linked_to(token,list_pos):
  for rtoken in token.rights:
    if rtoken.pos_ in list_pos:
      return True


def generate_wh(text):
    #document = nlp(text_rank_algorithm(text)).sents  <- uncomment for the extraction of important sentences only
    document = nlp(text).sents
    #summary_array=generate_summary_array(document)
    document = extract_clauses(document)
    #document = preprocessing(document)
    #document=document.union(set(summary_array))
    questions = set()
    for sentence in document:
        for token in nlp(sentence):
            if (str(token) == "in"):
                question = generate_where(document,token)
                if(question is not None):
                    question.stem = question.stem + '?'
                    questions.add(question)
            if (token.ent_type_=="DATE"):
                question = generate_when(document,token)
                if(question is not None):
                    question.stem = question.stem + '?'
                    questions.add(question)
            if ((token.dep_=="dobj" and token.pos_!="PRON") or (token.dep_=="attr" and token.pos_=="NOUN")):
                question = generate_what(document,token)
                if(question is not None):
                    question.stem = question.stem + '?'
                    questions.add(question)
            if (token.pos_=="ADJ"):
                question = generate_how(document,token)
                if(question is not None):
                    question.stem = question.stem + '?'
                    questions.add(question)
            if ((token.pos_=="PROPN" or linked_to(token,["PROPN"])) and token.dep_=="nsubj"):
                question = generate_who(document,token)
                if(question is not None):
                    question.stem = question.stem + '?'
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

            question.stem = question.stem + '?'
            questions.add(question)

    return questions
