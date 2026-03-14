# PyThaiNLP ประมวลผลภาษาไทยด้วย Python

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

[pythainlp.org](https://pythainlp.org/)
| [วิธีใช้งาน](https://pythainlp.org/tutorials)
| [ข้อมูลสัญญาอนุญาต](https://pythainlp.org/dev-docs/notes/license.html)
| [ใบข้อมูลโมเดล](https://github.com/PyThaiNLP/pythainlp/wiki/Model-Cards)
| [ใครใช้ PyThaiNLP บ้าง](https://github.com/PyThaiNLP/pythainlp/blob/dev/INTHEWILD.md)
| *[English README](https://github.com/PyThaiNLP/pythainlp/blob/dev/README.md)*

**PyThaiNLP** ถูกออกแบบให้เป็นเครื่องมือมาตรฐานสำหรับการวิเคราะห์ภาษาศาสตร์ภาษาไทย
ภายใต้สัญญาอนุญาต Apache-2.0 โดยข้อมูลและโมเดลอยู่ภายใต้ CC0-1.0 และ CC-BY-4.0

```sh
pip install pythainlp
```

| รุ่น | รุ่นของ Python | มีอะไรเปลี่ยน | เอกสาร |
| :-: | :-: | :-: | :-: |
| [5.3.1](https://github.com/PyThaiNLP/pythainlp/releases) | 3.9+ | [Log](https://github.com/PyThaiNLP/pythainlp/issues/1080) | [pythainlp.org/docs](https://pythainlp.org/docs) |
| [`dev`](https://github.com/PyThaiNLP/pythainlp/tree/dev) | 3.9+ | [Log](https://github.com/PyThaiNLP/pythainlp/issues/1169) | [pythainlp.org/dev-docs](https://pythainlp.org/dev-docs/) |

## ความสามารถ

- **วิเคราะห์หน่วยทางภาษา:** การแบ่งประโยค คำ และหน่วยคำย่อย
  (`sent_tokenize`, `word_tokenize`, `subword_tokenize`)
- **กำกับหน้าที่ของคำ:** part-of-speech tagging (`pos_tag`)
- **ถอดอักษร:** การถ่ายเสียงเป็นอักษรโรมัน (`transliterate`) และการแปลงเป็น IPA
- **ตรวจตัวสะกด:** การแนะนำและแก้ไขการสะกด (`spell`, `correct`)
- **เครื่องมือเสริม:** soundex, การเรียงลำดับ, แปลงตัวเลขเป็นข้อความ (`bahttext`),
  การจัดรูปแบบวันที่ (`thai_strftime`), และแก้ไขการสลับแป้นพิมพ์
- **คลังภาษา:** ชุดตัวอักษรไทย, รายการคำ, และคำหยุด (stop words)
- **CLI:** ใช้งานทาง command line ด้วย `thainlp`

  ```sh
  thainlp data catalog  # แสดงรายการชุดข้อมูล
  thainlp help          # แสดงวิธีใช้งาน
  ```

## ตัวเลือกการติดตั้ง

การติดตั้งพร้อม extras เฉพาะ (เช่น `translate`, `wordnet`, `full`):

```sh
pip install "pythainlp[extra1,extra2,...]"
```

`extras` ที่ใช้ได้:

<details>
  <summary>รายการสำหรับติดตั้งผ่าน <code>extras</code></summary>

- `compact` — ติดตั้งชุดย่อยที่เสถียรและเล็ก (แนะนำ)
- `full` — ติดตั้ง dependencies ทั้งหมด (อาจเกิดความขัดแย้ง)
- `abbreviation` — เครื่องมือขยายคำย่อ
- `attacut` — รองรับ AttaCut (ตัวตัดคำที่รวดเร็วและแม่นยำ)
- `budoux` — รองรับการแบ่งข้อความด้วย BudouX
- `benchmarks` — รองรับการรันเบนช์มาร์ก
- `coreference_resolution` — รองรับการแก้ไขการอ้างอิงร่วม
- `dependency_parsing` — รองรับการวิเคราะห์โครงสร้างประโยค
- `el` — รองรับการเชื่อมโยงเอนทิตี
- `esupar` — รองรับ ESuPAR parser
- `generate` — รองรับการสร้างข้อความ
- `icu` — รองรับ ICU (International Components for Unicode) ใช้ในการถอดอักษรและการตัดคำ
- `ipa` — รองรับ IPA (International Phonetic Alphabet) ในการถอดอักษร
- `ml` — รองรับโมเดล ULMFiT ที่ใช้ในการจำแนกประเภท
- `mt5` — โมเดล mT5 สำหรับการสรุปข้อความภาษาไทย
- `nlpo3` — รองรับการตัดคำภาษาไทยด้วย nlpo3
- `onnx` — รองรับโมเดล ONNX
- `oskut` — รองรับ OSKUT
- `sefr_cut` — รองรับการตัดคำภาษาไทยด้วย SEFR CUT
- `spacy_thai` — รองรับภาษาไทยใน spaCy
- `spell` — รองรับตัวตรวจการสะกดเพิ่มเติม (phunspell & symspellpy)
- `ssg` — รองรับตัวตัดพยางค์ SSG
- `textaugment` — เครื่องมือเสริมข้อความ
- `thai_nner` — รองรับการจดจำเอนทิตีชื่อภาษาไทย
- `thai2fit` — เวกเตอร์คำภาษาไทย (thai2fit)
- `thai2rom` — การถอดอักษรด้วยแมชชีนเลิร์นนิง
- `transformers_ud` — รองรับ Universal Dependencies ด้วย transformers
- `translate` — รองรับการแปลภาษาด้วยแมชชีน
- `wangchanberta` — โมเดล WangchanBERTa
- `wangchanglm` — รองรับโมเดล WangchanGLM
- `word_approximation` — รองรับการประมาณคำ
- `wordnet` — รองรับ WordNet
- `wsd` — รองรับการแก้ความกำกวมของความหมายคำ (pythainlp.wsd)
- `wtp` — รองรับการแบ่งข้อความด้วย Where's the Point
- `wunsen` — รองรับตัวตรวจการสะกด Wunsen

</details>

สำหรับรายละเอียด dependencies
สามารถดูได้ที่ส่วน `[project.optional-dependencies]` ใน
[`pyproject.toml`](https://github.com/PyThaiNLP/pythainlp/blob/dev/pyproject.toml)

## Environment variables

| ตัวแปร | คำอธิบาย | สถานะ |
|---|---|---|
| `PYTHAINLP_DATA` | พาธของไดเรกทอรีข้อมูล (ค่าเริ่มต้น: `~/pythainlp-data`) | ปัจจุบัน |
| `PYTHAINLP_DATA_DIR` | ชื่อเดิมของ `PYTHAINLP_DATA` แสดง `DeprecationWarning` และหากตั้งค่าทั้งสองพร้อมกันจะเกิด `ValueError` | เลิกใช้แล้ว; ใช้ `PYTHAINLP_DATA` แทน |
| `PYTHAINLP_OFFLINE` | ตั้งเป็น `1` เพื่อปิดการดาวน์โหลดคลังภาษาอัตโนมัติ การเรียก `download()` โดยตรงยังคงใช้งานได้ | ปัจจุบัน |
| `PYTHAINLP_READ_ONLY` | ตั้งเป็น `1` เพื่อเปิดโหมดอ่านอย่างเดียว ป้องกันการเขียนในฉากหลังที่ผู้ใช้อาจไม่ทราบ (ดาวน์โหลดคลังภาษา, ปรับปรุงแค็ตตาล็อก, สร้างไดเรกทอรี) การบันทึกแฟ้มที่ผู้ใช้ระบุเองไม่ได้รับผลกระทบ | ปัจจุบัน |
| `PYTHAINLP_READ_MODE` | ชื่อเดิมของ `PYTHAINLP_READ_ONLY` แสดง `DeprecationWarning` และหากตั้งค่าทั้งสองพร้อมกันจะเกิด `ValueError` | เลิกใช้แล้ว; ใช้ `PYTHAINLP_READ_ONLY` แทน |

### ไดเรกทอรีข้อมูล

PyThaiNLP ดาวน์โหลดข้อมูล (ดูแค็ตตาล็อกข้อมูล `db.json` ที่
[pythainlp-corpus](https://github.com/PyThaiNLP/pythainlp-corpus))
ไปที่ `~/pythainlp-data` ตามค่าเริ่มต้น
ตั้งค่า environment variable `PYTHAINLP_DATA` เพื่อเปลี่ยนตำแหน่งนี้
(`PYTHAINLP_DATA_DIR` ยังคงใช้ได้ แต่จะเลิกใช้ในอนาคต)

เมื่อใช้ PyThaiNLP ในสภาพแวดล้อมการคำนวณแบบกระจาย
(เช่น Apache Spark) ให้ตั้งค่า environment variable `PYTHAINLP_DATA`
ภายในฟังก์ชันที่จะถูกกระจายไปยัง worker nodes
ดูรายละเอียดใน[เอกสาร](https://pythainlp.org/dev-docs/notes/installation.html)

### โหมดออฟไลน์

ตั้งค่า `PYTHAINLP_OFFLINE=1` เพื่อปิดการดาวน์โหลดคลังภาษาหรือโมเดลภาษา **อัตโนมัติ**
เมื่อตั้งค่าตัวแปรนี้และไม่มีแฟ้มในเครื่อง จะเกิด `FileNotFoundError`
แทนที่จะพยายามดาวน์โหลดจากเครือข่าย
การเรียก `pythainlp.corpus.download()` โดยตรงยังคงทำงานได้ตามปกติ
ใช้ `pythainlp.is_offline_mode()` เพื่อตรวจสอบสถานะปัจจุบันในโค้ด

```python
import pythainlp
print(pythainlp.is_offline_mode())  # True ถ้า PYTHAINLP_OFFLINE=1
```

### โหมดอ่านอย่างเดียว

ตั้งค่า `PYTHAINLP_READ_ONLY=1` เพื่อป้องกันการเขียนในฉากหลังที่เกิดขึ้นโดยอัตโนมัติ
ในไดเรกทอรีข้อมูลภายในของ PyThaiNLP ได้แก่ การดาวน์โหลดคลังภาษา, การปรับปรุงแค็ตตาล็อก
และการสร้างไดเรกทอรีข้อมูล — การเขียนเหล่านี้เกิดขึ้นเป็นผลข้างเคียงที่ผู้ใช้อาจไม่ทราบ

การดำเนินการที่ผู้ใช้ระบุ path เอาไว้อย่างชัดเจนจะไม่ได้รับผลกระทบ
เช่น `model.save("path")`, `tagger.train(..., save_loc="path")`,
`thainlp misspell --output myfile.txt`

ใช้ `pythainlp.is_read_only_mode()` เพื่อตรวจสอบสถานะปัจจุบันในโค้ด

```python
import pythainlp
print(pythainlp.is_read_only_mode())  # True ถ้า PYTHAINLP_READ_ONLY=1
```

## การทดสอบ

เราทดสอบฟังก์ชันหลักบน Python ทุกเวอร์ชันที่รองรับอย่างเป็นทางการ

ดู [tests/README.md](./tests/README.md) สำหรับ test matrix และรายละเอียดอื่น ๆ

## ร่วมพัฒนา PyThaiNLP

กรุณา fork และสร้าง pull request
ดู [CONTRIBUTING.md](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md)
สำหรับแนวทางและการอ้างอิงอัลกอริทึม

## การอ้างอิง

หากคุณใช้ซอฟต์แวร์ `PyThaiNLP` ในโครงงานหรืองานวิจัยของคุณ คุณสามารถอ้างอิงได้ตามนี้:

> Phatthiyaphaibun, Wannaphong, Korakot Chaovavanich, Charin Polpanumas,
> Arthit Suriyawongkul, Lalita Lowphansirikul, and Pattarawat Chormai.
> “PyThaiNLP: Thai Natural Language Processing in Python”.
> Zenodo, 2 June 2024. <https://doi.org/10.5281/zenodo.3519354>.

โดยใช้รายการ BibTeX นี้:

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

หากคุณอ้างอิงงานวิจัยของเราในงานประชุมวิชาการ
[NLP-OSS 2023](https://nlposs.github.io/2023/)
คุณสามารถอ้างอิงได้ตามนี้:

> Wannaphong Phatthiyaphaibun, Korakot Chaovavanich, Charin Polpanumas,
> Arthit Suriyawongkul, Lalita Lowphansirikul, Pattarawat Chormai,
> Peerat Limkonchotiwat, Thanathip Suntorntip, and Can Udomcharoenchaikit.
> 2023.
> [PyThaiNLP: Thai Natural Language Processing in Python.](https://aclanthology.org/2023.nlposs-1.4)
> In Proceedings of the 3rd Workshop for Natural Language Processing
> Open Source Software (NLP-OSS 2023),
> pages 25–36, Singapore, Singapore.
> Empirical Methods in Natural Language Processing.

โดยใช้รายการ BibTeX นี้:

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

## สัญญาอนุญาต

| เนื้อหา | สัญญาอนุญาต |
| :-- | :-- |
| ซอร์สโค้ดและโน๊ตบุ๊กของ PyThaiNLP | [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE) |
| คลังข้อมูล ชุดข้อมูล และเอกสารที่สร้างโดยโครงการ PyThaiNLP | [Creative Commons Zero 1.0 Universal Public Domain Dedication License (CC0)](https://creativecommons.org/publicdomain/zero/1.0/)|
| โมเดลภาษาที่สร้างโดยโครงการ PyThaiNLP | [Creative Commons Attribution 4.0 International Public License (CC-BY)](https://creativecommons.org/licenses/by/4.0/) |
| คลังข้อมูลและโมเดลอื่น ๆ ที่อาจมาพร้อมกับ PyThaiNLP | ดู [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md) |

## ผู้สนับสนุน

โครงการ PyThaiNLP ก่อตั้งโดย วรรณพงษ์  ภัททิยไพบูลย์ ในปี พ.ศ. 2559
การพัฒนาในโครงการ PyThaiNLP ของวรรณพงษ์ ตั้งแต่ปี พ.ศ. 2564
เกิดขึ้นระหว่างการสนับสนุนทุนการศึกษาระดับปริญญาเอกโดย
[สถาบันวิทยสิริเมธี (VISTEC)][vistec]

การพัฒนาในโครงการ PyThaiNLP ของ อาทิตย์ สุริยะวงศ์กุล
ตั้งแต่พฤศจิกายน พ.ศ. 2560 ถึงสิงหาคม พ.ศ. 2562
สนับสนุนโดยบริษัท [Wisesight][]
และตั้งแต่เดือนพฤศจิกายน พ.ศ. 2562 ถึงตุลาคม พ.ศ. 2566
เกิดขึ้นระหว่างการสนับสนุนทุนการศึกษาระดับปริญญาเอกโดย
[Taighde Éireann – Research Ireland][researchireland]
ภายใต้เลขที่ทุน 18/CRT/6224
([Research Ireland Centre for Research Training in Digitally-Enhanced Reality (d-real)][dreal])

การพัฒนาในโครงการ PyThaiNLP ของ ภัทรวัต ช่อไม้
ตั้งแต่ปี พ.ศ. 2561 ถึง พ.ศ. 2562
เกิดขึ้นระหว่างการเป็นนักวิจัย ณ
[ห้องปฏิบัติการประมวลผลภาษาธรรมชาติ
ภาควิชาภาษาศาสตร์ คณะอักษรศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย][nlp-chula]

การพัฒนาในโครงการ PyThaiNLP ของ กรกฎ เชาวะวณิช และ ลลิตา โล่พันธุ์ศิริกุล
ตั้งแต่ปี พ.ศ. 2562 ถึง พ.ศ. 2565
สนับสนุนโดย
[สถาบันวิจัยปัญญาประดิษฐ์ประเทศไทย (VISTEC-depa Thailand AI Research Institute)][airesearch]

เครื่อง Mac Mini M1 ที่ใช้สำหรับการทดสอบระบบบน macOS บริจาคโดย [MacStadium][]
ฮาร์ดแวร์นี้ช่วยให้การทดสอบซอฟต์แวร์ของโครงการเป็นไปอย่างครบถ้วนมากขึ้น
ระหว่างเดือนตุลาคม พ.ศ. 2565 ถึงตุลาคม พ.ศ. 2566
ซึ่งเป็นช่วงก่อนที่ GitHub Actions จะรองรับ Apple Silicon อย่างเป็นทางการ

[vistec]: https://www.vistec.ac.th/
[airesearch]: https://airesearch.in.th/
[wisesight]: https://wisesight.com/
[researchireland]: https://www.researchireland.ie/
[dreal]: https://d-real.ie/
[nlp-chula]: https://attapol.github.io/lab.html
[macstadium]: https://www.macstadium.com/

![VISTEC-depa Thailand AI Research Institute](./docs/images/airesearch-logo.png)
![MacStadium](./docs/images/macstadium-logo.png)

เรามีที่เก็บข้อมูลอย่างเป็นทางการที่เดียวที่
<https://github.com/PyThaiNLP/pythainlp>
และมีที่เก็บสำเนาอีกแห่งที่
<https://gitlab.com/pythainlp/pythainlp>.

โปรดระมัดระวังซอฟต์แวร์ประสงค์ร้ายหรือมัลแวร์
ถ้าคุณใช้โค้ดจากที่เก็บข้อมูลอื่นนอกเหนือจาก 2 แหล่งนี้

สร้างด้วย ❤️ | ทีม PyThaiNLP 💻 | "เราสร้างการประมวลผลภาษาไทย" 🇹🇭
