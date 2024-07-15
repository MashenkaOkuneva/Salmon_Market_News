# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 14:52:00 2021

@author: mokuneva
"""


import re
from string import punctuation

# import bi_tri_data with bigrams and trigrams
import bi_tri_data

class tokens():
    
    '''This class pre-processes a text and transforms it into a list of tokens.'''
    
    def __init__(self, text):
        self.doc = text
        
    def preprocess(self):
        # lower case the text
        text = self.doc.lower()

        # remove punctuation
        text = ''.join([c for c in text if c not in punctuation and c not in ['«', '»']])
        # remove non-alphabetic characters
        text = ''.join([c for c in text if c.isalpha() == 1 or c == ' '])
        # remove multiple whitespaces
        text = re.sub(r'\s{2,}', ' ', text)
        # add collocations
        for k, v in bi_tri_data.dic_bigrams.items():
            text = re.sub(k, v, text)
        for k, v in bi_tri_data.dic_trigrams.items():
            text = re.sub(k, v, text)
        # split the text into tokens
        self.words = text.split()
    
        return self.words
