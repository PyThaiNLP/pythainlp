# เอกสารการใช้งาน

ให้ทำการเรียกใช้โมดูลด้วยคำสั่ง

```python
import pythainlp
```

## การตัดคำภาษาไทย

```python
pythainlp.segment.segment(str)
```

คืนค่าออกมาเป็น list

### ตัวอย่างการใช้งาน

```python
>>> pythainlp.segment.segment('แมวกิน')
['แมว', 'กิน']
```

## Postaggers ภาษาไทย

```python
pythainlp.postaggers.tag(str)
```
คืนค่าออกมาเป็น list


### ตัวอย่างการใช้งาน

```python
>>> pythainlp.postaggers.tag('แมวกินปลา')
[('แมว', 'NCMN'), ('กิน', 'VACT'), ('ปลา', 'NCMN')
```

## ตรวจคำผิด

คุณจะต้องติดตั้ง hunspell ( https://github.com/hunspell/hunspell/ )ในเครื่องของคุณก่อนใช้งานความสามารถนี้

```python
pythainlp.spell.spell(str)
```
ส่งออกเป็น list

## หาคำที่มีจำนวนการใช้งานมากที่สุด

```python
pythainlp.rank.rank(list)
```

คืนค่าออกมาเป็น dict

### ตัวอย่างการใช้งาน

```python
>>> pythainlp.rank.rank(['แมง','แมง','คน'])
Counter({'แมง': 2, 'คน': 1})
```

## ถอดเสียงภาษาไทย

ถอดเสียงภาษาไทยเป็น Latin

```python
pythainlp.romanization.romanization(str)
```

คืนค่าออกมาเป็น str

### ตัวอย่างการใช้งาน

```python
>>> pythainlp.romanization.romanization('แมว')
'mæw'
```

## แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา

```python
pythainlp.change.คำสั่ง()
```

มีคำสั่งดังนี้

  - texttothai(str) แปลงแป้นตัวอักษรภาษาอังกฤษเป็นภาษาไทย
  - texttoeng(str) แปลงแป้นตัวอักษรภาษาไทยเป็นภาษาอังกฤษ

คืนค่าออกมาเป็น str

## เปลี่ยนตัวเลขเป็นตัวอักษรภาษาไทย (เงินบาท)

```python
pythainlp.number.numtowords(float)
```

## เรียงลำดับข้อมูลใน list

```python
pythainlp.collation.collation(list)
```

คืนค่าออกมาเป็น list

### ตัวอย่างการใช้งาน

```python
>>> pythainlp.number.numtowords(169.10)
'หนึ่งร้อยหกสิบเก้าบาทสิบสตางค์'
```

# ตัวอย่างการใช้งาน

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