#!/usr/bin/env python3
from parsers import Static
import re
FULLREPLACE = ['^None$','^\s*$']
INLINE = {'\s*$':'', '^\s*':''}

class TextCleaners:
    class GenericCleaner:
        FULLREPLACE = FULLREPLACE
        INLINE = INLINE

    class IngredientCleaner:
        FULLREPLACE = FULLREPLACE + ["$\s*Add all ingredients to list"]
        INLINE = INLINE

    class DirectionCleaner:
        FULLREPLACE = FULLREPLACE
        INLINE = INLINE.copy().update({'\s*Watch Now$':''})

    class IngredientMeasurementCleaner:
        INLINE = INLINE.copy().update({i:'' for i in [re.compile('\d*[/.]{0,1}\d*'),
                               re.compile('teaspoons{0,1}', re.IGNORECASE),
                               re.compile('tablespoons{0,1}', re.IGNORECASE),
                               re.compile('cups{0,1}', re.IGNORECASE),
                               re.compile('liters{0,1}', re.IGNORECASE),
                               re.compile('quarts{0,1}', re.IGNORECASE),
                               re.compile('pints{0,1}', re.IGNORECASE),
                               'jumbo', 'extra large', 'large', 'extra small', 'small', 'medium', 'pinch', 'dash',
                               re.compile('pounds{0,1}', re.IGNORECASE),
                               re.compile('ounces{0,1}', re.IGNORECASE),
                               ]})
        FULLREPLACE = FULLREPLACE

    AbstractCleaner ={'list':{
        Static.INGREDIENTS: IngredientCleaner,
        Static.DIRECTIONS: GenericCleaner,
                      },'str':{},
                    }

    AllRecipes = AbstractCleaner
