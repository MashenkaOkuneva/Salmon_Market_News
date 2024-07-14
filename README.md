# Salmon stock returns around market news

## Overview

This repository contains the code necessary to replicate the main results of the paper "Salmon Stock Returns Around Market News" by Clemens Knoppe, Mariia Okuneva, and Mikaella Zitti. It includes scripts for:
- Scraping articles from IntraFish.
- Pre-processing text and financial data.
- Estimating an LDA model for topic modeling and a word2vec model for embeddings.
- Performing lexicon-based sentiment analysis using both the Loughran-McDonald (LM) dictionary and our extended dictionary.
- Conducting Principal Component Analysis (PCA) and Vector Autoregression (VAR) analysis.
- An out-of-sample forecasting exercise aimed at predicting stock market direction.

## Repository Structure

The repository is structured into various directories, each serving a distinct purpose aligned with the paper's methodologies:

- **[scraping](https://github.com/MashenkaOkuneva/Salmon_Market_News/tree/master/scraping)**: Contains the scripts used for web scraping articles from [IntraFish](https://www.intrafish.com/). It also includes the code for dividing blog posts into individual entries based on their posting times and visualizing the monthly distribution of article counts. Due to copyright restrictions, only a sample of five articles is provided for demonstration.
- **[analysis](https://github.com/MashenkaOkuneva/Salmon_Market_News/tree/master/analysis)**: Contains the scripts and results for the detailed analysis outlined in the study. This includes:
  - Text data pre-processing: [read_txt_sorting_ts notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/read_txt_sorting_ts.ipynb).
  - Estimation of a word2vec model for generating embeddings, which aid in creating our sentiment dictionary.
  - Lexicon-based sentiment analysis utilizing both the Loughran-McDonald and our extended dictionaries: ['Sentiment analysis' notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/Sentiment%20analysis.ipynb), [added positive words](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/topicmodels/keywords_pos_final.txt), [added negative words](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/topicmodels/keywords_neg_final.txt).
  - Identification of competitors for the five firms whose stock returns are analysed: [FindCompetitors notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/FindCompetitors.ipynb).
  - Estimation of the Latent Dirichlet Allocation (LDA) topic model and visualization of the estimated topics: [LDA notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/LDA.ipynb), [Collocations notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Collocations.ipynb), [Cross-validation notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Cross-validation.ipynb), [Find_topic_articles notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Find_topic_articles.ipynb), ['Perplexity train set' notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Perplexity%20train%20set.ipynb), [Wordclouds notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Wordclouds.ipynb), [Figures notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/Figures.ipynb), [LDA_forecasting notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/LDA_forecasting.ipynb).
  - Performing Vector Autoregression (VAR) and Principal Component Analysis (PCA) to explore the principal components and dynamic relationships in the data.
  - An out-of-sample forecasting experiment aimed at predicting stock market direction.
- **[finance data](https://github.com/MashenkaOkuneva/Salmon_Market_News/tree/master/finance%20data)**: This directory contains scripts that process and analyse financial data related to the study. It includes:
  - Calculation and visualisation of investor reactions: [Investors_reaction notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/finance%20data/Investors_reaction.ipynb).
  - Assignment of dates to articles based on their potential impact on stock markets, rather than publication dates: [daily_articles notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/finance%20data/daily_articles.ipynb).
  - Combining financial data with sentiment scores, estimated topics, and extracted components for PCA and VAR analyses: ["Combine the datasets for VAR analysis" notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/finance%20data/Combine%20the%20datasets%20for%20VAR%20analysis.ipynb).
  - Preparation of all the data necessary for the out-of-sample forecasting exercise: [Data for forecasting notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/finance%20data/Data%20for%20forecasting.ipynb).
