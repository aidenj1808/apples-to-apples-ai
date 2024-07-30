import spacy
from collections import defaultdict

# Ensure that "python -m spacy download en_core_web_md" has been used before running this file
nlp = spacy.load("en_core_web_md")

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

def get_adj_associations(adjective, which='all'):
    associations = defaultdict(dict)
    if which == 'all':
        nouns = read_words_from_file('src/all_red_cards.csv')  # Adjust path if necessary
    else:
        nouns = which
    adj_doc = nlp(adjective)
    for noun in nouns:
        noun_doc = nlp(noun)
        similarity = adj_doc.similarity(noun_doc)
        associations[adjective][noun] = similarity
    return associations

def get_noun_associations(noun, which='all'):
    associations = defaultdict(dict)
    if which == 'all':
        adjectives = read_words_from_file('src/all_green_cards.csv')  # Adjust path if necessary
    else:
        adjectives = which
    noun_doc = nlp(noun)
    for adjective in adjectives:
        adj_doc = nlp(adjective)
        similarity = noun_doc.similarity(adj_doc)
        associations[adjective][noun] = similarity
    return associations

def get_all_associations(nouns=None, adjectives=None):
    associations = defaultdict(dict)
    if nouns is None:
        nouns = read_words_from_file('src/all_red_cards.csv')  # Adjust path if necessary
    if adjectives is None:
        adjectives = read_words_from_file('src/all_green_cards.csv')  # Adjust path if necessary
    for adjective in adjectives:
        adj_doc = nlp(adjective)
        for noun in nouns:
            noun_doc = nlp(noun)
            similarity = adj_doc.similarity(noun_doc)
            associations[adjective][noun] = similarity
    return associations

