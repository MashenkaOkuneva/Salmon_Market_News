# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 21:45:10 2022

@author: mOkuneva
"""

import spacy
eng_model = spacy.load("en_core_web_sm")

def identify_names(text):
    """ 
    This function retrieves names of people using an english model from spacy.
    """   
    # Process a text using the spacy model
    text_spacy = eng_model(text)
    
    # The list of identifies names
    names = []
    
    # If the identified entity is a 'PERSON', then add the name to the list
    for ent in text_spacy.ents:
        if ent.label_ == 'PERSON':
            names.append(ent.text)        
    return(names)