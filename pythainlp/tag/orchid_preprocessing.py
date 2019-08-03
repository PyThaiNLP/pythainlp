# -*- coding: utf-8 -*-
"""
Data preprocessing for orchid
"""
from typing import List

orchid_tag = {
    " " : "<space>",
    "+" : "<plus>",
    "-" : "<minus>",
    "=" : "<equal>",
    "," : "<comma>",
    "$" : "<dollar>",
    "." : "<full_stop>",
    "(" : "<left_parenthesis>",
    ")" : "<right_parenthesis>",
    '"' : "<quotation>",
    "@" : "<at_mark>",
    "&" : "<ampersand>",
    "{" : "<left_curly_bracket>",
    "^" : "<circumflex_accent>",
    "?" : "<question_mark>",
    "<" : "<less_than>",
    ">" : "<greater_than>",
    "!" : "<exclamation>",
    "’" : "<apostrophe>",
    ":" : "<colon>",
    "*" : "<asterisk>",
    ";" : "<semi_colon>",
    "/" : "<slash>"
}
orchid_text = dict((v,k) for k,v in orchid_tag.items())

def orchid_preprocessing(words: List[str]) -> List[str]:
	i = 0
	while i < len(words):
		if words[i] in orchid_tag.keys():
			words[i] = orchid_tag[words[i]]
		i += 1
	return words
def orchid_tag_to_text(word: str) -> str:
    if word in orchid_text.keys():
        word = orchid_text[word]
    return word