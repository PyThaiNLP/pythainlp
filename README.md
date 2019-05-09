![PyThaiNLP Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

# PyThaiNLP

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cb946260c87a4cc5905ca608704406f7)](https://www.codacy.com/app/pythainlp/pythainlp_2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade)[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Downloads](https://pepy.tech/badge/pythainlp/month)](https://pepy.tech/project/pythainlp)
[![Build Status](https://travis-ci.org/PyThaiNLP/pythainlp.svg?branch=develop)](https://travis-ci.org/PyThaiNLP/pythainlp)
[![Build status](https://ci.appveyor.com/api/projects/status/9g3mfcwchi8em40x?svg=true)](https://ci.appveyor.com/project/wannaphongcom/pythainlp-9y1ch)
[![Coverage Status](https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev)](https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPyThaiNLP%2Fpythainlp.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FPyThaiNLP%2Fpythainlp?ref=badge_shield)

Thai Natural Language Processing in Python.

PyThaiNLP is a Python package for text processing and linguistic analysis, similar to `nltk` but with focus on Thai language.

**This is a document for development branch (post 2.0). Things will break.**

- The latest stable release is [2.0.5](https://github.com/PyThaiNLP/pythainlp/tree/master)
- PyThaiNLP 2 supports Python 3.6+. Some functions may work with older version of Python 3, but it is not well-tested and will not be supported. See [change log](https://github.com/PyThaiNLP/pythainlp/issues/118).
  - [Upgrading from 1.7](https://thainlp.org/pythainlp/docs/2.0/notes/pythainlp-1_7-2_0.html)
  - [Upgrade ThaiNER from 1.7](https://github.com/PyThaiNLP/pythainlp/wiki/Upgrade-ThaiNER-from-PyThaiNLP-1.7-to-PyThaiNLP-2.0)
- Python 2.7+ users can use PyThaiNLP 1.6.

📫 follow us on Facebook [PyThaiNLP](https://www.facebook.com/pythainlp/)

## Capabilities

- Convenient character and word classes, like Thai consonants (`pythainlp.thai_consonants`), vowels (`pythainlp.thai_vowels`), digits (`pythainlp.thai_digits`), and stop words (`pythainlp.corpus.thai_stopwords`) -- comparable to constants like `string.letters`, `string.digits`, and `string.punctuation`
- Thai word segmentation (`word_tokenize`), including subword segmentation based on Thai Character Cluster (`subword_tokenize`)
- Thai transliteration (`transliterate`)
- Thai part-of-speech taggers (`pos_tag`)
- Read out number to Thai words (`bahttext`, `num_to_thaiword`)
- Thai collation (sort by dictionoary order) (`collate`)
- Thai-English keyboard misswitched fix (`eng_to_thai`, `thai_to_eng`)
- Thai spelling suggestion and correction (`spell` and `correct`)
- Thai soundex (`soundex`) with three engines (`lk82`, `udom83`, `metasound`)
- Thai WordNet wrapper
- and much more - see examples in [PyThaiNLP Get Started notebook](https://github.com/PyThaiNLP/pythainlp/blob/dev/notebooks/pythainlp-get-started.ipynb).

## Installation

PyThaiNLP uses PyPI as its main distribution channel, see https://pypi.org/project/pythainlp/

### Stable release

Standard installation:

```sh
$ pip install pythainlp
```

### Development release:

```sh
$ pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
```

For some advanced functionalities, like word vector, extra packages may be needed. Install them with these options during pip install:

```sh
$ pip install pythainlp[extra1,extra2,...]
```

where `extras` can be
  - `artagger` (to support artagger part-of-speech tagger)*
  - `deepcut` (to support deepcut machine-learnt tokenizer)
  - `icu` (for ICU, International Components for Unicode, support in transliteration and tokenization)
  - `ipa` (for IPA, International Phonetic Alphabet, support in transliteration)
  - `ml` (to support fastai 1.0.22 ULMFiT models)
  - `ner` (for named-entity recognizer)
  - `thai2fit` (for Thai word vector)
  - `thai2rom` (for machine-learnt romanization)
  - `full` (install everything)

* Note: standard `artagger` package from PyPI will not work on Windows, please ```pip install https://github.com/wannaphongcom/artagger/tarball/master#egg=artagger``` instead.

** see `extras` and `extras_require` in [`setup.py`](https://github.com/PyThaiNLP/pythainlp/blob/dev/setup.py) for package details.

## Documentation

See [https://thainlp.org/pythainlp/docs/2.0/](https://thainlp.org/pythainlp/docs/2.0/)

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

**เอกสารนี้สำหรับรุ่นพัฒนา อาจมีการเปลี่ยนแปลงได้ตลอด**

- รุ่นเสถียรล่าสุดคือรุ่น [2.0.5](https://github.com/PyThaiNLP/pythainlp/tree/master)
- PyThaiNLP 2 รองรับ Python 3.6 ขึ้นไป
- ผู้ใช้ Python 2.7+ ยังสามารถใช้ PyThaiNLP 1.6 ได้

📫 ติดตามข่าวสารได้ที่ Facebook [Pythainlp](https://www.facebook.com/pythainlp/)

## ความสามารถ

- ชุดค่าคงที่ตัวอักษระและคำไทยที่เรียกใช้ได้สะดวก เช่น พยัญชนะ (`pythainlp.thai_consonants`), สระ (`pythainlp.thai_vowels`), ตัวเลขไทย (`pythainlp.thai_digits`), และ stop word (`pythainlp.corpus.thai_stopwords`) -- เหมือนกับค่าคงที่อย่าง `string.letters`, `string.digits`, และ `string.punctuation`
- ตัดคำภาษาไทย (`word_tokenize`) และรองรับการตัดระดับต่ำกว่าคำโดยใช้ Thai Character Clusters (`subword_tokenize`)
- ถอดเสียงภาษาไทยเป็นอักษรละตินและสัทอักษร (`transliterate`)
- ระบุชนิดคำ (part-of-speech) ภาษาไทย (`pos_tag`)
- อ่านตัวเลขเป็นข้อความภาษาไทย (`bahttext`, `num_to_thaiword`)
- เรียงลำดับคำตามพจนานุกรมไทย (`collate`)
- แก้ไขปัญหาการพิมพ์ลืมเปลี่ยนภาษา (`eng_to_thai`, `thai_to_eng`)
- ตรวจคำสะกดผิดในภาษาไทย (`spell`, `correct`)
- soundex ภาษาไทย (`soundex`) 3 วิธีการ (`lk82`, `udom83`, `metasound`)
- Thai WordNet wrapper
- และอื่น ๆ ดูตัวอย่างได้ใน [PyThaiNLP Get Started notebook](https://github.com/PyThaiNLP/pythainlp/blob/dev/notebooks/pythainlp-get-started.ipynb)

## ติดตั้ง

### รุ่นเสถียร

```sh
$ pip install pythainlp
```

### รุ่นกำลังพัฒนา

```sh
$ pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
```

สำหรับความสามารถเพิ่มเติมบางอย่าง เช่น word vector จำเป็นต้องติดตั้งแพคเกจสนับสนุนเพิ่มเติม ติดตั้งแพคเพจเหล่านั้นได้ ด้วยการระบุออปชันเหล่านี้ตอน pip install:

```sh
$ pip install pythainlp[extra1,extra2,...]
```

โดยที่ `extras` คือ
  - `artagger` (สำหรับตัวติดป้ายกำกับชนิดคำ artagger)*
  - `deepcut` (สำหรับตัวตัดคำ deepcut)
  - `icu` (สำหรับการถอดตัวสะกดเป็นสัทอักษรและการตัดคำด้วย ICU)
  - `ipa` (สำหรับการถอดตัวสะกดเป็นสัทอักษรสากล (IPA))
  - `ml` (สำหรับการรองรับโมเดล ULMFiT)
  - `ner` (สำหรับการติดป้ายชื่อเฉพาะ (named-entity))
  - `thai2fit` (สำหรับ word vector)
  - `thai2rom` (สำหรับการถอดตัวสะกดเป็นอักษรละติน)
  - `full` (ติดตั้งทุกอย่าง)

* หมายเหตุ: แพคเกจ `artagger` มาตรฐานจาก PyPI อาจมีปัญหาการถอดรหัสข้อความบน Windows กรุณาติดตั้ง artagger รุ่นแก้ไขด้วยคำสั่ง ```pip install https://github.com/wannaphongcom/artagger/tarball/master#egg=artagger``` แทน ก่อนจะติดตั้ง PyThaiNLP

** สามารถดู `extras` และ `extras_require` ใน [`setup.py`](https://github.com/PyThaiNLP/pythainlp/blob/dev/setup.py) สำหรับรายละเอียดแพคเกจของเสริม

## เอกสารการใช้งาน

อ่านที่ [https://thainlp.org/pythainlp/docs/2.0/](https://thainlp.org/pythainlp/docs/2.0/)

## สัญญาอนุญาต

- โค้ด PyThaiNLP ใช้สัญญาอนุญาต [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE)
- คลังคำและข้อมูลที่สร้างโดยโครงการ PyThaiNLP ใช้สัญญาอนุญาตครีเอทีฟคอมมอนส์แบบแสดงที่มา-อนุญาตแบบเดียวกัน 4.0 [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)
- คลังคำและข้อมูลอื่นๆ ที่อาจแจกจ่ายไปพร้อมกับแพคเกจ PyThaiNLP อาจใช้สัญญาอนุญาตอื่น โปรดดูเอกสาร [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md)

## ตราสัญลักษณ์

ออกแบบโดยคุณ วรุตม์ พสุธาดล จากการประกวดที่ https://www.facebook.com/groups/408004796247683/permalink/475864542795041/ และ https://www.facebook.com/groups/408004796247683/permalink/474262752955220/

## สนับสนุนและร่วมพัฒนา

คุณสามารถ[ร่วมพัฒนาโครงการนี้](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md)ได้ โดยการ fork และส่ง pull request กลับมา
