# -*- coding: utf-8 -*-
"""
Data preprocessing for orchid
"""
def orchid_preprocessing(words):
	i = 0
	while i < len(words):
		if words[i] == " ":
			words[i] = "<space>"
		elif words[i] == "+":
			words[i] = "<plus>"
		elif words[i] == "-":
			words[i] = "<minus>"
		elif words[i] == "=":
			words[i] = "<equal>"
		elif words[i] == ",":
			words[i] = "<comma>"
		elif words[i] == "$":
			words[i] = "<dollar>"
		elif words[i] == ".":
			words[i] = "<full_stop>"
		elif words[i] == "(":
			words[i] = "<left_parenthesis>"
		elif words[i] == ")":
			words[i] = "<right_parenthesis>"
		elif words[i] == '"':
			words[i] = "<quotation>"
		elif words[i] == "@":
			words[i] = "<at_mark>"
		elif words[i] == "&":
			words[i] = "<ampersand>"
		elif words[i] == "{":
			words[i] = "<left_curly_bracket>"
		elif words[i] == "^":
			words[i] = "<circumflex_accent>"
		elif words[i] == "?":
			words[i] = "<question_mark>"
		elif words[i] == "<":
			words[i] = "<less_than>"
		elif words[i] == ">":
			words[i] = "<greater_than>"
		elif words[i] == "=":
			words[i] = "<equal>"
		elif words[i] == "!":
			words[i] = "<exclamation>"
		elif words[i] == "’":
			words[i] = "<apostrophe>"
		elif words[i] == ":":
			words[i] = "<colon>"
		elif words[i] == "*":
			words[i] = "<asterisk>"
		elif words[i] == ";":
			words[i] = "<semi_colon>"
		elif words[i] == "/":
			words[i] = "<slash>"
		i += 1
	return words
def orchid_tag_to_text(word):
    if word == "<space>":
        word = " "
    elif word == "<plus>":
        word = "+"
    elif word == "<minus>":
        word = "-"
    elif word == "<equal>":
        word = "="
    elif word == "<comma>":
        word = ","
    elif word == "<dollar>":
        word = "$"
    elif word == "<full_stop>":
        word = "."
    elif word == "<left_parenthesis>":
        word = "("
    elif word == "<right_parenthesis>":
        word = ")"
    elif word == "<quotation>":
        word = '"'
    elif word == "<at_mark>":
        word = "@"
    elif word == "<ampersand>":
        word = "&"
    elif word == "<left_curly_bracket>":
        word = "{"
    elif word == "<circumflex_accent>":
        word = "^"
    elif word == "<question_mark>":
        word = "?"
    elif word == "<less_than>":
        word = "<"
    elif word == "<greater_than>":
        word = ">"
    elif word == "<equal>":
        word = "="
    elif word == "<exclamation>":
        word = "!"
    elif word == "<apostrophe>":
        word = "’"
    elif word == "<colon>":
        word = ":"
    elif word == "<asterisk>":
        word = "*"
    elif word == "<semi_colon>":
        word = ";"
    elif word == "<slash>":
        word = "/"
    return word