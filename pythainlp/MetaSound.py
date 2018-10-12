# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
from builtins import *
'''
MetaSound

References

Snae & Brückner. (2009). Novel Phonetic Name Matching Algorithm with a Statistical Ontology for Analysing Names Given in Accordance with Thai Astrology. Retrieved from https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf
'''
import re
def MetaSound(name):
    '''
    Thai MetaSound

    :param str name: thai text
    :return: MetaSound for thai text
    **Example**::
        >>> from pythainlp.MetaSound import MetaSound
        >>> MetaSound('รัก')
        '501'
        >>> MetaSound('ลัก')
        '501'
    '''
    name1=list(name)
    count=len(name1)
    word=[]
    i=0
    while i<count:
        if (re.search(r'[ก-ฮ]',name1[i]),re.U):
            word.append(name1[i])
        i+=1
    i=0
    count=len(name1)
    while i<count:
        if (re.search('์',name1[i],re.U)):
            word[i-1]=''
            word[i]=''
        i+=1
    i=0
    while i<count:
        if (re.search('[กขฃคฆฅ]',word[i],re.U)):
            name1[i]='1'
        elif (re.search('[จฉชฌซฐทฒดฎตสศษ]',word[i],re.U)):
            name1[i]='2'
        elif (re.search('[ฟฝพผภบป]',word[i],re.U)):
            name1[i]='3'
        elif (re.search('[ง]',word[i],re.U)):
            name1[i]='4'
        elif (re.search('[ลฬรนณฦญ]',word[i],re.U)):
            name1[i]='5'
        elif (re.search('[ม]',word[i],re.U)):
            name1[i]='6'
        elif (re.search('[ย]',word[i],re.U)):
            name1[i]='7'
        elif (re.search('[ว]',word[i],re.U)):
            name1[i]='8'
        else:
            name1[i]='0'
        i+=1
    return ''.join(name1)
if __name__ == '__main__':
    print(MetaSound('รัก'))
    print(MetaSound('ลัก'))
