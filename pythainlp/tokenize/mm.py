# -*- coding: utf-8 -*-

'''
based on algorithm from
http://www.aclweb.org/anthology/E14-4016

fork from https://github.com/narongdejsrn/pythaiwordcut
License: MIT
'''

from __future__ import print_function
from six.moves import range,zip
import codecs
import re
from pythainlp.tools import file_trie
from pythainlp.corpus import stopwords # load  stopwords
import marisa_trie
class wordcut(object):
    """
    ตัดคำภาษาไทยด้วย Maximum Matching algorithm
    """
    def __init__(self, removeRepeat=True, keyDictionary="", stopDictionary="", removeSpaces=True, minLength=1, stopNumber=False, removeNonCharacter=False, caseSensitive=True, ngram=(1,1), negation=False,data=""):
        if data!="":
            d = data # load dictionary
        # load negation listdir
        self.negationDict = []
        if negation:
            self.negationDict = ['ไม่','แต่']
        self.stopword = False
        self.stopdict = []
        if(stopDictionary is not ""):
            self.stopword = True
            with codecs.open(stopDictionary, 'r',encoding='utf8') as f:
                for line in f:
                    self.stopdict.append(line)
        else:
            self.stopdict = stopwords.words('thai')
        self.keyword = False
        self.keydict = []
        if(keyDictionary is not ""):
            self.keyword = True
            with codecs.open(keyDictionary, 'r',encoding='utf8') as f:
                for line in f.read().splitlines():
                    self.keydict.append(line)

        if data=="":
            self.trie = file_trie(data="old")
        else:
            self.trie = marisa_trie.Trie(d)
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
            match = re.search(u"[0-9A-Za-z\u0E00-\u0E7F]+", word,re.U)
            if not match:
                return False

        return True

    # Find maximum matching in Trie if match return id else return -1
    def search_trie(self, word):
        # remove negation if see a space
        if(word[0:1] == " "):
            self.onNegation = False

        # check latin words
        match = re.search(u"[A-Za-z\d]*", word,re.U)
        if match.group(0):
            if not self.caseSensitive:
                return match.group(0).lower()
            else:
                return match.group(0)

        # check number
        match = re.search(u"[\d]*", word,re.U)
        if match.group(0):
            return match.group(0)

        longest = 0
        max_data = None

        for x in range(20):
            if word[0:x] in self.trie:
                longest = len(word[0:x])
                max_data = word[0:x]

        if longest > 20:
            for data in self.trie.keys(word[0:longest]):
                if len(data) > longest and data in word[0:len(data)]:
                    longest = len(data)
                    max_data = data


        if max_data:
            try:
                # Special check for case like ๆ
                if word[len(max_data)] == 'ๆ':
                    return word[0:(len(max_data) + 1)]
                else:
                    return max_data
            except:
                return max_data
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

    def extract_keyword(self, wordArray):
        """
        ใช้ในการหาคำสำคัญ
        """
        result_array = []
        for dd in wordArray:
            try:
                if self.caseSensitive and dd in self.keydict:
                    result_array.append(dd)
                else:
                    if dd.lower() in self.keydict:
                        result_array.append(dd)
            except ValueError:
                pass

        return result_array
    # c = sentence which represent as char
    # N = number of character
    def find_segment(self, c):
        i = 0
        N = len(c)
        arr = []
        while(i < N):
            j = self.search_trie(c[i:N])
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
        '''
        ตัดคำใช้ฟังก์ชัน segment
        '''
        result = self.find_segment(c)
        if self.stopword:
            result = self.transform(result)

        result = [x for x in result if self.determine(x)]

        lastresult = []
        for x in range(self.ngram[0], self.ngram[1]+1):
            for r in self.find_ngrams(result, x):
                match = re.search(u"[A-Za-z\d]+", ''.join(r),re.U)
                if not match:
                    lastresult.append(''.join(r))
                else:
                    if self.negation:
                        lastresult.append(''.join(r))
                    else:
                        lastresult.append(' '.join(r))
        return lastresult
