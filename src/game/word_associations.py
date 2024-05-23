import spacy
from collections import defaultdict

#This file contains functions related to using Spacy for natural language
#processing in order to find word associations

#Ensure that "python -m spacy download en_core_web_md" has been used before
#running this file

#Get words from file supplied
def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

'''
calculate associations between given adjective and specified nouns.
If which not supplied, defaults to all possible nouns.
Which should be a list of strings if supplied.
RETURN: dictionary with adjectives as keys. Each key then has a dictionary
with nouns as keys with their similarity values.
'''
def get_adj_associations(adjective, which='all'):

     #Load English tokenizer, tagger, parser, and word vectors
    nlp = spacy.load("en_core_web_md")
    #Create a defaultdict to store associations
    associations = defaultdict(dict)

    #Get associations of all nouns with the supplied adjective
    if which == 'all':
        #Read all adjectives and nouns from files
        nouns = read_words_from_file('../red_deck.txt')


    #Get associations of specified nouns with the supplied adjectives
    else:
        nouns = which

    for noun in nouns:
            similarity = nlp(adjective).similarity(nlp(noun))
            associations[adjective][noun] = similarity

    return associations

'''
calculate associations between given noun and specified adjectives.
If which not supplied, defaults to all possible adjectives.
Which should be a list of strings if supplied.
RETURN: dictionary with adjectives as keys. Each key then has a dictionary
with nouns as keys with their similarity values.
'''
def get_noun_associations(noun, which='all'):

     #Load English tokenizer, tagger, parser, and word vectors
    nlp = spacy.load("en_core_web_md")
    #Create a defaultdict to store associations
    associations = defaultdict(dict)

    #Get associations of all nouns with the supplied adjective
    if which == 'all':
        #Read all adjectives from file
        adjectives = read_words_from_file('../green_deck.txt')


    #Get associations of specified adjectives with the supplied adjectives
    else:
        adjectives = which

    for adjective in adjectives:
            similarity = nlp(adjective).similarity(nlp(noun))
            associations[adjective][noun] = similarity

    return associations

'''
Calculate all possible associations between nouns and adjectives.
If both arguments are None, then all words from list are compared.
NOTE: If the above condition occurs, this will take a very long time.
Otherwise, calculate associations between the supplied nouns and adjectives.
Both should be lists of strings if supplied.
RETURN: dictionary with adjectives as keys. Each key then has a dictionary
with nouns as keys with their similarity values.
'''
def get_all_associations(nouns=None, adjectives=None):

    nlp = spacy.load("en_core_web_md")

    associations = defaultdict(dict)

    #if nouns is none, then get all nouns from file
    if nouns is None:
        nouns = read_words_from_file('../red_deck.txt')

    #if adjectives is none, then get all adjectives from file
    if adjectives is None:
        adjectives = read_words_from_file('../green_deck.txt')

    #check similarties between adjectives and nouns
    for adjective in adjectives:
        for noun in nouns:
            similarity = nlp(adjective).similarity(nlp(noun))
            associations[adjective][noun] = similarity

    return associations
