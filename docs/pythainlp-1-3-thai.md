# คู่มือการใช้งาน PyThaiNLP 1.3

รองรับเฉพาะ Python 3.4 ขึ้นไปเท่านั้น

ติดตั้งใช้คำสั่ง

```
pip install pythainlp
```

**วิธีติดตั้งสำหรับ Windows**

ให้ทำการติดตั้ง pyicu โดยใช้ไฟล์ .whl จาก [http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu) 

หากใช้ python 3.5 64 bit ให้โหลด PyICU‑1.9.7‑cp35‑cp35m‑win_amd64.whl แล้วเปิด cmd ใช้คำสั่ง

```
pip install PyICU‑1.9.7‑cp35‑cp35m‑win_amd64.whl
```

แล้วจึงใช้ 

```
pip install pythainlp
```

**ติดตั้งบน Mac**

```sh
$ brew install icu4c --force
$ brew link --force icu4c
$ CFLAGS=-I/usr/local/opt/icu4c/include LDFLAGS=-L/usr/local/opt/icu4c/lib pip install pythainlp
```

ข้อมูลเพิ่มเติม [คลิกที่นี้](https://medium.com/data-science-cafe/install-polyglot-on-mac-3c90445abc1f#.rdfrorxjx)

## API

### ตัดคำไทย

สำหรับการตัดคำไทยนั้น ใน PyThaiNLP 1.3 ได้ทำเปลี่ยน API ใหม่ ยกเลิก pythainlp.segment ให้ทำการเปลี่ยนไปใช้ API ชุดใหม่

```python
from pythainlp.tokenize import word_tokenize
word_tokenize(text,engine)
```
text คือ ข้อความในรูปแบบสตริง str เท่านั้น

engine คือ ระบบตัดคำไทย ปัจจุบันนี้ PyThaiNLP ได้พัฒนามี 3 engine ให้ใช้งานกันดังนี้

1. icu -  engine ตัวดั้งเดิมของ PyThaiNLP (ความแม่นยำต่ำ) และเป็นค่าเริ่มต้น
2. dict - เป็นการตัดคำโดยใช้พจานุกรมจาก thaiword.txt ใน corpus  (ความแม่นยำปานกลาง)
3. mm - ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย

คืนค่าเป็น ''list'' เช่น ['แมว','กิน']

**ตัวอย่าง**

```python
from pythainlp.tokenize import word_tokenize
text='ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด'
a=word_tokenize(text,engine='icu') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอ', 'เค', 'บ่', 'พวก', 'เรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้าน', 'เกิด']
b=word_tokenize(text,engine='dict') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
c=word_tokenize(text,engine='mm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
```

### Postaggers ภาษาไทย

ตั้งแต่ PyThaiNLP 1.3 เป็นต้นไป ได้ทำการยกเลิก pythainlp.postaggers เดิม เปลี่ยนไปใช้ API ชุดใหม่ดังนี้

```python
from pythainlp.tag import pos_tag
pos_tag(list,engine='old')
```

list คือ list ที่เก็บข้อความหลังผ่านการตัดคำแล้ว

engine คือ ชุดเครื่องมือในการ postaggers มี 2 ตัวดังนี้

1. old เป็น UnigramTagger (ค่าเริ่มต้น)
2. artagger เป็น RDR POS Tagger ละเอียดยิ่งกว่าเดิม รองรับเฉพาะ Python 3 เท่านั้น

### แปลงข้อความเป็น Latin

```python
from pythainlp.romanization import romanization
romanization(str)
```
**ตัวอย่าง**

```python
from pythainlp.romanization import romanization
romanization("แมว") # 'mæw'
```

### เช็คคำผิด * 

*ความสามารถนี้รองรับเฉพาะ Python 3

ก่อนใช้งานความสามารถนี้ ให้ทำการติดตั้ง hunspell และ hunspell-th ก่อน

**วิธีติดตั้ง** สำหรับบน Debian , Ubuntu

```
sudo apt-get install hunspell hunspell-th
```

บน Mac OS ติดตั้งตามนี้ [http://pankdm.github.io/hunspell.html](http://pankdm.github.io/hunspell.html)

ให้ใช้ pythainlp.spell ตามตัวอย่างนี้

```python
from pythainlp.spell import *
a=spell("สี่เหลียม")
print(a) # ['สี่เหลี่ยม', 'เสียเหลี่ยม', 'เหลี่ยม']
```
### pythainlp.number

```python
from pythainlp.number import *
```
จัดการกับตัวเลข โดยมีดังนี้

- nttn(str)  - เป็นการแปลงเลขไทยสู่เลข
- nttt(str) - เลขไทยสู่ข้อความ
- ntnt(str) - เลขสู่เลขไทย
- ntt(str) - เลขสู่ข้อความ
- ttn(str) - ข้อความสู่เลข
- numtowords(float) -  อ่านจำนวนตัวเลขภาษาไทย (บาท) รับค่าเป็น ''float'' คืนค่าเป็น  'str'

### เรียงลำดับข้อมูลภาษาไทยใน List

```python
from pythainlp.collation import collation
print(collation(['ไก่','ไข่','ก','ฮา'])) # ['ก', 'ไก่', 'ไข่', 'ฮา']
```

รับ list คืนค่า list

### รับเวลาปัจจุบันเป็นภาษาไทย

```python
from pythainlp.date import now
now() # '30 พฤษภาคม 2560 18:45:24'
```
### WordNet ภาษาไทย

เรียกใช้งาน

```python
from pythainlp.corpus import wordnet
```

**รับ Synset**

```python
wordnet.getSynset(คำ)
```

เป็นคำสั่ง ใช้รับ Synset รับค่า str ส่งออกเป็น tuple ('Synset', 'synset li')

**รับคำจาก id**

```python
wordnet.getWords()
```

เป็นคำสั่ง ใช้รับคำจาก ID รับค่า str ส่งออกเป็น tuple ('Word', 'synsetid li')

### stopword ภาษาไทย

```python
from pythainlp.corpus import stopwords
stopwords = stopwords.words('thai')
```

### หาคำที่มีจำนวนการใช้งานมากที่สุด

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

### แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา

```python
from pythainlp.change import *
```

มีคำสั่งดังนี้

- texttothai(str) แปลงแป้นตัวอักษรภาษาอังกฤษเป็นภาษาไทย
- texttoeng(str) แปลงแป้นตัวอักษรภาษาไทยเป็นภาษาอังกฤษ

คืนค่าออกมาเป็น str

### Sentiment analysis ภาษาไทย

ใช้ข้อมูลจาก https://github.com/wannaphongcom/lexicon-thai/tree/master/ข้อความ/

```python
from pythainlp.sentiment import sentiment
sentiment(str)
```

รับค่า str ส่งออกเป็น pos , neg หรือ neutral