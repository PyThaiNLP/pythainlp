# PyThaiNLP
[![Build Status](https://travis-ci.org/wannaphongcom/pythainlp.svg?branch=master)](https://travis-ci.org/wannaphongcom/pythainlp)
[![Documentation Status](https://readthedocs.org/projects/pythainlp/badge/?version=latest)](http://pythainlp.readthedocs.io/en/latest/?badge=latest)

Thai NLP in python package. 

Natural language processing หรือ การประมวลภาษาธรรมชาติ  โมดูล PyThaiNLP เป็นโมดูลที่ถูกพัฒนาขึ้นเพื่องานวิจัยและพัฒนา การประมวลภาษาธรรมชาติในภาษา Python

รองรับเฉพาะ Python 3 เท่านั้น (Python 2 กำลังพัฒนา)

### Version
0.0.3

### มีอะไรใหม่
แก้ไข bug import ใน python บางรุ่น

### ความสามารถ
  - ตัดคำภาษาไทย
  - อ่านตัวเลขเป็นข้อความภาษาไทย
  - เรียงจำนวนคำของประโยค
  - แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา
  - และอื่น ๆ 

# ติดตั้ง

รองรับเฉพาะ Python 3

```sh
$ git clone https://github.com/wannaphongcom/pythainlp.git
$ cd pythainlp
$ python setup.py install
```

# เอกสารการใช้งานเบื้องต้น

ตัวอย่างการใช้งาน
```python
# ตัดคำ
from pythainlp.segment import segment
a = 'ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'
b = segment(a)
print(b) # ['ฉัน', 'รัก', 'ภาษาไทย', 'เพราะ', 'ฉัน', 'เป็น', 'คนไทย']
# หาคำที่มีจำนวนการใช้งานมากที่สุด
from pythainlp.rank import rank
aa = rank(a)
print(aa) # Counter({'น': 4, 'ั': 3, 'า': 3, 'ร': 2, 'ท': 2, 'ย': 2, 'เ': 2, 'ฉ': 2, 'ไ': 2,
 #'ก': 1, 'พ': 1, 'ป': 1, '็': 1, 'ะ': 1, 'ษ': 1, 'ภ': 1, 'ค': 1})
# ทับศัพท์เสียงไทยในภาษาอังกฤษ (ยังไม่รองรับเสียงสระ)
from pythainlp.romanization import romanization
b=romanization("ต้นกก")
print(b) # tonkok
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

พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลบ์