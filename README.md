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
  - Lexicon-based sentiment analysis utilizing both the Loughran-McDonald and our extended dictionaries.
  - Identification of competitors for the five firms whose stock returns are analysed.
  - Estimation of the Latent Dirichlet Allocation (LDA) topic model and visualization of the estimated topics.
  - Performing Vector Autoregression (VAR) and Principal Component Analysis (PCA) to explore the principal components and dynamic relationships in the data.
  - An out-of-sample forecasting experiment aimed at predicting stock market direction.
