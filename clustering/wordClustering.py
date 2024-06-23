import io
import re
import string
import tqdm
import tensorflow as tf
from tensorflow.keras import layers
import spacy
import en_core_web_md
nlp = en_core_web_md.load()

doc = nlp("this is a sentence")
for token in doc:
    print(token.vector)