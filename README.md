# Spotify API: EDA and ML - What Variables are Associated with Song Popularity
## Abstract
These collections of Jupyter Notebooks set out to answer the research question: "What variables are associated with song popularity?"

## Notebooks
- **01_introduction.ipynb**: Introduction to the project.
- **02_scraping_random_samp.ipynb**: Scrapes 1000 random songs form random-song.com using Selenium and Beautiful Soup.
- **03_spotify_api.ipynb**: Uses the Spotify API to develop a databse containing the random sample of 1000 songs and their variables.
- **04_eda_.iptnb**: An exploratory data analysis conducted on the song database.

## Data
There were two stages of data collection:
- **Collecting Random Songs**: In 02_scraiping_random_samp.ipynb, 1000 songs were scraped from random-song.com.
- **Collecting Spotify Songs**: The songs were passed to the Spotify API, which provided the variables necessary for an ML model.

## Cleaning
- **Missing Values**: There were missing values in rand_samp, which were cleaned.
- **Normalization**: Variables were normalized for the K-means Clustering.
- **General Cleaning**: General cleaning was necessary to use the scraped data.

## Initial Issues
Originally, as seen in Final.py, 500 songs were scraped from Rolling Stone's Top 500 Songs of All Time list. Afterwords, it became clear that the outcome variable of the intended ML algorithm is popularity -- having a dataset solely containing popular songs would make the model less accurate. The scraping approach above was adopted instead.
