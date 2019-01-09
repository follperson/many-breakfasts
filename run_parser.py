#!/usr/bin/env python3
from parsers.allrecipes_parser import AllRecipesParser

__author__ = 'Andrew Follmann'
__date__ = ''
__version__ = '0.0.3'


def main():
    parser = AllRecipesParser(start_page=18,search_limit=3)
    parser.main()



if __name__ == '__main__':
    main()