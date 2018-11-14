![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

# PyThaiNLP

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cb946260c87a4cc5905ca608704406f7)](https://www.codacy.com/app/pythainlp/pythainlp_2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade)[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Build Status](https://travis-ci.org/PyThaiNLP/pythainlp.svg?branch=develop)](https://travis-ci.org/PyThaiNLP/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/9g3mfcwchi8em40x?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp-9y1ch)
[![Coverage Status](https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev)](https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPyThaiNLP%2Fpythainlp.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FPyThaiNLP%2Fpythainlp?ref=badge_shield)

Thai Natural Language Processing in Python.

PyThaiNLP is a Python package for text processing and linguistic analysis, similar to `nltk` but with focus on Thai language.

- [Current PyThaiNLP release is 1.7.1](https://github.com/PyThaiNLP/pythainlp/tree/master)
- PyThaiNLP 1.8 will support only Python 3.6+. Some functions may work with older version of Python 3, but it is not well-tested and will not be supported. See [PyThaiNLP 1.8 change log](https://github.com/PyThaiNLP/pythainlp/issues/118).
- Python 2 users can use PyThaiNLP 1.6, our latest released that tested with Python 2.7.

**This is a document for development branch (post 1.7.x). Things will break. For a stable branch document, see [master](https://github.com/PyThaiNLP/pythainlp/tree/master).**

## Capabilities

- Convenient character and word classes, like Thai consonants (```pythainlp.thai_consonants```), vowels (```pythainlp.thai_vowels```), digits (```pythainlp.thai_digits```), and stop words (```pythainlp.corpus.thai_stopwords```) -- comparable to constants like ```string.letters```, ```string.digits```, and ```string.punctuation```
- Thai word segmentation (```word_tokenize```), including subword segmentation based on Thai Character Cluster (```tcc```) and ETCC (```etcc```)
- Thai romanization and transliteration (```romanize```, ```transliterate```)
- Thai part-of-speech taggers (```pos_tag```)
- Read out number to Thai words (```bahttext```, ```num_to_thaiword```)
- Thai collation (sort by dictionoary order) (```collate```)
- Thai-English keyboard misswitched fix (```eng_to_thai```, ```thai_to_eng```)
- Thai misspellings detection and spelling correction (```spell```)
- Thai soundex (```lk82```, ```udom83```, ```metasound```)
- Thai WordNet wrapper
- and much more - see [examples](https://github.com/PyThaiNLP/pythainlp/tree/dev/examples).

## Installation

PyThaiNLP uses PyPI as its main distribution channel, see https://pypi.org/project/pythainlp/

### Stable release

Standard installation:

```sh
$ pip install pythainlp
```

For some advanced functionalities, like word vector, extra packages may be needed. Install them with these options during pip install:

```sh
$ pip install pythainlp[extra1,extra2,...]
```

where ```extras``` can be
  - ```artagger``` (to support artagger part-of-speech tagger)*
  - ```deepcut``` (to support deepcut machine-learnt tokenizer)
  - ```icu``` (for ICU support in transliteration and tokenization)
  - ```ipa``` (for International Phonetic Alphabet support in transliteration)
  - ```ml``` (to support ULMFiT models, like one for sentiment analyser)
  - ```ner``` (for named-entity recognizer)
  - ```thai2rom``` (for machine-learnt romanization)
  - ```thai2vec``` (for Thai word vector)
  - ```full``` (install everything)

* Note: standard ```artagger``` package from PyPI will not work on Windows, please ```pip install https://github.com/wannaphongcom/artagger/tarball/master#egg=artagger``` instead.

** see ```extras``` and ```extras_require``` in [```setup.py```](https://github.com/PyThaiNLP/pythainlp/blob/dev/setup.py) for package details.

### Development release:

```sh
$ pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
```

## Documentation

See [https://thainlp.org/pythainlp/docs/1.7/](https://thainlp.org/pythainlp/docs/1.7/)

## License

- PyThaiNLP code uses [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE)
- Corpus data created by PyThaiNLP project use [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)
- For other corpus that may included with PyThaiNLP distribution, please refer to [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md).


[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPyThaiNLP%2Fpythainlp.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FPyThaiNLP%2Fpythainlp?ref=badge_large)

## Contribute to PyThaiNLP

Please do fork and create a pull request :)

For style guide and other information, including references to algorithms we use, please refer to our [contributing](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md) page.


# ภาษาไทย

ประมวลภาษาไทยในภาษา Python

PyThaiNLP เป็นไลบารีภาษาไพทอนเพื่อการประมวลผลภาษาธรรมชาติ โดยเน้นการสนับสนุนภาษาไทย **แจกจ่ายฟรี (ตลอดไป) เพื่อคนไทยและชาวโลกทุกคน!**

> เพราะโลกขับเคลื่อนต่อไปด้วยการแบ่งปัน

รองรับ Python 3.6 ขึ้นไป

ตั้งแต่รุ่น 1.7 PyThaiNLP จะเลิกสนับสนุน Python 2 (บางฟังก์ชันอาจยังทำงานได้ แต่จะไม่ได้รับการสนับสนุน) และตั้งแต่รุ่น 1.8 จะยุติการรองรับ Python 2 ทั้งหมด
ผู้ใช้ Python 2 ยังสามารถใช้ PyThaiNLP 1.6 ได้

**เอกสารนี้สำหรับรุ่นพัฒนา (หลัง 1.7.x) อาจมีการเปลี่ยนแปลงได้ตลอด สำหรับเอกสารรุ่นเสถียร ดูที่ [master](https://github.com/PyThaiNLP/pythainlp/tree/master).**

## ความสามารถ

- ชุดค่าคงที่ตัวอักษระและคำไทยที่เรียกใช้ได้สะดวก เช่น พยัญชนะ (```pythainlp.thai_consonants```), สระ (```pythainlp.thai_vowels```), ตัวเลขไทย (```pythainlp.thai_digits```), และ stop word (```pythainlp.corpus.thai_stopwords```) -- เหมือนกับต่าคงที่อย่าง ```string.letters```, ```string.digits```, และ ```string.punctuation```
- Thai word segmentation (```word_tokenize```), including subword segmentation based on Thai Character Cluster (```tcc```) and ETCC (```etcc```)
- ตัดคำภาษาไทย (```word_tokenize```) และรองรับ Thai Character Clusters (```tcc```) และ ETCC (```etcc```)
- ถอดเสียงภาษาไทยเป็นอักษรละตินและสัทอักษร (```romanize```, ```transliterate```)
- ระบุชนิดคำ (part-of-speech) ภาษาไทย (```pos_tag```)
- อ่านตัวเลขเป็นข้อความภาษาไทย (```bahttext```, ```num_to_thaiword```)
- เรียงลำดับคำตามพจนานุกรมไทย (```collate```)
- แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา (```eng_to_thai```, ```thai_to_eng```)
- ตรวจคำสะกดผิดในภาษาไทย (```spell```)
- soundex ภาษาไทย (```lk82```, ```udom83```, ```metasound```)
- Thai WordNet wrapper
- และอื่น ๆ [ดูตัวอย่าง](https://github.com/PyThaiNLP/pythainlp/tree/dev/examples)

## ติดตั้ง

### รุ่นเสถียร

```sh
$ pip install pythainlp
```

สำหรับความสามารถเพิ่มเติมบางอย่าง เช่น word vector จำเป็นต้องติดตั้งแพคเกจสนับสนุนเพิ่มเติม ติดตั้งแพคเพจเหล่านั้นได้ ด้วยการระบุออปชันเหล่านี้ตอน pip install:

```sh
$ pip install pythainlp[extra1,extra2,...]
```

โดยที่ ```extras``` คือ
  - ```artagger``` (สำหรับตัวติดป้ายกำกับชนิดคำ artagger)*
  - ```deepcut``` (สำหรับตัวตัดคำ deepcut)
  - ```icu``` (สำหรับการถอดตัวสะกดเป็นสัทอักษรและการตัดคำด้วย ICU)
  - ```ipa``` (สำหรับการถอดตัวสะกดเป็นสัทอักษรสากล (IPA))
  - ```ml``` (สำหรับการรองรับโมเดล ULMFiT ซึ่งใช้ในฟังก์ชันเช่นการวิเคราะห์อารมณ์)
  - ```ner``` (สำหรับการติดป้ายชื่อเฉพาะ (named-entity))
  - ```thai2rom``` (สำหรับการถอดตัวสะกดเป็นอักษรละติน)
  - ```thai2vec``` (สำหรับ word vector)
  - ```full``` (ติดตั้งทุกอย่าง)

* หมายเหตุ: แพคเกจ ```artagger``` มาตรฐานจาก PyPI อาจมีปัญหาการถอดรหัสข้อความบน Windows กรุณาติดตั้งรุ artagger รุ่นแก้ไขด้วยคำสั่ง ```pip install https://github.com/wannaphongcom/artagger/tarball/master#egg=artagger``` แทน ก่อนจะติดตั้ง PyThaiNLP

** นักพัฒนาสามารถดู ```extras``` และ ```extras_require``` ใน [```setup.py```](https://github.com/PyThaiNLP/pythainlp/blob/dev/setup.py) สำหรับรายละเอียดแพคเกจของเสริม


### รุ่นกำลังพัฒนา

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