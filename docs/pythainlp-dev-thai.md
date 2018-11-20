# คู่มือการใช้งาน PyThaiNLP

[TOC]

โมดูล PyThaiNLP เป็นโมดูลที่ถูกพัฒนาขึ้นเพื่อประมวลภาษาไทยด้วยภาษาโปรแกรม Python และ**มันฟรี (ตลอดไป) เพื่อคนไทยและชาวโลกทุกคน!**

> เพราะโลกขับเคลื่อนต่อไปด้วยการแบ่งปัน

รองรับ Python 3.4 ขึ้นไปเท่านั้น

ติดตั้งโดยใช้คำสั่ง

```
pip install pythainlp
```

ปัจจุบัน PyThaiNLP ไม่จำเป็นต้องใช้ PyICU แล้ว แต่หากท่านต้องการใช้ API ที่มี PyICU ให้ทำตามคำแนะนำข้างล่างนี้

**ติดตั้ง PyICU บน Windows**

การติดตั้ง PyThaiNLP บน Windows ต้องติดตั้ง PyICU ก่อน วิธีที่ง่ายที่สุดคือใช้ wheel ที่ถูกสร้างมาก่อนแล้ว

1. ดาวน์โหลด wheel ตามแพลตฟอร์มที่ต้องการจาก [http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu) เช่น Python x64 3.6 บน Windows ให้ใช้ PyICU‑2.x‑cp36‑cp36m‑win_amd64.whl

2. `pip install PyICU‑2.1‑cp36‑cp36m‑win_amd64.whl`

3. `pip install pythainlp`

**ติดตั้ง PyICU บน macOS**

```sh
brew install icu4c --force
brew link --force icu4c
CFLAGS=-I/usr/local/opt/icu4c/include LDFLAGS=-L/usr/local/opt/icu4c/lib pip install pythainlp
```

ข้อมูลเพิ่มเติมที่ https://medium.com/data-science-cafe/install-polyglot-on-mac-3c90445abc1f

## API

### tokenize

#### word_tokenize

ตัดคำภาษาไทย

```python
from pythainlp.tokenize import word_tokenize

word_tokenize(text, engine)
```
text คือ ข้อความในรูปแบบสตริง str เท่านั้น

engine คือ ระบบตัดคำ ปัจจุบันมี engine ดังนี้

