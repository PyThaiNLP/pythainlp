![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

# PyThaiNLP

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cb946260c87a4cc5905ca608704406f7)](https://www.codacy.com/app/pythainlp/pythainlp_2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade)[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/PyThaiNLP/pythainlp.svg?branch=develop)](https://travis-ci.org/PyThaiNLP/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/9g3mfcwchi8em40x?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp-9y1ch)
[![Coverage Status](https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev)](https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Thai natural language processing in Python.

PyThaiNLP is a Python package for text processing and linguistic analysis, similar to `nltk`, but with focus on Thai language.

PyThaiNLP supports Python 3.4+. Since version 1.7, PyThaiNLP deprecates its support for Python 2. Python 2 users can still use PyThaiNLP 1.6.

### Capabilities

- Thai word segmentation, including subword segmentation based on Thai Character Cluster (TCC) and ETCC
- Thai WordNet
- Thai part-of-speech taggers
- Thai romanization
- Thai soundex and MetaSound
- Thai misspellings detection and spelling correction
- Thai stop words
- and much more.

### Install

**Using pip**

Stable release

```sh
$ pip install pythainlp
```

Development release

```sh
$ pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
```

### Documentation

See [https://thainlp.org/pythainlp/docs/1.7/](https://thainlp.org/pythainlp/docs/1.7/)

### License

[Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE)

## ภาษาไทย

ประมวลภาษาไทยในภาษา Python

PyThaiNLP เป็นไลบารีภาษาไพทอนเพื่อการประมวลผลภาษาธรรมชาติ โดยเน้นการสนับสนุนภาษาไทย **แจกจ่ายฟรี (ตลอดไป) เพื่อคนไทยและชาวโลกทุกคน!**

> เพราะโลกขับเคลื่อนต่อไปด้วยการแบ่งปัน

รองรับ Python 3.4 ขึ้นไป

  - หน้าหลัก GitHub: [https://github.com/PyThaiNLP/pythainlp/](https://github.com/PyThaiNLP/pythainlp/)

### ความสามารถ
  - ตัดคำภาษาไทย
  - ถอดเสียงภาษาไทยเป็นอักษรละติน
  - ระบุชนิดคำ (part-of-speech) ภาษาไทย
  - อ่านตัวเลขเป็นข้อความภาษาไทย
  - เรียงจำนวนคำของประโยค
  - แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา
  - ตรวจคำสะกดผิดในภาษาไทย
  - รองรับ Thai Character Clusters (TCC) และ ETCC
  - Thai WordNet
  - stop word ภาษาไทย
  - MetaSound และ soundex ภาษาไทย
  - และอื่น ๆ 

### ติดตั้ง

รุ่นเสถียร

```sh
$ pip install pythainlp
```

รุ่นกำลังพัฒนา

```sh
$ pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
```

### เอกสารการใช้งาน

อ่านที่ [https://thainlp.org/pythainlp/docs/1.7/](https://thainlp.org/pythainlp/docs/1.7/)

### License

[Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE)

### Logo

ออกแบบโดยคุณ วรุตม์ พสุธาดล จากการประกวดที่ https://www.facebook.com/groups/408004796247683/permalink/475864542795041/ และ https://www.facebook.com/groups/408004796247683/permalink/474262752955220/

### สนับสนุน

คุณสามารถ[ร่วมพัฒนาโครงการนี้](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md)ได้ โดยการ fork และส่ง pull request กลับมา
