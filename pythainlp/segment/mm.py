# -*- coding: utf-8 -*-

'''
based on algorithm from
http://www.aclweb.org/anthology/E14-4016

fork from https://github.com/narongdejsrn/pythaiwordcut
License: MIT 
'''

from __future__ import print_function
from six.moves import range,zip
import re
from .thai import newdata # load dictionary
from pythainlp.corpus import stopwords # load  stopwords

class wordcut(object):
    def __init__(self, removeRepeat=True, stopDictionary="", removeSpaces=True, minLength=1, stopNumber=False, removeNonCharacter=False, caseSensitive=True, ngram=(1,1), negation=False):
        d = newdata() # load dictionary
        # load negation listdir
        self.negationDict = ['ไม่','แต่']
        self.stopword = False
        self.stopdict = stopwords.words('thai')

        self.trie = d
        self.removeRepeat = removeRepeat
        self.stopNumber = stopNumber
        self.removeSpaces = removeSpaces
        self.minLength = minLength
        self.removeNonCharacter = removeNonCharacter
        self.caseSensitive = caseSensitive
        self.ngram = ngram
        self.negation = negation
        self.onNegation = False

    def determine(self, word):
        if self.stopNumber and word.isdigit():
            return False

        if self.removeSpaces and word.isspace():
            return False

        if len(word) < self.minLength:
            return False

        if self.removeNonCharacter:
            match = re.search(u"[0-9A-Za-z\u0E00-\u0E7F]+", word)
            if not match:
                return False

        return True

    # Find maximum matching in Trie if match return id else return -1
    def searchTrie(self, word):
        # remove negation if see a space
        if(word[0:1] == " "):
            self.onNegation = False

        # check latin words
        match = re.search(u"[A-Za-z\d]*", word)
        if match.group(0):
            if not self.caseSensitive:
                return match.group(0).lower()
            else:
                return match.group(0)

        # check number
        match = re.search(u"[\d]*", word)
        if match.group(0):
            return match.group(0)

        longest = 0
        maxData = None

        for x in range(20):
            if word[0:x] in self.trie:
                longest = len(word[0:x])
                maxData = word[0:x]

        if longest > 20:
            for data in self.trie.keys(word[0:longest]):
                if(len(data) > longest):
                    if data in word[0:len(data)]:
                        wordLength = 0
                        longest = len(data)
                        maxData = data


        if maxData:
            try:
                # Special check for case like ๆ
                if word[len(maxData)] == u'ๆ':
                    return word[0:(len(maxData) + 1)]
                else:
                    return maxData
            except:
                return maxData
        else:
            return -1

    def transform(self, wordArray):
        for dd in self.stopdict:
            try:
                if self.caseSensitive:
                    wordArray.remove(dd)
                else:
                    wordArray.remove(dd.lower())
            except ValueError:
                pass

        return wordArray

    # c = sentence which represent as char
    # N = number of character
    def find_segment(self, c):
        i = 0
        N = len(c)
        arr = []
        while(i < N):
            j = self.searchTrie(c[i:N])
            if(j == -1):
                if(self.removeRepeat is False or c[i] != c[i - 1]):
                    arr.append(c[i])
                    i = i + 1
                else:
                    i = i + 1
            else:
                k = j
                if self.negation:
                    if self.onNegation:
                        k = 'NOT_' + j

                    if j in self.negationDict:
                        self.onNegation = True

                arr.append(k)
                i = i + len(j)
        return arr

    def find_ngrams(self, input_list, n):
        return zip(*[input_list[i:] for i in range(n)])

    def segment(self, c):
        result = self.find_segment(c)
        if self.stopword:
            result = self.transform(result)

        result = [x for x in result if self.determine(x)]

        lastresult = []
        for x in range(self.ngram[0], self.ngram[1]+1):
            for r in self.find_ngrams(result, x):
                match = re.search(u"[A-Za-z\d]+", ''.join(r))
                if not match:
                    lastresult.append(''.join(r))
                else:
                    if self.negation:
                        lastresult.append(''.join(r))
                    else:
                        lastresult.append(' '.join(r))
        return lastresult
def segment(text):
    pt = wordcut(stopNumber=False, removeNonCharacter=True, caseSensitive=False, negation=True, removeRepeat=True)
    return pt.segment(text)