import json

import re

#pip install newsapi-python
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='4422331d7100422b860fbce5a4f3bc69')

# pip install nltk

#import nltk
#nltk.download('cmudict')
from nltk.corpus import cmudict
NLTK_Cmudict = cmudict.dict()

import nltk.data
#nltk.download('punkt')

import sys
from io import StringIO

#pip install pandas
import pandas as pd

import numpy as np


#referred from https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word

def nsyl(word):
  return int([len(list(y for y in x if y[-1].isdigit())) for x in NLTK_Cmudict[word.lower()]][0])

#approximate back up approach, returns number of syllables in a word
def syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count

def fleschScore(text, ret_errors = False, OUTPUT = False):
    if text == None :
        return np.NaN

    text_parsed = parseText(text, NewsAPI=True, OUTPUT = OUTPUT)

    NOSy = 0 #Number of syllables in the text
    NOW = 0 #Number of words in the text
    NOS = len(text_parsed) #Number of sentences in the text

    if NOS == 0:
        return np.NaN

    errors = 0

    for sentence in text_parsed:
        NOW += len(sentence) #Number of words in the sentence

        for word in sentence:
            try:
                NOSy += nsyl(word)

            except Exception as e:
                #print(e)
                errors += 1
                if OUTPUT:
                    print("Error processing: \"{}\"".format(word))
                try: #if word not found in cmudict use approximation
                    NOSy += syllables(word)

                except Exception as e: #if string is invalid (a number, symbol, etc)
                    print("Error counting syllables in: \"{}\"".format(word))
                    #print(e)

    ASL = NOW / NOS
    ASW = NOSy / NOW
    RS = 206.835 - (1.015 * ASL) - (84.6 * ASW)

    # if RS <= 0:
    #     return np.NaN
    # if RS >= 100:
    #     return np.NaN
    if ret_errors:
        return (RS, errors)
    if OUTPUT:
        print(RS)
    return RS

if __name__ == "__main__":
    pass
