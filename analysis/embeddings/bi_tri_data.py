import os
import pandas as pd


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

