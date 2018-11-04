![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

# PyThaiNLP

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cb946260c87a4cc5905ca608704406f7)](https://www.codacy.com/app/pythainlp/pythainlp_2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade)[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/PyThaiNLP/pythainlp.svg?branch=develop)](https://travis-ci.org/PyThaiNLP/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/9g3mfcwchi8em40x?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp-9y1ch)
[![Coverage Status](https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev)](https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Thai Natural Language Processing in Python.

PyThaiNLP is a Python package for text processing and linguistic analysis, similar to `nltk`, but with focus on Thai language.

PyThaiNLP supports Python 3.4+. Since version 1.7, PyThaiNLP deprecates its support for Python 2. Python 2 users can still use PyThaiNLP 1.6.

## Capabilities

- Thai word segmentation (```word_tokenize```), including subword segmentation based on Thai Character Cluster (```tcc```) and ETCC (```etcc```)
- Thai romanization (```romanize```)
- Thai part-of-speech taggers (```pos_tag```)
- Read out number to Thai words (```bahttext```, ```num_to_thaiword```)
- Thai collation (sort by dictionoary order) (```collate```)
- Thai-English keyboard misswitched fix (```eng_to_thai```, ```thai_to_eng```)
- Thai misspellings detection and spelling correction (```spell```)
- Thai soundex (```lk82```, ```udom83```, ```metasound```)
- Thai stop words (```pythainlp.corpus.thai_stopwords```)
- Thai WordNet
- and much more - see [examples](https://github.com/PyThaiNLP/pythainlp/tree/dev/examples).

## Installation

**Using pip**

Stable release

```sh
$ pip install pythainlp
```

Development release

```sh
$ pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
```

## Documentation

See [https://thainlp.org/pythainlp/docs/1.7/](https://thainlp.org/pythainlp/docs/1.7/)

## License

- PyThaiNLP code uses [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE)
- Corpus data created by PyThaiNLP project use [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)
- For other corpus that may included with PyThaiNLP distribution, please refer to [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md).

## Contribute to PyThaiNLP

Please do fork and create a pull request :)

For style guide and other information, including references to algorithms we use, please refer to our [contributing](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md) page.


# ภาษาไทย

ประมวลภาษาไทยในภาษา Python

PyThaiNLP เป็นไลบารีภาษาไพทอนเพื่อการประมวลผลภาษาธรรมชาติ โดยเน้นการสนับสนุนภาษาไทย **แจกจ่ายฟรี (ตลอดไป) เพื่อคนไทยและชาวโลกทุกคน!**

> เพราะโลกขับเคลื่อนต่อไปด้วยการแบ่งปัน

รองรับ Python 3.4 ขึ้นไป

- หน้าหลัก GitHub: [https://github.com/PyThaiNLP/pythainlp/](https://github.com/PyThaiNLP/pythainlp/)

## ความสามารถ

- ตัดคำภาษาไทย (```word_tokenize```) และรองรับ Thai Character Clusters (```tcc```) และ ETCC (```etcc```)
- ถอดเสียงภาษาไทยเป็นอักษรละติน (```romanize```)
- ระบุชนิดคำ (part-of-speech) ภาษาไทย (```pos_tag```)
- อ่านตัวเลขเป็นข้อความภาษาไทย (```bahttext```, ```num_to_thaiword```)
- เรียงลำดับคำตามพจนานุกรมไทย (```collate```)
- แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา (```eng_to_thai```, ```thai_to_eng```)
- ตรวจคำสะกดผิดในภาษาไทย (```spell```)
- soundex ภาษาไทย (```lk82```, ```udom83```, ```metasound```)
- stop word ภาษาไทย (```pythainlp.corpus.thai_stopwords```)
- Thai WordNet
- และอื่น ๆ [ดูตัวอย่าง](https://github.com/PyThaiNLP/pythainlp/tree/dev/examples)

## ติดตั้ง

รุ่นเสถียร

```sh
$ pip install pythainlp
```

รุ่นกำลังพัฒนา

```sh
$ pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
```

## เอกสารการใช้งาน

อ่านที่ [https://thainlp.org/pythainlp/docs/1.7/](https://thainlp.org/pythainlp/docs/1.7/)

## สัญญาอนุญาต

- โค้ด PyThaiNLP ใช้สัญญาอนุญาต [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE)
- คลังคำและข้อมูลที่สร้างโดยโครงการ PyThaiNLP ใช้สัญญาอนุญาตครีเอทีฟคอมมอนส์แบบแสดงที่มา-อนุญาตแบบเดียวกัน 4.0 [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)
- คลังคำและข้อมูลอื่นๆ ที่อาจแจกจ่ายไปพร้อมกับแพคเกจ PyThaiNLP อาจใช้สัญญาอนุญาตอื่น โปรดดูเอกสาร [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md)

## ตราสัญลักษณ์

ออกแบบโดยคุณ วรุตม์ พสุธาดล จากการประกวดที่ https://www.facebook.com/groups/408004796247683/permalink/475864542795041/ และ https://www.facebook.com/groups/408004796247683/permalink/474262752955220/

## สนับสนุนและร่วมพัฒนา

คุณสามารถ[ร่วมพัฒนาโครงการนี้](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md)ได้ โดยการ fork และส่ง pull request กลับมา
