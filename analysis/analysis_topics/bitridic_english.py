# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 11:48:02 2019

@author: mOkuneva
"""
import os
import nltk
from itertools import chain
   
nltk.data.path.append(os.getcwd() + '\\nltk_data')



class BiTriDic():
    
    """
    This class creates a list of two-word and three-word collocations.
    """
        
    def __init__(self, doc):
        self.sents = [nltk.sent_tokenize(doc.replace(u'\ufeff', ''))]
            
    def tagger(self):
        def tag(sents):
            return list(chain.from_iterable([nltk.pos_tag(nltk.word_tokenize(s)) for s in sents]))
        self.sents = map(tag, self.sents)
        
    def bigr(self):
        def bi(sents):
            return [a[0] + ' ' + b[0] for (a,b) in nltk.bigrams(sents) if \
                (a[1] == 'JJ' or a[1] == 'NN' or a[1] == 'NNS' or a[1] == 'NNP' or a[1] == 'NNPS') and (b[1] == 'NN' or b[1] == 'NNS' or b[1] == 'NNP' or b[1] == 'NNPS')  and (a[0][0].isdigit() == False)]
        self.bigr = map(bi, self.sents)
        
    def trigr(self):
        # Patterns: AN, NN, AAN, ANN, NAN, NNN, NPrepN;
        # A stands for adjectives, N for nouns, and Prep for prepositions.
        def trigr(sents):
            return [a[0] + ' ' + b[0] + ' ' + c[0] for (a,b,c) in nltk.trigrams(sents) if \
                (a[1] == 'JJ' or a[1] == 'NN' or a[1] == 'NNS' or a[1] == 'NNP' or a[1] == 'NNPS') and (b[1] == 'NN' or b[1] == 'NNS' or b[1] == 'NNP' or b[1] == 'NNPS') and (c[1] == 'NN' or c[1] == 'NNS' or c[1] == 'NNP' or c[1] == 'NNPS')  or \
                (a[1] == 'JJ' or a[1] == 'NN' or a[1] == 'NNS' or a[1] == 'NNP' or a[1] == 'NNPS') and (b[1] == 'JJ') and (c[1] == 'NN' or c[1] == 'NNS' or c[1] == 'NNP' or c[1] == 'NNPS')  or \
                (a[1] == 'NN' or a[1] == 'NNS' or a[1] == 'NNP' or a[1] == 'NNPS') and (b[1] == 'IN') and (c[1] == 'NN' or c[1] == 'NNS' or c[1] == 'NNP' or c[1] == 'NNPS')]
        self.trigr = map(trigr, self.sents)
        