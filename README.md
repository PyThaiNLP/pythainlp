# PyThaiNLP
[![PyPI Downloads](https://img.shields.io/pypi/dm/pythainlp.png)]
[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/wannaphongcom/pythainlp.svg?branch=develop)](https://travis-ci.org/wannaphongcom/pythainlp)

Homepages :[https://sites.google.com/view/pythainlp/home](https://sites.google.com/view/pythainlp/home)

# English

Thai NLP in python package. 

Thai Natural language processing in Python language.

Supports Python 3.4 +

  - Document : [https://pythonhosted.org/pythainlp/](https://pythonhosted.org/pythainlp/)
  - GitHub Home :  [https://github.com/wannaphongcom/pythainlp](https://github.com/wannaphongcom/pythainlp)

### Project status

Developing

### Version
1.1

### Capabilities
  - Thai Segment 
  - Thai to Latin
  - Thai Postaggers
  - Read a number to text in Thai language
  - Sort the words of a sentence
  - Fix the printer forgot to change the language
  - Check the wrong words in Thai languag
  - And more.

# Install

Supports Python 3.4 +

Stable version

```sh
$ pip install pythainlp
```


# Document

Sample usage

```python
# Thai Segment 
from pythainlp.segment import segment
a = 'ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'
b = segment(a)
print(b) # ['ฉัน', 'รัก', 'ภาษาไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คนไทย']
# Thai Postaggers
from pythainlp.postaggers import tag
print(tag('คุณกำลังประชุม')) # [('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')]
# Find the number word of the most
from pythainlp.rank import rank
aa = rank(b)
print(aa) # Counter({'ฉัน': 2, 'ไทย': 2, 'เป็น': 1, 'รัก': 1, 'ภาษา': 1, 'เพราะ': 1, 'คน': 1})
# Thai to Latin
from pythainlp.romanization import romanization
b=romanization("แมว")
print(b) # mæw
# Fix the printer forgot to change the language
from pythainlp.change import *
a="l;ylfu8iy["
a=texttothai(a)
b="นามรสนอำันี"
b=texttoeng(b)
print(a) # สวัสดีครับ
print(b) # ok,iloveyou
# Read a number to text in Thai language
from pythainlp.number import numtowords
print("5611116.50")
print(numtowords(5611116.50)) # ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์
```

### License

Apache Software License 2.0

# Thai

Thai NLP in python package. 

Natural language processing หรือ การประมวลภาษาธรรมชาติ  โมดูล PyThaiNLP เป็นโมดูลที่ถูกพัฒนาขึ้นเพื่องานวิจัยและพัฒนาการประมวลภาษาธรรมชาติภาษาไทยในภาษา Python

รองรับ Python 3.4 ขึ้นไป

  - เอกสารการใช้งาน : [https://pythonhosted.org/pythainlp/](https://pythonhosted.org/pythainlp/)
  - หน้าหลัก GitHub :  [https://github.com/wannaphongcom/pythainlp](https://github.com/wannaphongcom/pythainlp)

### สถานะโครงการ

กำลังพัฒนา 

### Version
1.1

### ความสามารถ
  - ตัดคำภาษาไทย
  - ถอดเสียงภาษาไทยเป็น Latin
  - Postaggers ภาษาไทย
  - อ่านตัวเลขเป็นข้อความภาษาไทย
  - เรียงจำนวนคำของประโยค
  - แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา
  - เช็คคำผิดในภาษาไทย
  - และอื่น ๆ 

# ติดตั้ง

รองรับ Python 3.4 ขึ้นไป

รุ่นเสถียร

```sh
$ pip install pythainlp
```

# เอกสารการใช้งานเบื้องต้น

ตัวอย่างการใช้งาน

```python
# ตัดคำ
from pythainlp.segment import segment
a = 'ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'
b = segment(a)
print(b) # ['ฉัน', 'รัก', 'ภาษาไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คนไทย']
# Postaggers ภาษาไทย
from pythainlp.postaggers import tag
print(tag('คุณกำลังประชุม')) # [('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')]
# หาคำที่มีจำนวนการใช้งานมากที่สุด
from pythainlp.rank import rank
aa = rank(b)
print(aa) # Counter({'ฉัน': 2, 'ไทย': 2, 'เป็น': 1, 'รัก': 1, 'ภาษา': 1, 'เพราะ': 1, 'คน': 1})
# ถอดเสียงภาษาไทยเป็น Latin
from pythainlp.romanization import romanization
b=romanization("แมว")
print(b) # mæw
# แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา
from pythainlp.change import *
a="l;ylfu8iy["
a=texttothai(a)
b="นามรสนอำันี"
b=texttoeng(b)
print(a) # สวัสดีครับ
print(b) # ok,iloveyou
# เปลี่ยนตัวเลขเป็นตัวอักษรภาษาไทย (เงินบาท)
from pythainlp.number import numtowords
print("5611116.50")
print(numtowords(5611116.50)) # ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์
```

### License

Apache Software License 2.0


พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์

### สนับสนุน

คุณสามารถร่วมพัฒนาโครงการนี้ได้ โดยการ Fork และส่ง pull requests กลับมา