def mergelistlen(listdata,lennum):
    '''
    แก้ Bug ที่เกิดจาก mm
    '''
    i=0
    listlen=len(listdata)
    while i<listlen:
        if i>(listlen-1) or i+1==listlen:
            '''
            ถ้า i เกินความยาว list ให้ออกจากการลูป
            '''
            break
        elif re.search(r'[0-9]',listdata[i]):
            '''
            ถ้าหาก listdata[i] เป็นตัวเลขให้ข้ามไป
            '''
            pass
        elif re.search(r'[ะา]',listdata[i]) and (len(listdata[i])==lennum and len(listdata[i+1])==lennum):
            '''
            ถ้าหาก listdata[i] คือ ะ/า ซึ่งเปนสระที่ไว้ข้างหลังได้เท่านั้น และ listdata[i] กับ listdata[i+1] ยาวเท่า lennum
            จึงนำ listdata[i] ไปรวมกับ listdata[i-1] แล้วลบ listdata[i] ออก
            '''
            listdata[i-1]+=listdata[i]
            del listdata[i]
            i-=1
        elif re.search(r'[ก-ฮ]',listdata[i]) and re.search(r'[0-9]',listdata[i+1]):
            '''
            กันปัญหา ก-ฮ ตัวต่อมาเป็น 0-9 มีความยาวเท่ากัน ให้ ก-ฮ ไปรวมกับตัวก่อนหน้า
            '''
            listdata[i-1]+=listdata[i]
            del listdata[i]
            i-=1
        elif len(listdata[i])==lennum and len(listdata[i+1])==lennum:
            '''
            ถ้าหาก list มีความยาวเท่ากันอยู่ติดกัน
            '''
            #print(listdata,'99')
            T=True
            num=1
            while T==True:
               if (i+num)>=listlen:
                   ii=i
                   num2=1
                   TT=True
                   while TT==True:
                    if (i+num2)<=(listlen-1):
                        listdata[i]+=listdata[i+num2]
                        num2+=1
                    elif (i+num2)>(listlen-1):
                        num2-=1
                        TT=False
                   TT=True
                   while TT==True:
                    if (i+num2) != i:
                        del listdata[i+num2]
                        num2-=1
                    else:
                        TT=False
                   T=False
               elif len(listdata[i+(num-1)])!=len(listdata[i+num]): #and re.search(r'[0-9]',listdata[i+(num-1)])==False:# and isThai(listdata[i+(num-1)])==True:
                    ii=1+i
                    while ii<(i+num) and ii<(len(listdata)-1):
                        listdata[i]+=listdata[ii]
                        ii+=1
                    ii=i+num-1
                    while ii>i:
                        del listdata[ii]
                        ii-=1
                    T=False
               num+=1
            del T,ii
        elif len(listdata[i])==lennum and len(listdata[i+1])!=lennum:
            '''
            ในกรณีที่ list ความยาวที่กำหนด แต่ตัวต่อไปยาวไม่เท่า ให้ยุบรวมกัน
            '''
            if re.search(r'[เแโใไ]',listdata[i]):
                '''
                ถ้าหากเป็นสระต้นคำ ให้รวมกัน
                '''
                listdata[i]+=listdata[i+1]
                del listdata[i+1]
            elif re.search(r'[ก-ฮ]',listdata[i]) or re.search(r'[ะา]',listdata[i]):
                '''
                หากเป็นแค่พยัญชนะให้รวมกับตัวหลัง
                '''
                listdata[i-1]+=listdata[i]
                del listdata[i]
                i-=1
        listlen=len(listdata)
        i+=1
    return listdata
def segment(text,data=""):
    '''
    ใช้ในการตัดตำ segment(str) คืนค่า list
    '''
    pt = wordcut(stopNumber=False, removeNonCharacter=True, caseSensitive=False,removeRepeat=True,data=data)
    return mergelistlen(pt.segment(text),1)