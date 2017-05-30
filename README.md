# PyThaiNLP
[![PyPI Downloads](https://img.shields.io/pypi/dm/pythainlp.png)]
[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/wannaphongcom/pythainlp.svg?branch=develop)](https://travis-ci.org/wannaphongcom/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/uxerymgggp1uch0p?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp)


Homepages :[https://sites.google.com/view/pythainlp/home](https://sites.google.com/view/pythainlp/home)

ประมวลภาษาธรรมชาติภาษาไทยในภาษา Python

Natural language processing หรือ การประมวลภาษาธรรมชาติ  โมดูล PyThaiNLP เป็นโมดูลที่ถูกพัฒนาขึ้นเพื่องานวิจัยและพัฒนาการประมวลภาษาธรรมชาติภาษาไทยในภาษา Python

รองรับ Python 2.7 และ Python 3.4 ขึ้นไป

  - เอกสารการใช้งาน : [https://sites.google.com/view/pythainlp/home](https://sites.google.com/view/pythainlp/home)
  - หน้าหลัก GitHub :  [https://github.com/wannaphongcom/pythainlp](https://github.com/wannaphongcom/pythainlp)

### สถานะโครงการ

กำลังพัฒนา 

### Version
1.3

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

รองรับ Python 2.7 และ Python 3.4 ขึ้นไป

รุ่นเสถียร

```sh
$ pip install pythainlp
```

## ติดตั้งบน Mac


```sh
$ brew install icu4c --force
$ brew link --force icu4c
$ CFLAGS=-I/usr/local/opt/icu4c/include LDFLAGS=-L/usr/local/opt/icu4c/lib pip install pythainlp
```

ข้อมูลเพิ่มเติม [คลิกที่นี้](https://medium.com/data-science-cafe/install-polyglot-on-mac-3c90445abc1f#.rdfrorxjx)


# เอกสารการใช้งานเบื้องต้น

### License

Apache Software License 2.0


พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์

### สนับสนุน

คุณสามารถร่วมพัฒนาโครงการนี้ได้ โดยการ Fork และส่ง pull requests กลับมา
