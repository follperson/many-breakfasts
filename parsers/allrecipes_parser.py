#!/usr/bin/env python3
import pandas as pd
from parsers.abstract_parser import AbstractRecipes
from text_cleaner import TextCleaners
from utils import get_text_from_nodes
from parsers import Static

class AllRecipesParser(AbstractRecipes):
    def __init__(self):
        super().__init__()
        self.name = 'All Recipes'
        self.base_url = 'https://www.allrecipes.com'
        self.data = {}
        self.search_tags = ''
        self.base_search_page = 'recipes/78/breakfast-and-brunch/?page='
        self.search_limit = 2
        # self.parse_functions = [self.get_title, self.get_ingredients, self.get_instructions, self.get_related,
        #                         self.get_rating]
        self.cleaner = TextCleaners.AllRecipes

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
        def __name__():
            return Static.TITLE
        return soup.find('meta',{'property':'og:title'}).get('content')

