# PyThaiNLP
[![PyPI Downloads](https://img.shields.io/pypi/dm/pythainlp.png)]
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/50fa9d87f4fb4a95aac62b398aa374fa)](https://www.codacy.com/app/wannaphongcom/pythainlp?utm_source=github.com&utm_medium=referral&utm_content=wannaphongcom/pythainlp&utm_campaign=badger)
[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/wannaphongcom/pythainlp.svg?branch=develop)](https://travis-ci.org/wannaphongcom/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/uxerymgggp1uch0p?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp)[![Code Issues](https://www.quantifiedcode.com/api/v1/project/7f699ed4cad24be18d0d24ebd60d7543/badge.svg)](https://www.quantifiedcode.com/app/project/7f699ed4cad24be18d0d24ebd60d7543)[![Coverage Status](https://coveralls.io/repos/github/wannaphongcom/pythainlp/badge.svg?branch=pythainlp1.4)](https://coveralls.io/github/wannaphongcom/pythainlp?branch=pythainlp1.4)

## English

Thai natural language processing in Python.

PyThaiNLP is python module like nltk , but It's working with thai language.

It's support python 3.4 +.

### Project status

Developing

### Version

1.4

### Capability

- Thai segment
- Thai wordnet
- Thai Character Clusters (TCC) and ETCC
- Thai stop word
- Thai meta sound
- Thai soundex
- Thai postaggers
- Thai romanization
- Check the wrong words in Thai.

and much more.

### Install

**using pip.**

```sh
$ pip install pythainlp
```

**Install in  Windows**

download pyicu from [http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu) than install pyicu. install pythainlp using pip.

```
pip install pythainlp
```

**Install in MacOS**

```sh
$ brew install icu4c --force
$ brew link --force icu4c
$ CFLAGS=-I/usr/local/opt/icu4c/include LDFLAGS=-L/usr/local/opt/icu4c/lib pip install pythainlp
```

### Documentation

Read on https://github.com/wannaphongcom/pythainlp/blob/pythainlp1.4/docs/pythainlp-1-4-eng.md

### License

Apache Software License 2.0

## ภาษาไทย

[![PyPI Downloads](https://img.shields.io/pypi/dm/pythainlp.png)]
[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/wannaphongcom/pythainlp.svg?branch=develop)](https://travis-ci.org/wannaphongcom/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/uxerymgggp1uch0p?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp)[![Code Issues](https://www.quantifiedcode.com/api/v1/project/7f699ed4cad24be18d0d24ebd60d7543/badge.svg)](https://www.quantifiedcode.com/app/project/7f699ed4cad24be18d0d24ebd60d7543)[![Coverage Status](https://coveralls.io/repos/github/wannaphongcom/pythainlp/badge.svg?branch=pythainlp1.4)](https://coveralls.io/github/wannaphongcom/pythainlp?branch=pythainlp1.4)

ประมวลภาษาธรรมชาติภาษาไทยในภาษา Python

Natural language processing หรือ การประมวลภาษาธรรมชาติ  โมดูล PyThaiNLP เป็นโมดูลที่ถูกพัฒนาขึ้นเพื่อพัฒนาการประมวลภาษาธรรมชาติภาษาไทยในภาษา Python และ**มันฟรี (ตลอดไป) เพื่อคนไทยและชาวโลกทุกคน !**

> เพราะโลกขับเคลื่อนต่อไปด้วยการแบ่งปัน

รองรับ Python 3.4 ขึ้นไป

  - หน้าหลัก GitHub :  [https://github.com/wannaphongcom/pythainlp](https://github.com/wannaphongcom/pythainlp)

### สถานะโครงการ

กำลังพัฒนา 

### Version
1.4

### สิ่งใหม่ที่เพิ่มเข้ามาใน PyThaiNLP 1.4

- รองรับ  Thai Character Clusters (TCC) และ ETCC
- Thai WordNet ตัวใหม่
- เพิ่มหลักเกณฑ์การถอดอักษรไทยเป็นอักษรโรมัน ฉบับราชบัณฑิตยสถาน
- เพิ่ม Meta Sound ภาษาไทย
- เพิ่ม Thai Soundex

### ความสามารถ
  - ตัดคำภาษาไทย
  - ถอดเสียงภาษาไทยเป็น Latin
  - Postaggers ภาษาไทย
  - อ่านตัวเลขเป็นข้อความภาษาไทย
  - เรียงจำนวนคำของประโยค
  - แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา
  - เช็คคำผิดในภาษาไทย
  - รองรับ  Thai Character Clusters (TCC) และ ETCC
  - Thai WordNet
  - Stop Word ภาษาไทย
  - Meta Sound ภาษาไทย
  - Thai Soundex
  - และอื่น ๆ 

### ติดตั้ง

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


### เอกสารการใช้งาน

อ่านได้ที่ https://github.com/wannaphongcom/pythainlp/blob/pythainlp1.4/docs/pythainlp-1-4-thai.md

### License

Apache Software License 2.0


พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์

### สนับสนุน

คุณสามารถร่วมพัฒนาโครงการนี้ได้ โดยการ Fork และส่ง pull requests กลับมา
