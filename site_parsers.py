#!/usr/bin/env python3
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

__author__ = 'Andrew Follmann'
__date__ = ''
__version__ = '0.0.1'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}


# self.search_tags = {'name':'article','attrs':{'class':'fixed-recipe-card'}}


class AbsractRecipes(object):
    def __str__(self):
        return 'Recipe Site Scraper for ' + self.name

    def __init__(self):
        self.name = ''
        self.base_url = ''
        self.data = {}
        self.base_search_page = ''
        self.search_limit = 2

    def get_urls_to_parse(self):
        search_url = self.base_url + '/' + self.base_search_page
        pageno = 1
        search_page = requests.get(url=search_url + str(pageno), headers=HEADERS)
        while search_page.status_code != 404 and self.search_limit > pageno:
            if search_page.status_code == 503: # temporary off
                time.sleep(15)
                continue
            soup = BeautifulSoup(search_page.content, features='lxml')
            self.parse_search_page(soup)
            search_page = requests.get(url=search_url + str(pageno), headers=HEADERS)
            pageno += 1
            time.sleep(2)

    def parse_search_page(self, soup):
        raise NotImplementedError

    def get_element(self, element_function, soup):
        pass

    def parse_article_page(self, soup):
        data = dict()
        data['ingredients'] = self.get_ingredients(soup)
        data['title'] = self.get_title(soup)
        data['related'] = self.get_related(soup)
        data['directions'] = self.get_instructions(soup)
        data['rating'] = self.get_rating(soup)
        # data['reviews'] = self.get_reviews(soup)
        print(data)
        return data

    def get_title(self, soup):
        def __name__():
            return 'title'
        raise NotImplementedError('Not implemented yet')

    def get_ingredients(self, soup):
        """get ingredients,to be overwritten"""
        def __name__():
            return 'ingredients'
        raise NotImplementedError('Not implemented yet')

    def get_related(self, soup):
        """get other tags, to be overwritten"""
        def __name__():
            return 'related-articles'
        raise NotImplementedError('Not implemented yet')

    def get_tags(self, soup):
        """get other tags, to be overwritten"""
        def __name__():
            return 'search-tags'
        raise NotImplementedError('Not implemented yet')

    def get_instructions(self, soup):
        def __name__():
            return 'directions'
        raise NotImplementedError('Not implemented yet')

    def get_rating(self, soup):
        def __name__():
            return 'rating'
        raise NotImplementedError('Not implemented yet')

    def get_reviews(self, soup):
        def __name__():
            return 'reviews'
        raise NotImplementedError('Not implemented yet')

    def collect_articles(self):
        for url in self.data:
            print(url)
            resp = requests.get(url, headers=HEADERS)
            time.sleep(2)
            if resp.status_code == 404:
                print("Cannot find %s" %url)
                continue
            if resp.status_code == 503:
                time.sleep(10)
                continue
            soup = BeautifulSoup(resp.content)
            info = self.parse_article_page(soup)
            self.data[url].update(info)


    def main(self):
        self.get_urls_to_parse()
        self.collect_articles()


class AllRecipesParser(AbsractRecipes):
    def __init__(self):
        self.name = 'All Recipes'
        self.base_url = 'https://www.allrecipes.com'
        self.data = {}
        self.search_tags = ''
        self.base_search_page = 'recipes/78/breakfast-and-brunch/?page='
        self.search_limit = 2

    def parse_search_page(self, soup):
        for node in soup.find_all(name='article', attrs={'class': 'fixed-recipe-card'}):
            self.data[node.find_next('a').get('href')] = {'description':node.find_next('div',{'class':'fixed-recipe-card__description'}).text}
        print(self.data)

    def get_ingredients(self, soup):
        nodes = soup.find_all('span',{'class':'recipe-ingred_txt added'})
        return get_text_from_nodes(nodes)

    def get_instructions(self, soup):
        nodes = soup.find_all('span', {'class': 'recipe-directions__list--item'})
        return get_text_from_nodes(nodes)

    def get_related(self, soup):
        root = soup.find('div', {'id': 'similarRecipes'})
        nodes = root.find_all_next('a', {'data-internal-referrer-link':'similar_recipe_banner'})
        return [node['href'] for node in nodes]

    def get_rating(self, soup):
        return soup.find('div',{'class':'rating-stars'}).get('data-ratingstars')


    def get_title(self, soup):
        return soup.find('meta',{'property':'og:title'}).get('content')

def get_text_from_nodes(nodes):
    return [node.get_text() for node in nodes if node.get_text() is not None]

def post_processing_instructions(instructions, ):
    for i, element in enumerate(instructions):
        element.strip()

def post_processing_list(x, Cleaner):
    cleaned = [i for i in x if not any([re.match(expr, i) for expr in Cleaner.FULLREPLACE])]
    for i in range(len(cleaned)):
        for drop in Cleaner.INLINE:
            cleaned[i].apply(lambda x: post_processing_element(x, Cleaner))
    return cleaned

def post_processing_element(x, Cleaner):
    return x.strip().replace(drop, Cleaner.INLINE[drop]

class TextCleaners:
    class Generic:
        pass

    class IngredientCleaner:
        FULLREPLACE = ["Add all ingredients to list",None]



if __name__ == '__main__':
    x = AllRecipesParser()
    x.main()
