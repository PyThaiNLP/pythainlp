# คู่มือการใช้งาน PyThaiNLP 1.7

[TOC]

Natural language processing หรือ การประมวลภาษาธรรมชาติ  โมดูล PyThaiNLP เป็นโมดูลที่ถูกพัฒนาขึ้นเพื่อพัฒนาการประมวลภาษาธรรมชาติภาษาไทยในภาษา Python และ**มันฟรี (ตลอดไป) เพื่อคนไทยและชาวโลกทุกคน !**

> เพราะโลกขับเคลื่อนต่อไปด้วยการแบ่งปัน

รองรับ Python 2.7 และ Python 3.4 ขึ้นไปเท่านั้น

ติดตั้งใช้คำสั่ง

```
pip install pythainlp
```

ปัจจุบันนี้ PyThaiNLP ไม่ต้องการ PyICU ในการใช้งาน API อีกแล้ว แต่หากท่านต้องการใช้ API ที่มี PyICU ให้ทำตามคำแนะนำข้างล่างนี้

**วิธีติดตั้งสำหรับ Windows**

การติดตั้ง pythainlp บน windows ต้องติดตั้ง pyicu ซึ่งทำได้ยากมาก
วิธีที่ง่ายที่สุดคือใช้ wheel

1. [http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu) แล้ว download wheel ตาม python ตัวเองเช่น
    ผมใช้ python x64 3.6.1 บน Windows ก็ให้ใช้ PyICU‑1.9.7‑cp36‑cp36m‑win_amd64.whl

2. `pip install PyICU‑1.9.7‑cp36‑cp36m‑win_amd64.whl`

3. `pip install pythainlp`

**ติดตั้งบน Mac**

** แนะนำให้ใช้ icu 58.2 เนื่องจาก icu 59.1 มาปัญหากับ PyICU **

```sh
$ brew install icu4c --force
$ brew link --force icu4c
$ CFLAGS=-I/usr/local/opt/icu4c/include LDFLAGS=-L/usr/local/opt/icu4c/lib pip install pythainlp
```

