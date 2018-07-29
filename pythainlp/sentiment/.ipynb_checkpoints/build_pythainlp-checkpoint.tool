# -*- coding: utf-8 -*-
# เครื่องมือในการ build sentiment เพื่อใช้ใน pythainlp
# เวชั่น 0.3
# 2018/01/18
# เขียนโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
# cc-by 3.0 Thai Sentiment Text https://github.com/wannaphongcom/lexicon-thai/tree/master/ข้อความ/
# อ่านบทความได้ที่ https://python3.wannaphong.com/2017/02/ทำ-sentiment-analysis-ภาษาไทยใน-python.html
from nltk import NaiveBayesClassifier as nbc
import dill
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import stopwords
import codecs
from itertools import chain
thaistopwords = stopwords.words('thai')
# pos.txt
with codecs.open('pos.txt', 'r', "utf-8") as f:
    lines = f.readlines()
listpos=[x for x in [e.strip() for e in lines] if x not in thaistopwords]
del lines
f.close() # ปิดไฟล์
# neg.txt
with codecs.open('neg.txt', 'r', "utf-8") as f:
    lines = f.readlines()
listneg=[x for x in [e.strip() for e in lines] if x not in thaistopwords]
f.close() # ปิดไฟล์
print(1)
pos1=['pos']*len(listpos)
neg1=['neg']*len(listneg)
print(2)
training_data = list(zip(listpos,pos1)) + list(zip(listneg,neg1))
print(3)
#vocabulary = set(chain(*[(set(word_tokenize(i[0]))-set(stopwords.words('thai'))) for i in training_data]))
#vocabulary = set(chain(*[x for x in a if x not in [list(set(word_tokenize(i[0]))) for i in training_data]]))
vocabulary = set(chain(*[word_tokenize(i[0]) for i in training_data]))
#print(vocabulary)
print(3.1)
feature_set = [({i:(i in word_tokenize(sentence)) for i in vocabulary},tag) for sentence, tag in training_data]
#print(feature_set)
print(4)
classifier = nbc.train(feature_set)
print(5)
with open('vocabulary.data', 'wb') as out_strm: 
    dill.dump(vocabulary,out_strm)
out_strm.close()
with open('sentiment.data', 'wb') as out_strm: 
    dill.dump(classifier,out_strm)
out_strm.close()
print('OK')