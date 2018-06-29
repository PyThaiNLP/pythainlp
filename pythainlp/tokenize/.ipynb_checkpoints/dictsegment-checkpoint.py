# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals,print_function
from .thai import data
lines = data()
# fork from https://stackoverflow.com/a/16690988
def segment(string):
    """รับค่าสตริง str คืนค่า list"""
    # Sort wset in decreasing string order
    lines.sort(key=len, reverse=True)
    result = tokenize(string, lines, "")
    if result:
        result.pop() # Remove the empty string token
        result.reverse() # Put the list into correct order
    return result

def tokenize(string, wset, token):
    """Returns either false if the string can't be segmented by 
    the current wset or a list of words that segment the string
    in reverse order."""
    # Are we done yet?
    if string == "":
        return [token]
    # Find all possible prefixes
    for pref in wset:
        if string.startswith(pref):
            res = tokenize(string.replace(pref, '', 1), wset, pref)
            if res:
                res.append(token)
                return res
    # Not possible
    return False
if __name__ == "__main__":
	print(segment("ฉันรักเธอ"))