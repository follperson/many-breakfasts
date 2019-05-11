#!/usr/bin/env python3
import pandas as pd
import markovify as mk
import nltk

def load_markov_model(fp):
    df = pd.read_excel(fp)
    df = df[df['related'] != 'Error']
    corpus = df['directions_cleaned'].tolist()

    line_level = '\n'.join(['\n'.join(eval(article)) for article in corpus])
    article_level = '\n'.join([' '.join(eval(article)) for article in corpus])

    line_level_model = mk.NewlineText(line_level, 4)
    article_level_model = mk.NewlineText(article_level, 5)
    recipe = [str(i) + ': ' + line_level_model.make_sentence() for i in range(5)]
    print(recipe)
    # print()
    # print(line_level_model.make_sentence())
    # print(line_level_model.make_sentence())
    # print(line_level_model.make_sentence())
    # print(line_level_model.make_sentence())
    print('_'*20)
    print(article_level_model.make_sentence())
    print(article_level_model.make_sentence())
    print(article_level_model.make_sentence())
    print(article_level_model.make_sentence())
    print(article_level_model.make_sentence())


if __name__ == '__main__':
    load_markov_model(r'C:\Users\Andrew Follmann\Documents\projects\random_breakfast\scraping\All Recipes_data scraping_best-sourced.xlsx')