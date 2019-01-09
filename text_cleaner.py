#!/usr/bin/env python3
from parsers import Static
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


    AbstractCleaner ={'list':{
        Static.INGREDIENTS: IngredientCleaner,
        Static.DIRECTIONS: GenericCleaner,
                      },'str':{},
                    }

    AllRecipes = AbstractCleaner
