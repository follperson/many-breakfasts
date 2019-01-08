#!/usr/bin/env python3
from parsers import Static
FULLREPLACE = ['\s', 'None','']
INLINE = ['/s$', '']

class TextCleaners:
    class GenericCleaner:
        FULLREPLACE = FULLREPLACE
        INLINE = INLINE

    class IngredientCleaner:
        FULLREPLACE = FULLREPLACE + ["Add all ingredients to list"]
        INLINE = INLINE

    AbstractCleaner ={'list':{
        Static.INGREDIENTS: IngredientCleaner,
        Static.DIRECTIONS: GenericCleaner,
                      },'str':{},
                    }

    AllRecipes = AbstractCleaner