- newmm (ค่าเริ่มต้น) - ใช้พจนานุกรม ด้วยวิธี Maximum Matching + Thai Character Cluster โค้ดชุดใหม่[โดยคุณ Korakot Chaovavanich](https://www.facebook.com/groups/408004796247683/permalink/431283740586455/)
- longest - ใช้พจนานุกรม ด้วยวิธี Longest Matching
- icu - เรียกใช้ตัวตัดคำจาก ICU ใช้พจนานุกรม (ความแม่นยำต่ำ)
- deepcut - เรียกใช้ตัวตัดคำจาก [deepcut](https://github.com/rkcosmos/deepcut) ใช้การเรียนรู้ของเครื่อง

คืนค่าเป็น ''list'' เช่น ['แมว', 'กิน']

**การใช้งาน**

```python
from pythainlp.tokenize import word_tokenize

text = "โอเคบ่เรารักภาษาถิ่น"
word_tokenize(text, engine="newmm")  # ['โอเค', 'บ่', 'เรา', 'รัก', 'ภาษาถิ่น']
word_tokenize(text, engine="icu")  # ['โอ', 'เค', 'บ่', 'เรา', 'รัก', 'ภาษา', 'ถิ่น']
```

#### dict_word_tokenize

ตัดคำโดยใช้พจนานุกรมที่ผู้ใช้กำหนด

```python
from pythainlp.tokenize import dict_word_tokenize
dict_word_tokenize(text, filename, engine)
```

text คือ ข้อความที่ต้องการตัดคำ

filename คือ ที่ตั้งไฟล์ที่ต้องการมาเป็นฐานข้อมูลตัดคำ

engine คือ ระบบตัดคำ (ดูรายละเอียดที่ word_tokenize)
- newmm
- longest

ตัวอย่างการใช้งาน https://gist.github.com/wannaphongcom/1e862583051bf0464b6ef4ed592f739c


#### sent_tokenize

ตัดประโยคภาษาไทย

```python
sent_tokenize(text, engine="whitespace+newline")
```

text คือ ข้อความในรูปแบบสตริง

engine คือ เครื่องมือสำหรับใช้ตัดประโยค

- whitespace ตัดประโยคจากช่องว่าง
- whitespace+newline ตัดประโยคจากช่องว่างและตัดจากการขึ้นบรรทัดใหม่

คืนค่าเป็น list

#### WhitespaceTokenizer

ใช้ตัดคำ/ประโยคจากช่องว่างในสตริง

```python
from pythainlp.tokenize import WhitespaceTokenizer

WhitespaceTokenizer("ทดสอบ ตัดคำช่องว่าง")  # ['ทดสอบ', 'ตัดคำช่องว่าง']
```


#### isthai

ตรวจสอบข้อความว่ามีอักษรไทยร้อยละเท่าใด

```python
isthai(text, check_all=False)
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

- TCC: Jakkrit TeCho
- Grammar: Wittawat Jitkrittum (https://github.com/wittawatj/jtcc/blob/master/TCC.g)
- Python code: Korakot Chaovavanich

**การใช้งาน**

```python
from pythainlp.tokenize import tcc

tcc.tcc("ประเทศไทย")  # 'ป/ระ/เท/ศ/ไท/ย'
```

#### Enhanced Thai Character Cluster (ETCC)

นอกจาก TCC แล้ว PyThaiNLP ยังรองรับ Enhanced Thai Character Cluster (ETCC) โดยแบ่งกลุ่มด้วย /

**การใช้งาน**

```python
from pythainlp.tokenize import etcc

etcc.etcc('คืนความสุข')  # '/คืน/ความสุข'
```

### tag

Part-of-speech tagging ภาษาไทย

```python
from pythainlp.tag import pos_tag

pos_tag(text, engine="unigram", corpus="orchid")
```

list คือ list ที่เก็บข้อความหลังผ่านการตัดคำแล้ว

engine คือ ตัวติดป้ายกำกับคำ (pos tagger) มีดังนี้
- unigram (ค่าเริ่มต้น) - UnigramTagger
- perceptron - PerceptronTagger
- artagger - RDR POS Tagger ละเอียดยิ่งกว่าเดิม

corpus ที่รองรับ
- orchid ใช้ข้อมูลจากคลังคำ ORCHID โดยเนคเทค
- pud ใช้ข้อมูล Parallel Universal Dependencies (PUD) treebanks

### summarize

สรุปเอกสารภาษาไทยแบบง่าย ๆ

```python
summarize(text, n, engine="frequency")
```

text เป็นข้อความ

n คือ จำนวนประโยคสรุป

engine ที่รองรับ
- frequency

**การใช้งาน**

```python
from pythainlp.summarize import summarize

summarize(text="อาหาร หมายถึง ของแข็งหรือของเหลว ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว จะทำให้เกิดพลังงานและความร้อนยเจริญเติบโต ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ อาหารจะต้องงกาย", n=1, engine="frequency")
# ['อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย']
```

### word_vector

สร้างเวกเตอร์คำ

```python
from pythainlp.word_vector import thai2vec
```

ปัจจุบันรองรับเฉพาะ thai2vec (https://github.com/cstorm125/thai2vec)

พัฒนาโดย Charin Polpanumas

#### thai2vec

ต้องการโมดูล
- gensim
- numpy

##### API

- get_model() - รับข้อมูล model ในรูปแบบของ gensim
- most_similar_cosmul(positive, negative)
- doesnt_match(listdata)
- similarity(word1, word2) - หาค่าความคล้ายระหว่าง 2 คำ โดยทั้งคู่เป็น str
- sentence_vectorizer(ss, dim=300, use_mean=False)
- about() - รายละเอียด thai2vec

### keywords

หาคำสำคัญจากข้อความภาษาไทย

#### find_keyword

การทำงาน หาคำที่ถูกใช้งานมากกว่าค่าขั้นต่ำที่กำหนดได้ โดยจะลบ stopword ออก

```python
from pythainlp.util import find_keyword

find_keyword(word_list, lentext=3)
```

word_list คือ list ของข้อความที่ตัดคำแล้ว

lentext คือ จำนวนคำขั้นต่ำที่ต้องการหา keyword

คืนค่าเป็น dict

### transliteration

```python
from pythainlp.transliterate import romanize, transliterate

romanize(str, engine="royin")
transliterate(str, engine="pyicu")
```

มี engine ดังนี้
- pyicu ส่งค่าสัทอักษร
- royin ใช้หลักเกณฑ์การถอดอักษรไทยเป็นอักษรโรมัน ฉบับราชบัณฑิตยสถาน (**หากมีข้อผิดพลาด ให้ใช้คำอ่าน เนื่องจากตัว royin ไม่มีตัวแปลงคำเป็นคำอ่าน**)

รับค่า ''str'' ข้อความ

คืนค่าเป็น ''str'' ข้อความ

**ตัวอย่าง**

```python
from pythainlp.transliterate import romanize, transliterate

romanize("แมว")  # 'maew'
transliterate("นก")
```

### spell

ตรวจสอบคำผิดในภาษาไทย

```python
spell(word, engine="pn")
```

engine ที่รองรับ
- pn (ค่าเริ่มต้น) พัฒนาจาก Peter Norvig

**ตัวอย่างการใช้งาน**

```python
from pythainlp.spell import spell

a = spell("สี่เหลียม")
print(a)  # ['สี่เหลี่ยม']
```
#### pn

```python
correct(word)
```

จะคืนค่าคำที่เป็นไปได้มากที่สุด

**ตัวอย่างการใช้งาน**

```python
from pythainlp.spell.pn import correct

a = correct("สี่เหลียม")
print(a)  # ['สี่เหลี่ยม']
```

### pythainlp.number

จัดการกับตัวเลข

```python
from pythainlp.number import *
```

มีฟังก์ชันดังนี้
- thai_num_to_num(str) - แปลงเลขไทยสู่เลขอารบิก
- thai_num_to_text(str) - เลขไทยสู่คำอ่านไทย
- num_to_thai_num(str) - เลขอารบิกสู่เลขไทย
- num_to_text(str) - เลขสู่ข้อความ
- text_to_num(str) - ข้อความสู่เลข
- bahttext(float) - อ่านจำนวนภาษาไทย (หน่วยเงินบาท) รับค่าเป็น ''float'' คืนค่าเป็น 'str'
- num_to_thaiword(float) - อ่านจำนวนภาษาไทย รับค่าเป็น ''float'' คืนค่าเป็น 'str'
- thaiword_to_num(List[str]) - แปลคำอ่านจำนวนไทยเป็นตัวเลขจำนวนเต็ม รับค่าเป็น ''List[str]'' คืนค่าเป็น int

**ตัวอย่าง**

```python
thaiword_to_num(["หกหมื่น", "หกพัน", "หกร้อย", "หกสิบ", "หก"])  # 66666
```

### collation

เรียงลำดับข้อมูลภาษาไทยใน List

```python
from pythainlp.util import collate
print(collate(["ไก่", "ไข่", "กา", "ฮา"]))  # ['กา', 'ไก่', 'ไข่', 'ฮา']
```

รับ list คืนค่า list

### date

#### thai_strftime

จัดรูปแบบข้อความบอกวันที่และเวลาเป็นภาษาไทยและปีพุทธศักราช

```python
import datetime
from pythainlp.util import thai_strftime

fmt = "%Aที่ %-d %B พ.ศ. %Y เวลา %H:%Mน. (%a %d-%b-%y)"
date = datetime.datetime(1976, 10, 6, 1, 40)
print(thai_strftime(date, fmt))
# วันพุธที่ 6 ตุลาคม พ.ศ. 2519 เวลา 01:40น. (พ 06-ต.ค.-19)
```
### rank

#### rank

หาคำที่มีจำนวนการใช้งานมากที่สุด

```python
from pythainlp.util import rank

rank(list)
```

คืนค่าออกมาเป็น dict

**ตัวอย่างการใช้งาน**

```python
rank(["แมง", "แมง", "คน"])  # Counter({'แมง': 2, 'คน': 1})
```

### soundex

กฎที่รองรับ
- lk82 - กฎการเข้ารหัสซาวน์เด็กซ์ของ วิชิตหล่อจีระชุณห์กุล และ เจริญ คุวินทร์พันธุ์
- udom83 - กฎการเข้ารหัสซาวน์เด็กซ์ของ วรรณี อุดมพาณิชย์
- metasound - กฎการเข้ารหัส MetaSoound ของ Snae & Brückner (2009)

เครดิต
- โค้ด lk82 และ udom83 - Korakot Chaovavanich https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8
- โค้ด metasound - Wannaphong Phattiyaphaibun, ปรับปรุงต่อโดย Arthit Suriyawongkul

**การใช้งาน**

```python
from pythainlp.soundex import lk82, metasound, udom83

print(lk82("รถ"))  # ร3000
print(lk82("รด"))  # ร3000
print(lk82("จัน"))  # จ4000
print(lk82("จันทร์"))  # จ4000
print(udom83("รถ"))  # ร800000
print(metasound("รัก"))  # 'ร100'
```

### Util

#### normalize

ซ่อมข้อความภาษาไทย

```python
normalize(text)
```

**ตัวอย่าง**

```python
from pythainlp.util import normalize

# เ เ ป ล ก กับ แปลก
normalize("เเปลก") == "แปลก"  # True
```

#### แก้ไขปัญหาการลืมเปลี่ยนภาษาแป้นพิมพ์

```python
from pythainlp.util import eng_to_thai, thai_to_eng
```

มีคำสั่งดังนี้

- eng_to_thai(str) แปลงแป้นตัวอักษรอังกฤษเป็นไทย
- thai_to_eng(str) แปลงแป้นตัวอักษรไทยเป็นอังกฤษ

คืนค่าออกมาเป็น str

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
from pythainlp.corpus import wordnet

print(wordnet.synsets("หนึ่ง"))
# [Synset('one.s.05'), Synset('one.s.04'), Synset('one.s.01'), Synset('one.n.01')]

print(wordnet.synsets("หนึ่ง")[0].lemma_names("tha"))
# []

print(wordnet.synset("one.s.05"))
# Synset('one.s.05')

print(wordnet.synset("spy.n.01").lemmas())
# [Lemma('spy.n.01.spy'), Lemma('spy.n.01.undercover_agent')]

print(wordnet.synset("spy.n.01").lemma_names("tha"))
# ['สปาย', 'สายลับ']
```

#### พยัญชนะในภาษาไทย

```python
from pythainlp import thai_consonants
```

จะได้ str ที่มีพยัญชนะในภาษาไทยทั้งหมด

#### วรรณยุกต์ในภาษาไทย

```python
from pythainlp import thai_tonemarks
```
จะได้ str ที่มีวรรณยุกต์ในภาษาไทยทั้งหมด

#### stopword ภาษาไทย

```python
from pythainlp.corpus import thai_stopwords

stopwords = thai_stopwords()
```

#### รายการคำในภาษาไทย

```python
from pythainlp.corpus import thai_words

words = thai_words()
```

#### ชื่อประเทศ ภาษาไทย

```python
from pythainlp.corpus import countries

for country in countries():
    print(country)
```

#### provinces

ข้อมูลชื่อจังหวัดในประเทศไทย

```python
from pythainlp.corpus import provinces

for province in provinces():
    print(province)
```

##### tag_provinces

สำหรับใช้ติดป้ายกำกับชื่อจังหวัดในประเทศไทย

```python
from pythainlp.tag.locations import tag_provinces

tag_provinces(text_list)
```

text_list คือ ข้อความภาษาไทยที่อยู่ใน list โดยผ่านการตัดคำมาแล้ว

**ตัวอย่าง**
```python
text = ['หนองคาย', 'น่าอยู่']
tag_provinces(text)
# [('หนองคาย', 'B-LOCATION'), ('น่าอยู่', 'O')]  
```

#### ConceptNet

เครื่องมือสำหรับ ConceptNet

**ค้นหา edges**

```python
edges(word, lang="th")
```

return dict

#### TNC

สำหรับใช้จัดการกับ Thai National Corpus (http://www.arts.chula.ac.th/~ling/TNC/index.php)

##### word_freq

ใช้วัดความถี่ของคำ

```python
word_freq(word, domain="all")
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
