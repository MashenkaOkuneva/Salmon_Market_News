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
  - Estimation of a word2vec model for generating embeddings, which aid in creating our sentiment dictionary: [Word_embeddings notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/embeddings/Word_embeddings.ipynb), [Synonyms_based_on_embeddings notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/embeddings/Synonyms_based_on_embeddings.ipynb).
  - Lexicon-based sentiment analysis utilizing both the Loughran-McDonald and our extended dictionaries: ['Sentiment analysis' notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/Sentiment%20analysis.ipynb), [added positive words](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/topicmodels/keywords_pos_final.txt), [added negative words](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/topicmodels/keywords_neg_final.txt).
  - Identification of competitors for the five firms whose stock returns are analysed: [FindCompetitors notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/FindCompetitors.ipynb).
  - Estimation of the Latent Dirichlet Allocation (LDA) topic model and visualization of the estimated topics: [LDA notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/LDA.ipynb), [Collocations notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Collocations.ipynb), [Cross-validation notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Cross-validation.ipynb), [Find_topic_articles notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Find_topic_articles.ipynb), ['Perplexity train set' notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Perplexity%20train%20set.ipynb), [Wordclouds notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/Wordclouds.ipynb), [Figures notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/Figures.ipynb), [LDA_forecasting notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/analysis_topics/LDA_forecasting.ipynb).
  - Performing Vector Autoregression (VAR) and Principal Component Analysis (PCA) to explore the principal components and dynamic relationships in the data: [PCA script](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/VAR/PCA.m), [VAR script](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/VAR/estimate_VAR.m).
  - An out-of-sample forecasting experiment aimed at predicting stock market direction: [Forecasting_exercise notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/analysis/forecasting/Forecasting_exercise.ipynb).
- **[finance data](https://github.com/MashenkaOkuneva/Salmon_Market_News/tree/master/finance%20data)**: This directory contains scripts that process and analyse financial data related to the study. It includes:
  - Calculation and visualisation of investor reactions: [Investors_reaction notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/finance%20data/Investors_reaction.ipynb).
  - Assignment of dates to articles based on their potential impact on stock markets, rather than publication dates: [daily_articles notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/finance%20data/daily_articles.ipynb).
  - Combining financial data with sentiment scores, estimated topics, and extracted components for PCA and VAR analyses: ["Combine the datasets for VAR analysis" notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/finance%20data/Combine%20the%20datasets%20for%20VAR%20analysis.ipynb).
  - Preparation of all the data necessary for the out-of-sample forecasting exercise: [Data for forecasting notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/finance%20data/Data%20for%20forecasting.ipynb).
- **[robustness_check](https://github.com/MashenkaOkuneva/Salmon_Market_News/tree/master/robustness_check)**: Includes the ['Combine datasets' notebook](https://github.com/MashenkaOkuneva/Salmon_Market_News/blob/master/robustness_check/Combine%20datasets.ipynb) that prepares the dataset for the robustness check, where we run a VAR model featuring three variables: components based on topics multiplied with extended sentiment, the log return of the SPI, and the log return of the Oslo Stock Exchange (OSE).

## Project Environment Setup

### Python Versions and Environment Setup
This project uses three separate Python environments to accommodate different requirements: two Python 3 environments—one with GPU support and one without—and a Python 2 environment.

- **Python 2 Environment**: For notebooks that require Python 2 (`LDA.ipynb`, `Collocations.ipynb`, `Cross-validation.ipynb`, `LDA_forecasting.ipynb`), set up your environment using the `py2_env.yml` file available in this repository.
- **Python 3 Environment (GPU support)**: This environment can be set up using the `py3_env_gpu.yml` file and is used for the estimation of word embeddings in the `Word_embeddings.ipynb` notebook.
- **Python 3 Environment (No GPU support)**: This environment can be set up using the `py3_env.yml` file and is used for all other notebooks.

### System Requirements
The code was run on a server equipped with the following specifications for optimal performance:
- **CPU**: 8-core 3.7 GHz AMD Ryzen 7 2700X
- **GPU**: NVIDIA GeForce RTX 2080 Ti
- **Memory**: 64 GB RAM
- **Operating System**: Windows Server 2022 Standard

## Usage and Citation
Feel free to use the code provided in this repository for your research or projects. If you utilize this code, please cite the paper: Knoppe C., Okuneva M., & Zitti M. (2025). Salmon stock returns around market news. Marine Resource Economics, 40(2).

## Contact
If you have any questions about this repository or the related research, please feel free to contact Clemens Knoppe [knoppe@economics.uni-kiel.de](mailto:knoppe@economics.uni-kiel.de), Mariia Okuneva [miokuneva2@gmail.com](mailto:miokuneva2@gmail.com), or Mikaella Zitti [mikaella.zitti@nmbu.no](mailto:mikaella.zitti@nmbu.no).


