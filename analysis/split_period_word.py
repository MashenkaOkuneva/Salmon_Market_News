# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 14:27:55 2022

@author: mOkuneva
"""

import re

def split_period_word(text):
    """ 
    This function splits the period and the word erroneously merged together.
    """
    # Create a dictionary where the keys are mistakes (the period and the word are merged
    # together) and values are the corresponding corrections.                
    replace_dic = dict()
    
    # A regular expression for the group where the first element is a word
    # followed by the period, and the second element is a word.  
    pat = r"(\b[a-zA-Z]+\.)([a-zA-Z]+\b)"
    to_replace = re.findall(pat, text)
    
    for rep in to_replace:
        # rep_before is a mistake
        rep_before = rep[0]+rep[1]
        # add an item to the dictionary where the value is the correction
        replace_dic[rep_before] = rep[0] + ' ' + rep[1]
    
    # Split the period and the word using the dictionary replace_dic.
    for word, repl in replace_dic.items():
        text = text.replace(word, repl)
        
    return(text)