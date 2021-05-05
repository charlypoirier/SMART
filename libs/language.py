"""
All language-related variables and functions,
accessible from anywhere where this is imported.
"""

import spacy
from PyDictionary import PyDictionary

# Spacy model (sm=faster, trf=slower)
nlp = spacy.load("en_core_web_trf")

# English dictionnary
dictionary = PyDictionary()
