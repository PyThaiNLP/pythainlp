# เครื่องมือในการ build sentiment เพื่อใช้ใน pythainlp
# เวชั่น 0.2
# 2017/08/17
# เขียนโดย นาย วรรณพงษ์  ภัททิยไพบูลย์
# ใช้ประกอบบทความใน python3.wannaphong.com
# cc-by 3.0 Thai Sentiment Text https://github.com/wannaphongcom/lexicon-thai/tree/master/ข้อความ/
# อ่านบทความได้ที่ https://python3.wannaphong.com/2017/02/ทำ-sentiment-analysis-ภาษาไทยใน-python.html
from nltk import NaiveBayesClassifier as nbc
import dill
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import stopwords
import codecs
from itertools import chain
a = stopwords.words('thai')
# pos.txt
with codecs.open('pos.txt', 'r', "utf-8") as f:
    lines = f.readlines()
listpos=[e.strip() for e in lines]
del lines
f.close() # ปิดไฟล์
# neg.txt
with codecs.open('neg.txt', 'r', "utf-8") as f:
    lines = f.readlines()
listneg=[e.strip() for e in lines]
f.close() # ปิดไฟล์
print(1)
pos1=['pos']*len(listpos)
neg1=['neg']*len(listneg)
print(2)
training_data = list(zip(listpos,pos1)) + list(zip(listneg,neg1))
print(3)
vocabulary = set(chain(*[(set(word_tokenize(i[0]))-set(stopwords.words('thai'))) for i in training_data]))
#vocabulary = set(chain(*[x for x in a if x not in [list(set(word_tokenize(i[0]))) for i in training_data]]))
print(3.1)
feature_set = [({i:(i in word_tokenize(sentence)) for i in vocabulary},tag) for sentence, tag in training_data]
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
