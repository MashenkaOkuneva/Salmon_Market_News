# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 15:17:17 2022

@author: mOkuneva
"""

import topicmodels

def cross_val(data):
    """
    Perform cross-validation to find an optimal K.
    Output perplexity for a particular fold.
    """
    # Initialize an LDA object using the LDA class. 
    # A list of stems from the train set (data[0]) is an input.
    # The number of topics is data[2].
    ldaobj = topicmodels.LDA.LDAGibbs(data[0],data[2])
    # Sampling: 500 is the number of burn-in iterations; 50 is a thinning interval; 
    # 150 is the number of samples to take.
    ldaobj.sample(500,50,150)
    # Keep the last 80 samples corresponding to 4000 iterations where the chain has converged.
    ldaobj.samples_keep(80)
    # Re-sample document-specific topic proportions for the test data (data[1])
    # using 20 iterations of Gibbs sampler.
    queryobj = topicmodels.LDA.QueryGibbs(data[1],ldaobj.token_key,ldaobj.tt)
    queryobj.query(20)
    # The final perplexity is the average over 80 samples.
    perplexity = queryobj.perplexity().mean()
    return(perplexity)    
    