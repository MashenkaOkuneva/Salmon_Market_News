# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 18:59:36 2023

@author: mOkuneva
"""
import string
import re
import codecs
import os
import pandas as pd

negate = ["cannot", "doesnt", "hasnt", "neither", "never", "none", "nor", "not", "nothing", "nowhere", "without", "rarely",
          "seldom", "despite", "no", "nobody"]

def negated(word):
    """
    Determine if preceding word is a negation word
    """
    if word.lower() in negate:
        return True
    else:
        return False
    
def _strip_punc(token):
    """
    Removes all trailing and leading punctuation
    """
    stripped = token.strip(string.punctuation)
    return stripped


def _remove_numbers(token):
    """
    Removes all numbers
    """
    if re.findall(r'[0-9-£$€\,]+', token) != []:
        if re.findall(r'[0-9-£$€\,]+', token)[0] == token:
            token = ''
    return token

contractions = {
    u"ain[\u2019\']t": u"is not",
    u"aren[\u2019\']t": u"are not",
    u"can[\u2019\']t": u"cannot",
    u"could[\u2019\']ve": u"could have",
    u"couldn[\u2019\']t": u"could not",
    u"didn[\u2019\']t": u"did not",
    u"doesn[\u2019\']t": u"does not",
    u"don[\u2019\']t": u"do not",
    u"hadn[\u2019\']t": u"had not",
    u"hasn[\u2019\']t": u"has not",
    u"haven[\u2019\']t": u"have not",
    u"he[\u2019\']d": u"he would",
    u"he[\u2019\']ll": u"he will",
    u"he[\u2019\']s": u"he is",
    u"how[\u2019\']d": u"how did",
    u"how[\u2019\']ll": u"how will",
    u"how[\u2019\']s": u"how is",
    u"i[\u2019\']d": u"i would",
    u"i[\u2019\']ll": u"i will",
    u"i[\u2019\']m": u"i am",
    u"i[\u2019\']ve": u"i have",
    u"isn[\u2019\']t": u"is not",
    u"it[\u2019\']d": u"it would",
    u"it[\u2019\']ll": u"it will",
    u"it[\u2019\']s": u"it is",
    u"let[\u2019\']s": u"let us",
    u"ma[\u2019\']am": u"madam",
    u"might[\u2019\']ve": u"might have",
    u"must[\u2019\']ve": u"must have",
    u"needn[\u2019\']t": u"need not",
    u"o[\u2019\']clock": u"of the clock",
    u"shan[\u2019\']t": u"shall not",
    u"she[\u2019\']d": u"she would",
    u"she[\u2019\']ll": u"she will",
    u"she[\u2019\']s": u"she is",
    u"should[\u2019\']ve": u"should have",
    u"shouldn[\u2019\']t": u"should not",
    u"that[\u2019\']d": u"that would",
    u"that[\u2019\']ll": u"that will",
    u"that[\u2019\']s": u"that is",
    u"there[\u2019\']d": u"there would",
    u"there[\u2019\']ll": u"there will",
    u"there[\u2019\']s": u"there is",
    u"they[\u2019\']d": u"they would",
    u"they[\u2019\']ll": u"they will",
    u"they[\u2019\']re": u"they are",
    u"they[\u2019\']ve": u"they have",
    u"wasn[\u2019\']t": u"was not",
    u"we[\u2019\']d": u"we would",
    u"we[\u2019\']ll": u"we will",
    u"we[\u2019\']re": u"we are",
    u"we[\u2019\']ve": u"we have",
    u"weren[\u2019\']t": u"were not",
    u"what[\u2019\']ll": u"what will",
    u"what[\u2019\']re": u"what are",
    u"what[\u2019\']s": u"what is",
    u"when[\u2019\']s": u"when is",
    u"where[\u2019\']d": u"where did",
    u"where[\u2019\']s": u"where is",
    u"where[\u2019\']ve": u"where have",
    u"who[\u2019\']ll": u"who will",
    u"who[\u2019\']s": u"who is",
    u"who[\u2019\']ve": u"who have",
    u"why[\u2019\']s": u"why is",
    u"won[\u2019\']t": u"will not",
    u"would[\u2019\']ve": u"would have",
    u"wouldn[\u2019\']t": u"would not",
    u"y[\u2019\']all": u"you all",
    u"you[\u2019\']d": u"you would",
    u"you[\u2019\']ll": u"you will",
    u"you[\u2019\']re": u"you are",
    u"you[\u2019\']ve": u"you have"
}

def read_dictionary(file):
    """This function reads in data from .txt file."""
    with codecs.open(file, 'r', 'utf-8-sig') as f:
        # spitlines() splits a string into a list, where each line is a list item.
        dictionary = f.read().splitlines()
        dictionary = [word for word in dictionary if word != '']
        return set([d.lower().strip() for d in dictionary])
    
path_to_file = os.getcwd() + '\\analysis_topics\\topicmodels'
fish_neg = read_dictionary(path_to_file + '\\keywords_neg_final.txt')
fish_pos = read_dictionary(path_to_file + '\\keywords_pos_final.txt')

sent_words = list(fish_neg) + list(fish_pos)

# Create the list of bigrams for sentiment 
bigrams_sent = [w for w in sent_words if len(w.split()) == 2]
# Create a list with bigrams as one word, e.g. 'labour_market'
bigrams_one_word = ['_'.join(bi.split(' ')) for bi in bigrams_sent]

# Create the list of trigrams for sentiment 
trigrams_sent = [w for w in sent_words if len(w.split()) == 3]
# Create a list with trigrams as one word
trigrams_one_word = ['_'.join(tri.split(' ')) for tri in trigrams_sent]

# Create the list of fourgrams for sentiment 
fourgrams_sent = [w for w in sent_words if len(w.split()) == 4]
# Create a list with fourgrams as one word
fourgrams_one_word = ['_'.join(four.split(' ')) for four in fourgrams_sent]

# Create a dictionary where the keys are bigrams, and the values are bigrams as one word
dic_bigrams = dict(zip(bigrams_sent, bigrams_one_word))
# Create a dictionary where the keys are trigrams, and the values are trigrams as one word
dic_trigrams = dict(zip(trigrams_sent, trigrams_one_word))
# Create a dictionary where the keys are fourgrams, and the values are fourgrams as one word
dic_fourgrams = dict(zip(fourgrams_sent, fourgrams_one_word))

# Create a list of negative words
fish_neg = list(fish_neg)
# Create a list with bigrams/tirgrams/fougrams as one word, e.g. 'labour_market'
fish_neg = ['_'.join(neg.split(' ')) for neg in fish_neg]

# Create a list of positive words
fish_pos = list(fish_pos)
# Create a list with bigrams/tirgrams/fougrams as one word, e.g. 'labour_market'
fish_pos = ['_'.join(pos.split(' ')) for pos in fish_pos]

# Read an Excel file
dict_LM = pd.read_excel('Loughran-McDonald_MasterDictionary_1993-2021.xlsx',  usecols = "A,H,I")
neg = list(dict_LM[(dict_LM.Negative != 0) & (dict_LM.Negative != -2020)]['Word'])
pos = list(dict_LM[(dict_LM.Positive != 0) & (dict_LM.Positive != -2020)]['Word'])

neg = ['FALSE' if word == False else word for word in neg]
neg = [word.lower() for word in neg]
pos = [word.lower() for word in pos]

neg_combine = neg+fish_neg
pos_combine = pos+fish_pos


def tone_with_negation(article, sent_dict, bitrigrams = True):
    """
    Count positive and negative words with negation check. Account for simple negation for positive and negative words.
    Simple negation is taken to be observations of one of negate words occurring within three words
    preceding a positive or negative word.
    """
    
    if sent_dict == 0:
        neg_dict = neg
        pos_dict = pos
    elif sent_dict == 1:
        neg_dict = fish_neg
        pos_dict = fish_pos
    elif sent_dict == 2:
        neg_dict = neg_combine
        pos_dict = pos_combine
        
    pos_count = 0
    neg_count = 0
 
    pos_words = []
    neg_words = []
    
    article = re.sub('No\.', 'Number', article)
    for k,v in contractions.items():
        article = re.sub(k,v,article)
        
    article = article.lower()
    
    if bitrigrams:
        for k, v in dic_fourgrams.items():
            article = re.sub(k, v, article)
        for k, v in dic_trigrams.items():
            article = re.sub(k, v, article)
        for k, v in dic_bigrams.items():
            article = re.sub(k, v, article)
    
    input_words = article.split()
    input_words = list(map(_strip_punc, input_words))
    input_words = list(map(_remove_numbers, input_words))
    input_words = [w for w in input_words if w != '']
 
    word_count = len(input_words)
 
    for i in range(0, word_count):
        if input_words[i] in neg_dict:
            if i >= 3:
                if negated(input_words[i - 1]) or negated(input_words[i - 2]) or negated(input_words[i - 3]):
                    pos_count += 1
                    pos_words.append(input_words[i] + ' (with negation)')
                else:
                    neg_count += 1
                    neg_words.append(input_words[i])
            elif i == 2:
                if negated(input_words[i - 1]) or negated(input_words[i - 2]):
                    pos_count += 1
                    pos_words.append(input_words[i] + ' (with negation)')
                else:
                    neg_count += 1
                    neg_words.append(input_words[i])
            elif i == 1:
                if negated(input_words[i - 1]):
                    pos_count += 1
                    pos_words.append(input_words[i] + ' (with negation)')
                else:
                    neg_count += 1
                    neg_words.append(input_words[i])
            elif i == 0:
                neg_count += 1
                neg_words.append(input_words[i])
        if input_words[i] in pos_dict:
            if i >= 3:
                if negated(input_words[i - 1]) or negated(input_words[i - 2]) or negated(input_words[i - 3]):
                    neg_count += 1
                    neg_words.append(input_words[i] + ' (with negation)')
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 2:
                if negated(input_words[i - 1]) or negated(input_words[i - 2]):
                    neg_count += 1
                    neg_words.append(input_words[i] + ' (with negation)')
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 1:
                if negated(input_words[i - 1]):
                    neg_count += 1
                    neg_words.append(input_words[i] + ' (with negation)')
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 0:
                pos_count += 1
                pos_words.append(input_words[i])
 
    sentiment = (pos_count-neg_count)/word_count
 
    return sentiment