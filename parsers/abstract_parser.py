#!/usr/bin/env python3
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import os
from parsers import Static
from utils import post_processing_list, post_processing_element
from text_cleaner import TextCleaners
__author__ = 'Andrew Follmann'
__date__ = ''
__version__ = '0.0.1'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}


# self.search_tags = {'name':'article','attrs':{'class':'fixed-recipe-card'}}


class AbstractRecipes(object):
    def __str__(self):
        return 'Recipe Site Scraper for ' + self.name

    def __init__(self):
        self.name = ''
        self.base_url = ''
        self.data = {}
        self.base_search_page = ''
        self.search_limit = 2
        self.parse_functions = [[Static.TITLE, self.get_title], [Static.INGREDIENTS, self.get_ingredients],
                                [Static.DIRECTIONS, self.get_instructions], [Static.RELATED, self.get_related],
                                [Static.RATINGS, self.get_rating]]
        self.cleaner = TextCleaners.AbstractCleaner


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

    def call_function(self, func, *args,**kwargs):
        try:
            resp = func(**kwargs)
        except Exception as hmm:
            print(func.__name__, hmm)
            resp = 'Error'
        return resp

    def parse_article_page(self, soup):
        data = dict()
        for name, func in self.parse_functions:
            data[name] = self.call_function(func, soup=soup)
        print(data)
        return data

    def get_title(self, soup):
        raise NotImplementedError('Not implemented yet')

    def get_ingredients(self, soup):
        """get ingredients,to be overwritten"""
        raise NotImplementedError('Not implemented yet')

    def get_related(self, soup):
        """get other tags, to be overwritten"""
        raise NotImplementedError('Not implemented yet')

    def get_tags(self, soup):
        """get other tags, to be overwritten"""
        raise NotImplementedError('Not implemented yet')

    def get_instructions(self, soup):
        raise NotImplementedError('Not implemented yet')

    def get_rating(self, soup):
        raise NotImplementedError('Not implemented yet')

    def get_reviews(self, soup):
        raise NotImplementedError('Not implemented yet')

    def collect_articles(self):
        for url in self.data:
            print(url)
            time.sleep(2)
            local_html ='html-downloads/%s/%s.html' % (self.base_url.split('www')[-1].strip('.'), url.replace(self.base_url,'').strip('/').replace('/','-'))
            if os.path.exists(local_html):
                with open(local_html,'rb') as html:
                    content = html.read()
            else:
                resp = requests.get(url, headers=HEADERS)
                if resp.status_code == 404:
                    print("Cannot find %s" %url)
                    continue
                if resp.status_code == 503:
                    time.sleep(10)
                    continue
                content = resp.content
                if not os.path.exists(os.path.dirname(local_html)):
                    os.makedirs(os.path.dirname(local_html))
                with open(local_html, 'wb') as html:
                    html.write(content)
            soup = BeautifulSoup(content)
            info = self.parse_article_page(soup)
            self.data[url].update(info)


    def main(self):
        self.get_urls_to_parse()
        self.collect_articles()
        self.reformat_data()

    def reformat_data(self):
        df = pd.DataFrame().from_dict(self.data).T
        for col in self.cleaner['list']:
            df[col + '_cleaned'] =df[col].apply(lambda x: post_processing_list(x, self.cleaner['list'][col]))
        for col in self.cleaner['str']:
            df[col + '_cleaned'] = df[col].apply(lambda x: post_processing_element(x, self.cleaner['str'][col].INLINE))
        df.to_excel('scraping\\%s_data scraping_%s.xlsx' % (self.name, str(time.time()).split('.')[0]))


if __name__ == '__main__':
    pass