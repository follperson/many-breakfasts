#!/usr/bin/env python3
import pandas as pd
import markovify as mk
import nltk


def load_markov_model(fp,col,kind='list'):
    df = pd.read_excel(fp)
    # filter these
    df = df[df['related'] != 'Error']
    corpus = df[col].tolist()
    if kind =='list':
        line_level = '\n'.join(['\n'.join(eval(article)) for article in corpus])
        article_level = '\n'.join([' '.join(eval(article)) for article in corpus])
        line_level_model = mk.NewlineText(line_level, 4)
        recipe = [str(i) + ': ' + line_level_model.make_sentence() for i in range(1,6)]
        print('\n'.join(recipe))
    else:
        corpus = df[col].tolist()
        line_level = '\n'.join(corpus)
        article_level = '\n'.join(corpus)
        line_level_model = mk.Text(line_level, 4)
    with open('corpus\\' + col + ' - line level.txt', 'w') as fo:
        fo.write(line_level)
    with open('corpus\\' + col + ' - article level.txt', 'w') as fo:
        fo.write(article_level)

    article_level_model = mk.NewlineText(article_level, 4)

    print()
    print(line_level_model.make_sentence())
    print(line_level_model.make_sentence())
    print(line_level_model.make_sentence())
    print(line_level_model.make_sentence())
    print('_'*20)
    print(article_level_model.make_sentence())
    print(article_level_model.make_sentence())
    print(article_level_model.make_sentence())
    print(article_level_model.make_sentence())
    print(article_level_model.make_sentence())

    return line_level_model, article_level_model


def main():
    load_descriptions()
    load_directions()


def load_directions():
    load_markov_model(r'scraping\full_breakfast\All Recipes_data scraping_best-sourced.xlsx', 'directions_cleaned')


def load_descriptions():
    load_markov_model(r"scraping\full_breakfast\All Recipes Breakfast_data scraping_1558975838.xlsx",'description','str')

if __name__ == '__main__':

    main()