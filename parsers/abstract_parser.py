#!/usr/bin/env python3
import pandas as pd
import requests
from bs4 import BeautifulSoup
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
        self.alt_flag = None
        self.parse_functions = {Static.TITLE: self.get_title, Static.INGREDIENTS: self.get_ingredients,
                                Static.DIRECTIONS: self.get_instructions, Static.RELATED: self.get_related,
                                Static.RATINGS: self.get_rating, Static.TAGS: self.get_tags}
        self.cleaner = TextCleaners.AbstractCleaner

    def get_urls_to_parse(self):
        search_url = self.base_url + '/' + self.base_search_page
        pageno = self.start_page
        search_page = self.call_function(requests.get, url=search_url + str(pageno), headers=HEADERS)
        if search_page == 'Error':
            return
        while search_page != 'Error' and search_page.status_code != 404 and self.search_limit > (pageno - self.start_page):
            if search_page.status_code == 503: # temporary off
                random_wait(60)
                continue
            soup = BeautifulSoup(search_page.content, features='html.parser')
            self.parse_search_page(soup)
            pageno += 1
            random_wait(15)
            search_page = self.call_function(requests.get, url=search_url + str(pageno), headers=HEADERS)

    def get_local_urls(self):
        local_folder = 'html-downloads' + '/' + self.base_url.split('www')[-1].strip('.')
        self.data = {self.base_url + '/' +'/'.join(f.split('-')[0:2]) + '/' + '-'.join(f.split('-')[2:]).replace('.html', '/'):
                         {'description': 'tbd'}
                     for f in os.listdir(local_folder)}

    def parse_search_page(self, soup):
        raise NotImplementedError('meant to be overwritten')

    def call_function(self, func, *args, **kwargs):
        try:
            resp = func(*args, **kwargs)
        except (requests.urllib3.exceptions.MaxRetryError,requests.exceptions.ConnectionError) as requests_error:
            print(func.__name__, requests_error)
            resp = 'Error'
        except Exception as hmm:
            print(func.__name__, hmm)
            resp = 'Error'
        return resp

    def parse_article_page(self, soup):
        data = dict()
        for name, func in self.parse_functions.items():
            data[name] = self.call_function(func, soup=soup)
        return data

    def get_description(self, soup):
        raise NotImplementedError('Not implemented yet')

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
        local_folder = 'html-downloads' + '\\' + self.base_url.split('www')[-1].strip('.')
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)
        for url in self.data:
            local_html = local_folder + '\\' + url.replace(self.base_url, '').strip('/').replace('/', '-') + '.html'
            if os.path.exists(local_html):
                print("Using Local Copy %s" % url)
                with open(local_html, 'rb') as html:
                    content = html.read()
            else:
                random_wait(10) # only need to chill when using live
                print("Using live copy %s" % url)
                resp = self.call_function(requests.get, url=url, headers=HEADERS)
                if resp == 'Error':
                    random_wait(20)
                    continue
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
                if soup.contents[2] == self.alt_flag:  # todo implement alt parser
                    print('Alt flagged', local_html)
                    continue
                info = self.parse_article_page(soup)
            except Exception as wow:
                print('Serious error with url %s, : %s' % (url, wow))
                continue
            self.data[url].update(info)

    def main(self, live=True):
        if live:
            self.get_urls_to_parse()
        else:
            self.parse_functions.update({Static.DESCRIPTION: self.get_description})
            self.get_local_urls()
        self.collect_articles()
        print(curtime())
        self.reformat_data()

    def reformat_data(self):
        df = pd.DataFrame().from_dict(self.data).T
        out = 'scraping\\%s_data scraping_%s.xlsx' % (self.name, str(curtime()).split('.')[0])
        df.to_excel(out)
        for col in self.cleaner['list']:
            df[col + '_cleaned'] = df[col].apply(lambda x: x if pd.isnull(x) else post_processing_list(x, self.cleaner['list'][col]))
        for col in self.cleaner['str']:
            df[col + '_cleaned'] = df[col].apply(lambda x: x if pd.isnull(x) else post_processing_element(x, self.cleaner['str'][col].INLINE))
        df.to_excel(out)



if __name__ == '__main__':
    pass