#!/usr/bin/env python3
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from time import time as curtime
import os
from parsers import Static
from utils import post_processing_list, post_processing_element, random_wait
from text_cleaner import TextCleaners

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
        self.start_page = 1
        self.parse_functions = [[Static.TITLE, self.get_title], [Static.INGREDIENTS, self.get_ingredients],
                                [Static.DIRECTIONS, self.get_instructions], [Static.RELATED, self.get_related],
                                [Static.RATINGS, self.get_rating]]
        self.cleaner = TextCleaners.AbstractCleaner


    def get_urls_to_parse(self):
        search_url = self.base_url + '/' + self.base_search_page
        pageno = self.start_page
        search_page = requests.get(url=search_url + str(pageno), headers=HEADERS)
        while search_page.status_code != 404 and self.search_limit > (pageno - self.start_page):
            if search_page.status_code == 503: # temporary off
                random_wait(60)
                continue
            soup = BeautifulSoup(search_page.content, features='lxml')
            self.parse_search_page(soup)
            pageno += 1
            random_wait(30)
            search_page = requests.get(url=search_url + str(pageno), headers=HEADERS)

    def parse_search_page(self, soup):
        raise NotImplementedError('meant to be overwritten')

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
            random_wait(5)
            local_html ='html-downloads/%s/%s.html' % (self.base_url.split('www')[-1].strip('.'), url.replace(self.base_url,'').strip('/').replace('/','-'))
            if os.path.exists(local_html):
                print("Using Local Copy %s" % url)
                with open(local_html, 'rb') as html:
                    content = html.read()
            else:
                print("Using live copy %s" % url)
                resp = requests.get(url, headers=HEADERS)
                if resp.status_code == 404:
                    print("Cannot find %s" %url)
                    continue
                if resp.status_code == 503:
                    random_wait(20)
                    continue
                content = resp.content
                if not os.path.exists(os.path.dirname(local_html)):
                    os.makedirs(os.path.dirname(local_html))
                with open(local_html, 'wb') as html:
                    html.write(content)
            soup = BeautifulSoup(content)
            try:
                info = self.parse_article_page(soup)
            except Exception as wow:
                print('Serious error with url %s, : %s' % (url, wow))
                continue
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
        df.to_excel('scraping\\%s_data scraping_%s.xlsx' % (self.name, str(curtime()).split('.')[0]))



if __name__ == '__main__':
    pass