ข้อมูลเพิ่มเติม [คลิกที่นี้](https://medium.com/data-science-cafe/install-polyglot-on-mac-3c90445abc1f#.rdfrorxjx)

## API

### tokenize

#### word_tokenize

สำหรับการตัดคำไทยนั้น ใช้ API ดังต่อไปนี้

```python
from pythainlp.tokenize import word_tokenize
word_tokenize(text,engine)
```
text คือ ข้อความในรูปแบบสตริง str เท่านั้น

engine คือ ระบบตัดคำไทย ปัจจุบันนี้ PyThaiNLP ได้พัฒนามี 6 engine ให้ใช้งานกันดังนี้

1. newmm - ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย โค้ดชุดใหม่ โดยใช้โค้ดคุณ Korakot Chaovavanich  จาก https://www.facebook.com/groups/408004796247683/permalink/431283740586455/ มาพัฒนาต่อ (ค่าเริ่มต้น)
2. icu -  engine ตัวดั้งเดิมของ PyThaiNLP (ความแม่นยำต่ำ)
3. dict - เป็นการตัดคำโดยใช้พจานุกรมจาก thaiword.txt ใน corpus  (ความแม่นยำปานกลาง) **จะคืนค่า False หากข้อความนั้นไม่สามารถตัดคำได้**
4. longest-matching ใช้ Longest matching ในการตัดคำ
5. mm - ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย - API ชุดเก่า **อยู่ในหมวดบำรุงรักษาเท่านั้น**
6. pylexto ใช้ LexTo ในการตัดคำ โดยเป็น Longest matching
7. deepcut ใช้ deepcut จาก https://github.com/rkcosmos/deepcut ในการตัดคำภาษาไทย
8. wordcutpy ใช้ wordcutpy (https://github.com/veer66/wordcutpy) ในการตัดคำ

คืนค่าเป็น ''list'' เช่น ['แมว','กิน']

**ตัวอย่าง**

```
สำหรับผู้ใช้งาน Python 2.7 ให้ทำการ encode ให้เป็น UTF-8 ก่อนใช้งานโมดูล PyThaiNLP

เช่น text=u'ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด'
```

**การใช้งาน**

```python
from pythainlp.tokenize import word_tokenize
text='ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด'
a=word_tokenize(text,engine='icu') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอ', 'เค', 'บ่', 'พวก', 'เรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้าน', 'เกิด']
b=word_tokenize(text,engine='dict') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
c=word_tokenize(text,engine='mm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
d=word_tokenize(text,engine='pylexto') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
e=word_tokenize(text,engine='newmm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
g=word_tokenize(text,engine='wordcutpy') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้านเกิด']
```

#### dict_word_tokenize

```python
from pythainlp.tokenize import dict_word_tokenize
dict_word_tokenize(text,file,engine)
```

เป็นคำสั่งสำหรับตัดคำโดยใช้ข้อมูลที่ผู้ใช้กำหนด

text คือ ข้อความที่ต้องการตัดคำ

file คือ ที่ตั้งไฟล์ที่ต้องการมาเป็นฐานข้อมูลตัดคำ

engine คือ เครื่องมือตัดคำ

- newmm ตัดคำด้วย newmm
- wordcutpy ใช้ wordcutpy (https://github.com/veer66/wordcutpy) ในการตัดคำ
- mm ตัดคำด้วย mm
- longest-matching ตัดคำโดยใช้ longest matching

ตัวอย่างการใช้งาน https://gist.github.com/wannaphongcom/1e862583051bf0464b6ef4ed592f739c

```
สำหรับผู้ใช้งาน Python 2.7 ให้ทำการ encode ให้เป็น UTF-8 ก่อนใช้งานโมดูล PyThaiNLP

เช่น text=u'ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด'
```

#### sent_tokenize

ใช้ตัดประโยคภาษาไทย

```python
sent_tokenize(text,engine='whitespace+newline')
```

text คือ ข้อความในรูปแบบสตริง

engine คือ เครื่องมือสำหรับใช้ตัดประโยค

- whitespace ตัดประโยคจากช่องว่าง
- whitespace+newline ตัดประโยคจากช่องว่างและตัดจากการขึ้นบรรทัดใหม่

คืนค่า ออกมาเป็น list

#### WhitespaceTokenizer

ใช้ตัดคำ/ประโยคจากช่องว่างในสตริง

```python
>>> from pythainlp.tokenize import WhitespaceTokenizer
>>> WhitespaceTokenizer("ทดสอบ ตัดคำช่องว่าง")
['ทดสอบ', 'ตัดคำช่องว่าง']
```

```
สำหรับผู้ใช้งาน Python 2.7 ให้ทำการ encode ให้เป็น UTF-8 ก่อนใช้งานโมดูล PyThaiNLP

เช่น WhitespaceTokenizer(u"ทดสอบ ตัดคำช่องว่าง")
```



#### isthai

ใช้เช็คข้อความว่าเป็นภาษาไทยทั้งหมดกี่ %

```python
isthai(text,check_all=False)
```

text คือ ข้อความหรือ list ตัวอักษร

check_all สำหรับส่งคืนค่า True หรือ False เช็คทุกตัวอักษร

**การส่งคืนค่า**

```python
{'thai':% อักษรภาษาไทย,'check_all':tuple โดยจะเป็น (ตัวอักษร,True หรือ False)}
```

#### Thai Character Clusters (TCC)

รองรับ Thai Character Clusters (TCC) โดยจะแบ่งกลุ่มด้วย /

**เครดิต**

TCC : Mr.Jakkrit TeCho

grammar : คุณ Wittawat Jitkrittum (https://github.com/wittawatj/jtcc/blob/master/TCC.g)

โค้ด : คุณ Korakot Chaovavanich 

**การใช้งาน**

```python
>>> from pythainlp.tokenize import tcc
>>> tcc.tcc('ประเทศไทย')
'ป/ระ/เท/ศ/ไท/ย'
```

#### Enhanced Thai Character Cluster (ETCC)

นอกจาก TCC แล้ว PyThaiNLP 1.4 ยังรองรับ Enhanced Thai Character Cluster (ETCC) โดยแบ่งกลุ่มด้วย /

**การใช้งาน**

```python
>>> from pythainlp.tokenize import etcc
>>> etcc.etcc('คืนความสุข')
'/คืน/ความสุข'
```

### tag

เป็น Part-of-speech tagging ภาษาไทย

```python
from pythainlp.tag import pos_tag
pos_tag(text,engine='unigram',corpus='orchid')
```

list คือ list ที่เก็บข้อความหลังผ่านการตัดคำแล้ว

engine คือ ชุดเครื่องมือในการ postaggers มี 2 ตัวดังนี้

1. unigram เป็น UnigramTagger (ค่าเริ่มต้น)
2. perceptron เป็น PerceptronTagger
3. artagger เป็น RDR POS Tagger ละเอียดยิ่งกว่าเดิม รองรับเฉพาะ Python 3 เท่านั้น

corpus ที่รองรับ

1. orchid
2. pud ใช้ข้อมูล  Parallel Universal Dependencies (PUD) treebanks

### summarize

เป็นระบบสรุปเอกสารภาษาไทยแบบง่าย ๆ

summarize_text(text,n,engine='frequency')

    text เป็นข้อความ
    n คือ จำนวนประโยคสรุป
    engine ที่รองรับ
    - frequency
**การใช้งาน**

```python
>>> from pythainlp.summarize import summarize_text
>>> summarize_text(text="อาหาร หมายถึง ของแข็งหรือของเหลว ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว จะทำให้เกิดพลังงานและความร้อนยเจริญเติบโต ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ อาหารจะต้องงกาย",n=1,engine='frequency')
['อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย']
```

### word_vector

```python
from pythainlp.word_vector import thai2vec
```

word_vector เป็นระบบ word vector ใน PyThaiNLP

ปัจจุบันนี้รองรับเฉพาะ thai2vec (https://github.com/cstorm125/thai2vec)

thai2vec พัฒนาโดยคุณ Charin Polpanumas

#### thai2vec

ความต้องการโมดูล

- gensim
- numpy

##### API

- get_model() - รับข้อมูล model ในรูปแบบของ gensim
- most_similar_cosmul(positive,negative)
- doesnt_match(listdata)
- similarity(word1,word2) - หาค่าความคล้ายกันระหว่าง 2 คำ โดยทั้งคู่เป็น str
- sentence_vectorizer(ss,dim=300,use_mean=False)
- about() - รายละเอียด thai2vec



### keywords

ใช้หา keywords จากข้อความภาษาไทย

#### find_keyword

การทำงาน หาคำที่ถูกใช้งานมากกว่าค่าขั้นต่ำที่กำหนดได้ โดยจะลบ stopword ออกไป

```python
find_keyword(word_list,lentext=3)
```

word_list คือ list ของข้อความที่ผ่านการตัดคำแล้ว

lentext คือ จำนวนคำขั้นต่ำที่ต้องการหา keyword

คืนค่าออกมาเป็น dict

### romanization

```python
from pythainlp.romanization import romanization
romanization(str,engine='royin')
```
มี 2 engine ดังนี้

- pyicu ส่งค่า Latin
- royin ใช้หลักเกณฑ์การถอดอักษรไทยเป็นอักษรโรมัน ฉบับราชบัณฑิตยสถาน (**หากมีข้อผิดพลาด ให้ใช้คำอ่าน เนื่องจากตัว royin ไม่มีตัวแปลงคำเป็นคำอ่าน**) 

data :

รับค่า ''str'' ข้อความ 

คืนค่าเป็น ''str'' ข้อความ

**ตัวอย่าง**

```python
from pythainlp.romanization import romanization
romanization("แมว") # 'maew'
```

### spell 

เป็น API สำหรับเช็คคำผิดในภาษาไทย 

```python
spell(word,engine='pn')
```

engine ที่รองรับ

- pn พัฒนามาจาก Peter Norvig (ค่าเริ่มต้น)
- hunspell ใช้ hunspell (ไม่รองรับ Python 2.7)

**ตัวอย่างการใช้งาน**

```python
from pythainlp.spell import *
a=spell("สี่เหลียม")
print(a) # ['สี่เหลี่ยม']
```
#### pn

```python
correction(word)
```

แสดงคำที่เป็นไปได้มากที่สุด

**ตัวอย่างการใช้งาน**

```python
from pythainlp.spell.pn import correction
a=correction("สี่เหลียม")
print(a) # ['สี่เหลี่ยม']
```

ผลลัพธ์

```
สี่เหลี่ยม
```

### pythainlp.number

```python
from pythainlp.number import *
```
จัดการกับตัวเลข โดยมีดังนี้

- thai_num_to_num(str)  - เป็นการแปลงเลขไทยสู่เลข
- thai_num_to_text(str) - เลขไทยสู่ข้อความ
- num_to_thai_num(str) - เลขสู่เลขไทย
- num_to_text(str) - เลขสู่ข้อความ
- text_to_num(str) - ข้อความสู่เลข
- numtowords(float) -  อ่านจำนวนตัวเลขภาษาไทย (บาท) รับค่าเป็น ''float'' คืนค่าเป็น  'str'

### collation

ใช้ในการเรียงลำดับข้อมูลภาษาไทยใน List

```python
from pythainlp.collation import collation
print(collation(['ไก่','ไข่','ก','ฮา'])) # ['ก', 'ไก่', 'ไข่', 'ฮา']
```

รับ list คืนค่า list

### date

#### now

รับเวลาปัจจุบันเป็นภาษาไทย

```python
from pythainlp.date import now
now() # '30 พฤษภาคม 2560 18:45:24'
```
### rank

#### rank

หาคำที่มีจำนวนการใช้งานมากที่สุด

```python
from pythainlp.rank import rank
rank(list)
```

คืนค่าออกมาเป็น dict

**ตัวอย่างการใช้งาน**

```python
>>> rank(['แมง','แมง','คน'])
Counter({'แมง': 2, 'คน': 1})
```

### change

#### แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา

```python
from pythainlp.change import *
```

มีคำสั่งดังนี้

- texttothai(str) แปลงแป้นตัวอักษรภาษาอังกฤษเป็นภาษาไทย
- texttoeng(str) แปลงแป้นตัวอักษรภาษาไทยเป็นภาษาอังกฤษ

คืนค่าออกมาเป็น str

### soundex

เดติด คุณ Korakot Chaovavanich (จาก https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8)

กฎที่รองรับในเวชั่น 1.4

- กฎการเข้ารหัสซาวน์เด็กซ์ของ  วิชิตหล่อจีระชุณห์กุล  และ  เจริญ  คุวินทร์พันธุ์ - LK82
- กฎการเข้ารหัสซาวน์เด็กซ์ของ วรรณี อุดมพาณิชย์ - Udom83

**การใช้งาน**

```python
>>> from pythainlp.soundex import LK82,Udom83
>>> print(LK82('รถ'))
ร3000
>>> print(LK82('รด'))
ร3000
>>> print(LK82('จัน'))
จ4000
>>> print(LK82('จันทร์'))
จ4000
>>> print(Udom83('รถ'))
ร800000
```

### Meta Sound ภาษาไทย

```
Snae & Brückner. (2009). Novel Phonetic Name Matching Algorithm with a Statistical Ontology for Analysing Names Given in Accordance with Thai Astrology. Retrieved from https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf
```

**การใช้งาน**

```python
>>> from pythainlp.MetaSound import *
>>> MetaSound('คน')
'15'
```

### sentiment

เป็น Sentiment analysis ภาษาไทย ใช้ข้อมูลจาก [https://github.com/wannaphongcom/lexicon-thai/tree/master/ข้อความ/](https://github.com/wannaphongcom/lexicon-thai/tree/master/ข้อความ/)

```python
from pythainlp.sentiment import sentiment
sentiment(str)
```

รับค่า str ส่งออกเป็น pos , neg

### Util

การใช้งาน

```python
from pythainlp.util import *
```

#### ngrams

สำหรับสร้าง n-grams 

```python
ngrams(token,num)
```

- token คือ list
- num คือ จำนวน ngrams

#### bigrams

สำหรับสร้าง bigrams

```python
bigrams(token)
```

- token คือ list

#### trigram

สำหรับสร้าง trigram

```python
trigram(token)
```

- token คือ list

#### normalize

ซ่อมข้อความภาษาไทย เช่น กี่่่ ไปเป็น กี่

```python
normalize(text)
```

**ตัวอย่าง**

```python
>>> print(normalize("เเปลก")=="แปลก") # เ เ ป ล ก กับ แปลก
True
```

#### listtext_num2num

แปลง list ข้อความตัวเลขในภาษาไทยให้เป็นตัวเลข

```python
listtext_num2num(list)
```

**ตัวอย่าง**

```python
>>> listtext_num2num(['หก','ล้าน','หกแสน','หกหมื่น','หกพัน','หกร้อย','หกสิบ','หก'])
6666666
```

### Corpus

#### WordNet ภาษาไทย

เรียกใช้งาน

```python
from pythainlp.corpus import wordnet
```

**การใช้งาน**

API เหมือนกับ NLTK โดยรองรับ API ดังนี้

- wordnet.synsets(word)
- wordnet.synset(name_synsets)
- wordnet.all_lemma_names(pos=None, lang="tha")
- wordnet.all_synsets(pos=None)
- wordnet.langs()
- wordnet.lemmas(word,pos=None,lang="tha")
- wordnet.lemma(name_synsets)
- wordnet.lemma_from_key(key)
- wordnet.path_similarity(synsets1,synsets2)
- wordnet.lch_similarity(synsets1,synsets2)
- wordnet.wup_similarity(synsets1,synsets2)
- wordnet.morphy(form, pos=None)
- wordnet.custom_lemmas(tab_file, lang)

**ตัวอย่าง**

```python
>>> from pythainlp.corpus import wordnet
>>> print(wordnet.synsets('หนึ่ง'))
[Synset('one.s.05'), Synset('one.s.04'), Synset('one.s.01'), Synset('one.n.01')]
>>> print(wordnet.synsets('หนึ่ง')[0].lemma_names('tha'))
[]
>>> print(wordnet.synset('one.s.05'))
Synset('one.s.05')
>>> print(wordnet.synset('spy.n.01').lemmas())
[Lemma('spy.n.01.spy'), Lemma('spy.n.01.undercover_agent')]
>>> print(wordnet.synset('spy.n.01').lemma_names('tha'))
['สปาย', 'สายลับ']
```

#### stopword ภาษาไทย

```python
from pythainlp.corpus import stopwords
stopwords = stopwords.words('thai')
```

#### ชื่อประเทศ ภาษาไทย

```python
from pythainlp.corpus import country
country.get_data()
```

#### ตัววรรณยุกต์ในภาษาไทย

```python
from pythainlp.corpus import tone
tone.get_data()
```

#### ตัวพยัญชนะในภาษาไทย

```python
from pythainlp.corpus import alphabet
alphabet.get_data()
```

#### รายการคำในภาษาไทย

```python
from pythainlp.corpus.thaiword import get_data # ข้อมูลเก่า
get_data()
from pythainlp.corpus.newthaiword import get_data # ข้อมูลใหม่
get_data()
```

#### provinces

สำหรับจัดการชื่อจังหวัดในประเทศไทย

##### get_data

รับข้อมูลชื่อจังหวัดในประเทศไทบ

```python
get_data()
```

คือค่าออกมาเป็น list

##### parsed_docs

สำหรับใช้ Tag ชื่อจังหวัดในประเทศไทย

```python
parsed_docs(text_list)
```

text_list คือ ข้อความภาษาไทยที่อยู่ใน list โดยผ่านการตัดคำมาแล้ว

**ตัวอย่าง**

```python
>>> d=['หนองคาย', 'เป็น', 'เมือง', 'น่าอยู่', 'อันดับ', 'ต้น', 'ๆ', 'ของ', 'โลก', 'นอกจากนี้', 'ยัง', 'มี', 'เชียงใหม่']
>>> parsed_docs(d)
["[LOC : 'หนองคาย']", 'เป็น', 'เมือง', 'น่าอยู่', 'อันดับ', 'ต้น', 'ๆ', 'ของ', 'โลก', 'นอกจากนี้', 'ยัง', 'มี', "[LOC : 'เชียงใหม่']"]
```

#### ConceptNet

เครื่องมือสำหรับ ConceptNet

**ค้นหา edges**

```python
edges(word,lang='th')
```

return dict

#### TNC

สำหรับใช้จัดการกับ Thai National Corpus (http://www.arts.chula.ac.th/~ling/TNC/index.php)

##### word_frequency

ใช้วัดความถี่ของคำ

```python
word_frequency(word,domain='all')
```

word คือ คำ

domain คือ หมวดหมู่ของคำ

มีหมวดหมู่ดังนี้

- all
- imaginative
- natural-pure-science
- applied-science
- social-science
- world-affairs-history
- commerce-finance
- arts
- belief-thought
- leisure
- others

เขียนโดย PyThaiNLP
