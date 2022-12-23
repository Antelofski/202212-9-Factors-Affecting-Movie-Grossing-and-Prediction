# coding gbk
# -*-utf-8-*-
from time import sleep
import requests
import pandas as pd
from bs4 import BeautifulSoup


def appendColumns():
    for index, row in datasetDF.iterrows():
        datasetDF.loc[index, 'imdbRate'] = findRating(row["tconst"])
        datasetDF.loc[index, 'runtime'] = findRuntime(row["tconst"])
        datasetDF.loc[index, 'genres'] = findGenres(row["tconst"])
        datasetDF.loc[index, 'directors'] = findDirectors(row["tconst"])
        print(index)


def findRating(tconst):
    if tconst == '': return ''
    try:
        imdbRate = title_rating_df[title_rating_df['tconst'] == tconst]['averageRating'].values[0]
    except IndexError:
        imdbRate = ''
    return imdbRate

def findGenres(tconst):
    if tconst == '': return ''
    try:
        genres = title_basics_df[title_basics_df['tconst'] == tconst]['genres'].values
        genres = str(genres)
    except IndexError:
        genres = ''
    return genres

def findRuntime(tconst):
    if tconst == '': return ''
    try:
        runtime = title_basics_df[title_basics_df['tconst'] == tconst]['runtimeMinutes'].values[0]
    except IndexError:
        runtime = ''
    return runtime

def findDirectors(tconst):
    if tconst == '': return ''
    try:
        directors_id = title_crew_df[title_crew_df['tconst'] == tconst]['directors'].values
        directors = []
        for director_id in directors_id:
            directors.append(name_basics_df[name_basics_df['nconst'] == director_id]['primaryName'].values[0])
        directors = str(directors)
    except IndexError:
        directors = ''
    return directors

def saveAsCsv(path):
    datasetDF.to_csv(path, encoding='utf-8', index=False)

if __name__ == '__main__':
    datasetDF = pd.read_csv('crawl.dataset.csv')
    title_rating_df = pd.read_csv('title.ratings.tsv', sep='\t')
    name_basics_df = pd.read_csv('name.basics.tsv', sep='\t')
    title_basics_df = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
    title_crew_df = pd.read_csv('title.crew.tsv', sep='\t')
    print()
    appendColumns()
    saveAsCsv('combine.dataset.csv')
