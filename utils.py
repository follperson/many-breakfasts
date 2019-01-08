#!/usr/bin/env python3
import re

def get_text_from_nodes(nodes):
    return [node.get_text() for node in nodes if node.get_text() is not None]

def post_processing_list(x, Cleaner):
    cleaned = [post_processing_element(i,Cleaner.INLINE) for i in x
               if not any([re.match(expr, i) for expr in Cleaner.FULLREPLACE])]
    return cleaned

def post_processing_element(e, drop_dict):
    return e.strip().translate(drop_dict)
