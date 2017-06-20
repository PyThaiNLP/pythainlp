# PyThaiNLP
[![PyPI Downloads](https://img.shields.io/pypi/dm/pythainlp.png)]
[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/wannaphongcom/pythainlp.svg?branch=develop)](https://travis-ci.org/wannaphongcom/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/uxerymgggp1uch0p?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp)


Homepages :[https://sites.google.com/view/pythainlp/home](https://sites.google.com/view/pythainlp/home)

ประมวลภาษาธรรมชาติภาษาไทยในภาษา Python

Natural language processing หรือ การประมวลภาษาธรรมชาติ  โมดูล PyThaiNLP เป็นโมดูลที่ถูกพัฒนาขึ้นเพื่อพัฒนาการประมวลภาษาธรรมชาติภาษาไทยในภาษา Python และ**มันฟรี (ตลอดไป) เพื่อคนไทยและชาวโลกทุกคน !**

> เพราะโลกขับเคลื่อนต่อไปด้วยการแบ่งปัน

รองรับ Python 3.4 ขึ้นไป

  - เอกสารการใช้งาน : [https://sites.google.com/view/pythainlp/home](https://sites.google.com/view/pythainlp/home)
  - หน้าหลัก GitHub :  [https://github.com/wannaphongcom/pythainlp](https://github.com/wannaphongcom/pythainlp)

### สถานะโครงการ

กำลังพัฒนา 

### Version
1.4

### สิ่งใหม่ที่เพิ่มเข้ามาใน PyThaiNLP 1.4

- รองรับ  Thai Character Clusters (TCC) และ ETCC

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


# เอกสารการใช้งานเบื้องต้น

อ่านได้ที่ https://github.com/wannaphongcom/pythainlp/blob/master/docs/pythainlp-1-4-thai.md

### License

Apache Software License 2.0


พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์

### สนับสนุน

คุณสามารถร่วมพัฒนาโครงการนี้ได้ โดยการ Fork และส่ง pull requests กลับมา
