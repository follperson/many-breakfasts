#!/usr/bin/env python3
from parsers.abstract_parser import AbstractRecipes
from text_cleaner import TextCleaners
from utils import get_text_from_nodes
from parsers import Static


class AllRecipesParser(AbstractRecipes):
    def __init__(self, start_page=1, search_limit=2):
        super().__init__()
#        self.name = 'All Recipes All'
        self.name = 'All Recipes Breakfast'
        self.base_url = 'https://www.allrecipes.com'
        self.data = {}
        self.search_tags = ''
#        self.base_search_page = 'recipes/?page='
        self.base_search_page = 'recipes/78/breakfast-and-brunch/?page='
        self.search_limit = search_limit
        self.start_page = start_page
        self.parse_functions = {Static.TITLE: self.get_title, Static.INGREDIENTS: self.get_ingredients,
                                Static.DIRECTIONS: self.get_instructions, Static.RELATED: self.get_related,
                                Static.RATINGS: self.get_rating, Static.TAGS: self.get_tags}
        with open('static\\alt_parser_flag.txt','r') as flag:
            alt_flag = flag.read()
        self.alt_flag = alt_flag
        self.cleaner = TextCleaners.AllRecipes

    def parse_search_page(self, soup):
        for node in soup.find_all(name='article', attrs={'class': 'fixed-recipe-card'}):
            self.data[node.find_next('a').get('href')] = {'description':node.find_next('div',{'class':'fixed-recipe-card__description'}).text}
        print(len(self.data))

    def get_description(self, soup):
        return soup.find('meta',{'name':"description"}).get('content')

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
        # return soup.find('div',{'class':'rating-stars'}).get('data-ratingstars')
        val = soup.find('meta', {'itemprop': "ratingValue"}).get('content')
        ct = soup.find('meta', {'itemprop': "reviewCount"}).get('content')
        return val, ct

    def get_tags(self, soup):
        nodes = soup.find_all('meta', {'itemprop': "recipeCategory"})
        return [node['content'] for node in nodes]

    def get_title(self, soup):
        return soup.find('meta',{'property':'og:title'}).get('content')

