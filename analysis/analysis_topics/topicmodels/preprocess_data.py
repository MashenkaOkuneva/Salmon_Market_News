import codecs
import os
import pandas as pd
from os import path


with codecs.open(path.join(path.dirname(__file__), 'stopwords_long.txt'),
                 'r', 'utf-8') as f:
    stp_long = set(f.read().splitlines())
with codecs.open(path.join(path.dirname(__file__), 'stopwords_short.txt'),
                 'r', 'utf-8') as f:
    stp_short = set(f.read().splitlines())
    
def read_dictionary(file):
    """This function reads in data from .txt file."""
    with codecs.open(file, 'r', 'utf-8-sig') as f:
        # spitlines() splits a string into a list, where each line is a list item.
        dictionary = f.read().splitlines()
        return set([d.lower().strip() for d in dictionary])
    
journalist_names = read_dictionary(os.getcwd() + '\\topicmodels\\journalist_names.txt')

# Load the bigrams from a csv file to the Dataframe.    
bigrams = pd.read_csv(os.getcwd() + '\\bigrams.csv', encoding = 'utf-8-sig', header = None)
# Create a list of bigrams
bigrams = list(bigrams[0])
# Create a list with bigrams as one word, e.g. 'labour_market'
bigrams_one_word = ['_'.join(bi.split(' ')) for bi in bigrams]

# Load the trigrams from a csv file to the Dataframe.
trigrams = pd.read_csv(os.getcwd() + '\\trigrams.csv', encoding = 'utf-8-sig', header = None)
# Create a list of trigrams
trigrams = list(trigrams[0])
# Create a list with trigrams as one word
trigrams_one_word = ['_'.join(tri.split(' ')) for tri in trigrams]

# Create a dictionary where the keys are bigrams, and the values are bigrams as one word
dic_bigrams = dict(zip(bigrams, bigrams_one_word))
# Create a dictionary where the keys are trigrams, and the values are trigrams as one word
dic_trigrams = dict(zip(trigrams, trigrams_one_word))

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
