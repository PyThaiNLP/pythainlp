# PyThaiNLP: Thai Natural Language Processing in Python

![Project Logo](https://avatars0.githubusercontent.com/u/32934255?s=200&v=4)

[![pypi](https://img.shields.io/pypi/v/pythainlp.svg)](https://pypi.python.org/pypi/pythainlp)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3519354.svg)](https://doi.org/10.5281/zenodo.3519354)
[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Codacy Grade](https://app.codacy.com/project/badge/Grade/5821a0de122041c79999bbb280230ffb)](https://www.codacy.com/gh/PyThaiNLP/pythainlp/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev)](https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev)
[![Google Colab Badge](https://badgen.net/badge/Launch%20Quick%20Start%20Guide/on%20Google%20Colab/blue?icon=terminal)](https://colab.research.google.com/github/PyThaiNLP/tutorials/blob/master/source/notebooks/pythainlp_get_started.ipynb)
[![Facebook](https://img.shields.io/badge/Facebook-0866FF?style=flat&logo=facebook&logoColor=white)](https://www.facebook.com/pythainlp/)
[![Chat on Matrix](https://matrix.to/img/matrix-badge.svg)](https://matrix.to/#/#thainlp:matrix.org)

[pythainlp.org](https://pythainlp.org/) |
[Tutorials](https://pythainlp.org/tutorials) |
[License info](https://pythainlp.org/dev-docs/notes/license.html) |
[Model cards](https://github.com/PyThaiNLP/pythainlp/wiki/Model-Cards) |
[Adopters](https://github.com/PyThaiNLP/pythainlp/blob/dev/INTHEWILD.md) |
*[English](https://github.com/PyThaiNLP/pythainlp/blob/dev/README.md)*

PyThaiNLP เป็นไลบารีภาษาไพทอนสำหรับประมวลผลภาษาธรรมชาติ โดยเน้นภาษาไทย
**PyThaiNLP** ถูกออกแบบให้เป็นเครื่องมือมาตรฐานสำหรับการวิเคราะห์ภาษาศาสตร์ภาษาไทย
ภายใต้สัญญาอนุญาต Apache-2.0 โดยข้อมูลและโมเดลอยู่ภายใต้ CC0-1.0 และ CC-BY-4.0

```sh
pip install pythainlp
```

| Version | Python version | Changes | Documentation |
|:-------:|:--------------:|:-------:|:-------------:|
| [5.2.0](https://github.com/PyThaiNLP/pythainlp/releases) | 3.7+ | [Log](https://github.com/PyThaiNLP/pythainlp/issues/1080) | [pythainlp.org/docs](https://pythainlp.org/docs) |
| [`dev`](https://github.com/PyThaiNLP/pythainlp/tree/dev) | 3.9+ | [Log](https://github.com/PyThaiNLP/pythainlp/issues/1169) | [pythainlp.org/dev-docs](https://pythainlp.org/dev-docs/) |

## ความสามารถ

- **หน่วยภาษาศาสตร์:** การแบ่งประโยค คำ และหน่วยคำย่อย
  (`sent_tokenize`, `word_tokenize`, `subword_tokenize`)
- **การกำกับหน้าที่:** Part-of-speech tagging (`pos_tag`)
- **การถอดอักษร:** Romanization (`transliterate`) และการแปลงเป็น IPA
- **การแก้ไข:** การแนะนำและแก้ไขการสะกด (`spell`, `correct`)
- **เครื่องมือเสริม:** Soundex, การเรียงลำดับ, แปลงตัวเลขเป็นข้อความ (`bahttext`),
  การจัดรูปแบบวันที่ (`thai_strftime`), และแก้ไขการสลับแป้นพิมพ์
- **ข้อมูล:** ชุดตัวอักษรไทย, รายการคำ, และคำหยุด (stop words)
- **CLI:** Command-line interface ผ่าน `thainlp`

  ```sh
  thainlp data catalog  # แสดงรายการชุดข้อมูล
  thainlp help          # แสดงวิธีใช้งาน
  ```

## ตัวเลือกการติดตั้ง

การติดตั้งพร้อม extras เฉพาะ (เช่น `translate`, `wordnet`, `full`):

```sh
pip install "pythainlp[extra1,extra2,...]"
```

`extras` ที่เป็นไปได้:

- `compact` — ติดตั้งชุดย่อยที่เสถียรและเล็ก (แนะนำ)
- `translate` — รองรับการแปลภาษา
- `wordnet` — รองรับ WordNet
- `full` — ติดตั้ง dependencies ทั้งหมด (อาจเกิดความขัดแย้ง)

เว็บไซต์เอกสารมี[รายการ extras ทั้งหมด](https://pythainlp.org/dev-docs/notes/installation.html)
หากต้องการดูไลบารีที่รวมอยู่ในแต่ละ extra
กรุณาตรวจสอบส่วน `[project.optional-dependencies]` ใน
[`pyproject.toml`](https://github.com/PyThaiNLP/pythainlp/blob/dev/pyproject.toml)

## ไดเรกทอรีข้อมูล

PyThaiNLP ดาวน์โหลดข้อมูล (ดูแค็ตตาล็อกข้อมูล `db.json` ที่
[pythainlp-corpus](https://github.com/PyThaiNLP/pythainlp-corpus))
ไปที่ `~/pythainlp-data` ตามค่าเริ่มต้น
ตั้งค่า environment variable `PYTHAINLP_DATA_DIR` เพื่อเปลี่ยนตำแหน่งนี้

เมื่อใช้ PyThaiNLP ในสภาพแวดล้อมการคำนวณแบบกระจาย
(เช่น Apache Spark) ให้ตั้งค่า environment variable `PYTHAINLP_DATA_DIR`
ภายในฟังก์ชันที่จะถูกกระจายไปยัง worker nodes
ดูรายละเอียดใน[เอกสาร](https://pythainlp.org/dev-docs/notes/installation.html)

## การทดสอบ

เราทดสอบฟังก์ชันหลักบน Python ทุกเวอร์ชันที่รองรับอย่างเป็นทางการ

ดู [tests/README.md](./tests/README.md) สำหรับ test matrix และรายละเอียดอื่น ๆ

## ร่วมพัฒนา PyThaiNLP

กรุณา fork และสร้าง pull request
ดู [CONTRIBUTING.md](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md)
สำหรับแนวทางและการอ้างอิงอัลกอริทึม

## การอ้างอิง

หากคุณใช้ `PyThaiNLP` ในโครงงานหรืองานวิจัยของคุณ
กรุณาอ้างอิงไลบารีดังนี้:

> Phatthiyaphaibun, Wannaphong, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, and Pattarawat Chormai. “Pythainlp: Thai Natural Language Processing in Python”. Zenodo, 2 June 2024. <http://doi.org/10.5281/zenodo.3519354>.

หรือ BibTeX entry:

```bibtex
@software{pythainlp,
    title = "{P}y{T}hai{NLP}: {T}hai Natural Language Processing in {P}ython",
    author = "Phatthiyaphaibun, Wannaphong  and
      Chaovavanich, Korakot  and
      Polpanumas, Charin  and
      Suriyawongkul, Arthit  and
      Lowphansirikul, Lalita  and
      Chormai, Pattarawat",
    doi = {10.5281/zenodo.3519354},
    license = {Apache-2.0},
    month = jun,
    url = {https://github.com/PyThaiNLP/pythainlp/},
    version = {v5.0.4},
    year = {2024},
}
```

บทความของเราใน [NLP-OSS 2023](https://nlposs.github.io/2023/):

> Wannaphong Phatthiyaphaibun, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, Pattarawat Chormai, Peerat Limkonchotiwat, Thanathip Suntorntip, and Can Udomcharoenchaikit. 2023. [PyThaiNLP: Thai Natural Language Processing in Python.](https://aclanthology.org/2023.nlposs-1.4) In Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023), pages 25–36, Singapore, Singapore. Empirical Methods in Natural Language Processing.

และ BibTeX entry:

```bibtex
@inproceedings{phatthiyaphaibun-etal-2023-pythainlp,
    title = "{P}y{T}hai{NLP}: {T}hai Natural Language Processing in Python",
    author = "Phatthiyaphaibun, Wannaphong  and
      Chaovavanich, Korakot  and
      Polpanumas, Charin  and
      Suriyawongkul, Arthit  and
      Lowphansirikul, Lalita  and
      Chormai, Pattarawat  and
      Limkonchotiwat, Peerat  and
      Suntorntip, Thanathip  and
      Udomcharoenchaikit, Can",
    editor = "Tan, Liling  and
      Milajevs, Dmitrijs  and
      Chauhan, Geeticka  and
      Gwinnup, Jeremy  and
      Rippeth, Elijah",
    booktitle = "Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023)",
    month = dec,
    year = "2023",
    address = "Singapore, Singapore",
    publisher = "Empirical Methods in Natural Language Processing",
    url = "https://aclanthology.org/2023.nlposs-1.4",
    pages = "25--36",
    abstract = "We present PyThaiNLP, a free and open-source natural language processing (NLP) library for Thai language implemented in Python. It provides a wide range of software, models, and datasets for Thai language. We first provide a brief historical context of tools for Thai language prior to the development of PyThaiNLP. We then outline the functionalities it provided as well as datasets and pre-trained language models. We later summarize its development milestones and discuss our experience during its development. We conclude by demonstrating how industrial and research communities utilize PyThaiNLP in their work. The library is freely available at https://github.com/pythainlp/pythainlp.",
}
```

## ผู้สนับสนุน

| โลโก้ | รายละเอียด |
| --- | ----------- |
| [![VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/assets/img/logo/airesearch-logo.svg)](https://airesearch.in.th/) | ตั้งแต่ปี 2019 ผู้ร่วมพัฒนาของเรา Korakot Chaovavanich และ Lalita Lowphansirikul ได้รับการสนับสนุนจาก [VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/) |
| [![MacStadium](https://i.imgur.com/rKy1dJX.png)](https://www.macstadium.com) | เราได้รับการสนับสนุน Mac Mini M1 ฟรีจาก [MacStadium](https://www.macstadium.com) สำหรับการรัน CI builds |

------

<div align="center">
  สร้างด้วย ❤️ | ทีม PyThaiNLP 💻 | "เราสร้างการประมวลผลภาษาไทย" 🇹🇭
</div>

------

<div align="center">
  <strong>เรามีที่เก็บข้อมูลอย่างเป็นทางการที่เดียวที่ https://github.com/PyThaiNLP/pythainlp และมีที่เก็บสำเนาอีกแห่งที่ https://gitlab.com/pythainlp/pythainlp</strong>
</div>

<div align="center">
  <strong>โปรดระมัดระวังซอฟต์แวร์ประสงค์ร้ายหรือมัลแวร์ ถ้าคุณใช้โค้ดจากที่เก็บข้อมูลอื่นนอกเหนือจากที่ GitHub และ GitLab ข้างต้น</strong>
</div>
