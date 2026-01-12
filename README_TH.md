<div align="center">
  <img src="https://avatars0.githubusercontent.com/u/32934255?s=200&v=4"/>
  <h1>PyThaiNLP: Thai Natural Language Processing in Python</h1>
  <a href="https://www.repostatus.org/#active"><img alt="Project Status: Active – The project has reached a stable, usable state and is being actively developed." src="https://www.repostatus.org/badges/latest/active.svg"/></a>
  <a href="https://pypi.python.org/pypi/pythainlp"><img alt="pypi" src="https://img.shields.io/pypi/v/pythainlp.svg"/></a>
  <a href="https://www.python.org/downloads/"><img alt="Python 3.9" src="https://img.shields.io/badge/python-3.9-blue.svg"/></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"/></a>
  <a href="https://www.codacy.com/gh/PyThaiNLP/pythainlp/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PyThaiNLP/pythainlp&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/5821a0de122041c79999bbb280230ffb"/></a>
  <a href="https://coveralls.io/github/PyThaiNLP/pythainlp?branch=dev"><img alt="Coverage Status" src="https://coveralls.io/repos/github/PyThaiNLP/pythainlp/badge.svg?branch=dev"/></a>
  <a href="https://colab.research.google.com/github/PyThaiNLP/tutorials/blob/master/source/notebooks/pythainlp_get_started.ipynb"><img alt="Google Colab Badge" src="https://badgen.net/badge/Launch%20Quick%20Start%20Guide/on%20Google%20Colab/blue?icon=terminal"/></a>
  <a href="https://doi.org/10.5281/zenodo.3519354"><img alt="DOI" src="https://zenodo.org/badge/DOI/10.5281/zenodo.3519354.svg"/></a>
  <a href="https://matrix.to/#/#thainlp:matrix.org" rel="noopener" target="_blank"><img src="https://matrix.to/img/matrix-badge.svg" alt="Chat on Matrix"></a>
</div>

PyThaiNLP เป็นไลบารีภาษาไพทอนสำหรับประมวลผลภาษาธรรมชาติ โดยเน้นภาษาไทย

## ติดตั้งแบบด่วน

```sh
pip install pythainlp
```

| รุ่น | คำอธิบาย | สถานะ |
|:------:|:--:|:------:|
| [5.2.0](https://github.com/PyThaiNLP/pythainlp/releases) | Stable | [Change Log](https://github.com/PyThaiNLP/pythainlp/issues/1080) |
| [`dev`](https://github.com/PyThaiNLP/pythainlp/tree/dev) | Release Candidate for 5.3  | [Change Log](https://github.com/PyThaiNLP/pythainlp/issues/1169) |

ติดตามพวกเราบน [PyThaiNLP Facebook page](https://www.facebook.com/pythainlp/) เพื่อรับข่าวสารเพิ่มเติม

## เริ่มต้นกับ PyThaiNLP

พวกเราได้จัดทำ [PyThaiNLP Get Started Tutorial](https://pythainlp.org/tutorials/notebooks/pythainlp_get_started.html) สำหรับสำรวจความสามารถของ PyThaiNLP; พวกเรามีเอกสารสอนใช้งาน สามารถศึกษาได้ที่ [หน้า tutorial](https://pythainlp.org/tutorials).

อ่านเอกสารล่าสุดได้ที่ [https://pythainlp.org/docs](https://pythainlp.org/docs).

พวกเราพยายามทำให้โมดูลใช้งานได้ง่ายที่สุดเท่าที่จะเป็นไปได้; ตัวอย่างเช่น บางชุดข้อมูล (เช่น รายการคำและตัวแบบภาษา) จะถูกดาวน์โหลดอัตโนมัติเมื่อมีการเรียกใช้งาน โดย PyThaiNLP จะจัดเก็บข้อมูลเหล่านั้นไว้ในโฟลเดอร์ `~/pythainlp-data` เป็นค่าเริ่มต้น แต่ผู้ใช้งานสามารถระบุตำแหน่งที่ต้องการได้เองผ่านค่า environment variable `PYTHAINLP_DATA_DIR` อ่านรายละเอียดคลังข้อมูลเพิ่มเติมได้ที่ [PyThaiNLP/pythainlp-corpus](https://github.com/PyThaiNLP/pythainlp-corpus).

## ความสามารถ

PyThaiNLP มีความสามารถพื้นฐานสำหรับการประมวลผลภาษาไทย ตัวอย่างเช่นการกำกับหน้าที่ของคำ (part-of-speech tagging) การแบ่งหน่วยของข้อความตามหลักภาษาศาสตร์ (พยางค์ คำ และประโยค) บางความสามารถสามารถใช้งานได้ผ่านทางคอมมานด์ไลน์

<details>
  <summary>รายการความสามารถ</summary>

- ชุดตัวอักขระและคำภาษาไทยที่เรียกใช้ได้สะดวก เช่น พยัญชนะ (`pythainlp.thai_consonants`), สระ (`pythainlp.thai_vowels`), ตัวเลข (`pythainlp.thai_digits`), และคำหยุด (stop word) (`pythainlp.corpus.thai_stopwords`) -- ซึ่งเทียบได้กับค่าคงที่มาตรฐานในไพทอนอย่าง `string.letters`, `string.digits`, และ `string.punctuation`
- Thai linguistic unit segmentation/tokenization, including sentence (`sent_tokenize`), word (`word_tokenize`), and subword segmentations based on Thai Character Cluster (`subword_tokenize`)
- Thai part-of-speech taggers (`pos_tag`)
- Thai spelling suggestion and correction (`spell` and `correct`)
- Thai transliteration (`transliterate`)
- Thai soundex (`soundex`) with three engines (`lk82`, `udom83`, `metasound`)
- Thai collation (sort by dictionoary order) (`collate`)
- Read out number to Thai words (`bahttext`, `num_to_thaiword`)
- Thai datetime formatting (`thai_strftime`)
- Thai-English keyboard misswitched fix (`eng_to_thai`, `thai_to_eng`)
- Command-line interface for basic functions, like tokenization and pos tagging (run `thainlp` in your shell)

</details>

อ่านรายละเอียดได้ที่ [tutorials](https://pythainlp.org/tutorials)

## การติดตั้ง

```sh
pip install --upgrade pythainlp
```

วิธีดังกล่าวเป็นการติดตั้งรุ่นเสถียรของ PyThaiNLP
PyThaiNLP ใช้ pip สำหรับจัดการโมดูลและใช้ PyPI เป็นช่องทางหลักในการแจกจ่ายโมดูล อ่านรายละเอียดได้ที่ [https://pypi.org/project/pythainlp/](https://pypi.org/project/pythainlp/)

ความแตกต่างในแต่ละรุ่น:

- รุ่นเสถียร: `pip install --upgrade pythainlp`
- รุ่นก่อนเสถียร (near ready): `pip install --upgrade --pre pythainlp`
- รุ่นที่กำลังพัฒนา (likely to break things): `pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip`

### ตัวเลือกการติดตั้ง

บางความสามารถ เช่น Thai WordNet ต้องการโมดูลภายนอกในการทำงานนอกจาก PyThaiNLP ซึ่งในตอนติดตั้ง คุณจะต้องติดตั้งส่วนขยายพิเศษที่จำเป็นหรือ "extras" โดยระบุชื่อลงใน `[name]` ต่อท้าย `pythainlp`:

```sh
pip install pythainlp[extra1,extra2,...]
```

<details>
  <summary>รายการสำหรับติดตั้งผ่าน <code>extras</code></summary>

- `full` (ติดตั้งทุกอย่าง)
- `compact` (ติดตั้งไลบารีชุดเล็กที่ทดสอบแล้วว่าไม่ตีกันเองและติดตั้งได้ในทุกระบบปฏิบัติการ)
- `abbreviation` (สำหรับการย่อคำภาษาไทย)
- `attacut` (เพื่อสนับสนุน attacut ซึ่งเป็นตัวตัดคำที่ทำงานได้รวดเร็วและมีประสิทธิภาพ)
- `benchmarks` (สำหรับ [word tokenization benchmarking](tokenization-benchmark.md))
- `budoux` (สำหรับการแบ่งข้อความด้วย BudouX)
- `coreference_resolution` (สำหรับการหาคำที่อ้างอิงถึงกัน)
- `dependency_parsing` (สำหรับการวิเคราะห์โครงสร้างประโยค)
- `el` (สำหรับการเชื่อมโยงเอนทิตี)
- `esupar` (สำหรับการรองรับ esupar parser)
- `generate` (สำหรับการสร้างข้อความ)
- `icu` (สำหรับการรองรับ ICU หรือ International Components for Unicode ในการถอดเสียงเป็นอักษรและการตัดแบ่งคำ)
- `ipa` (สำหรับการรองรับ IPA หรือ International Phonetic Alphabet ในการถอดเสียงเป็นอักษร)
- `ml` (เพื่อให้สนับสนุนตัวแบบภาษา ULMFiT สำหรับการจำแนกข้อความ)
- `mt5` (สำหรับรองรับโมเดล mT5)
- `nlpo3` (สำหรับตัวตัดคำภาษาไทย nlpo3)
- `onnx` (สำหรับรองรับโมเดล ONNX)
- `oskut` (สำหรับตัวตัดคำภาษาไทย OSKut)
- `sefr_cut` (สำหรับตัวตัดคำภาษาไทย SEFR CUT)
- `spacy_thai` (สำหรับรองรับภาษาไทยใน spaCy)
- `spell` (สำหรับการแก้ไขคำสะกดผิด)
- `ssg` (สำหรับการแบ่งประโยค)
- `testing` (เวอร์ชันที่ปักหมุดสำหรับ CI/CD)
- `textaugment` (สำหรับการเพิ่มข้อมูลข้อความ)
- `thai_nner` (สำหรับการจดจำชื่อเฉพาะภาษาไทย)
- `thai2fit` (สำหรับ Thai word vector)
- `thai2rom` (สำหรับการถอดอักษรไทยเป็นอักษรโรมัน)
- `transformers_ud` (สำหรับ Universal Dependencies ด้วย transformers)
- `translate` (สำหรับการแปลภาษา)
- `wangchanberta` (สำหรับโมเดล WangchanBERTa)
- `wangchanglm` (สำหรับโมเดล WangchanGLM)
- `word_approximation` (สำหรับการประมาณคำ)
- `wordnet` (สำหรับ Thai WordNet API)
- `wsd` (สำหรับการแก้ความกำกวมของความหมายคำ)
- `wtp` (สำหรับการแบ่งข้อความด้วย Where's the Point)
- `wunsen` (สำหรับตัวตรวจการสะกดคำ Wunsen)

</details>

สำหรับโมดูลที่ต้องการ สามารถดูรายละเอียดได้ที่ส่วน `[project.optional-dependencies]` ใน [`pyproject.toml`](https://github.com/PyThaiNLP/pythainlp/blob/dev/pyproject.toml).

## Command-line

บางความสามารถของ PyThaiNLP สามารถใช้งานผ่าน command line ได้โดยใช้ `thainlp`

ตัวอย่าง, แสดงรายละเอียดของชุดข้อมูล:

```sh
thainlp data catalog
```

แสดงวิธีใช้งาน:

```sh
thainlp help
```

## ผู้ใช้งาน Python 2

- PyThaiNLP สนับสนุน Python 3.9 ขึ้นไป บางความสามารถ สามารถใช้งานกับ Python 3 รุ่นก่อนหน้าได้ แต่ไม่ได้มีการทดสอบว่าใช้งานได้หรือไม่ อ่านเพิ่มเติม [1.7 -> 2.0 change log](https://github.com/PyThaiNLP/pythainlp/issues/118).
  - [Upgrading from 1.7](https://pythainlp.org/docs/2.0/notes/pythainlp-1_7-2_0.html)
  - [Upgrade ThaiNER from 1.7](https://github.com/PyThaiNLP/pythainlp/wiki/Upgrade-ThaiNER-from-PyThaiNLP-1.7-to-PyThaiNLP-2.0)
- ผู้ใช้งาน Python 2.7 สามารถใช้งาน PyThaiNLP 1.6

## การอ้างอิง

หากคุณใช้ซอฟต์แวร์ `PyThaiNLP` ในโครงงานหรืองานวิจัยของคุณ คุณสามารถอ้างอิงได้ตามนี้

> Phatthiyaphaibun, Wannaphong, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, and Pattarawat Chormai. “Pythainlp: Thai Natural Language Processing in Python”. Zenodo, 2 June 2024. <http://doi.org/10.5281/zenodo.3519354>.

โดยสามารถใช้ BibTeX นี้:

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

บทความของเราในงานประชุมวิชาการ [NLP-OSS 2023](https://nlposs.github.io/2023/):

> Wannaphong Phatthiyaphaibun, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, Pattarawat Chormai, Peerat Limkonchotiwat, Thanathip Suntorntip, and Can Udomcharoenchaikit. 2023. [PyThaiNLP: Thai Natural Language Processing in Python.](https://aclanthology.org/2023.nlposs-1.4) In Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023), pages 25–36, Singapore, Singapore. Empirical Methods in Natural Language Processing.

โดยสามารถใช้ BibTeX นี้:

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

## ร่วมสนับสนุน PyThaiNLP

- กรุณา fork แล้วพัฒนาต่อ จากนั้นสร้าง pull request กลับมา :)
- สำหรับเอกสารแนะนำและอื่น ๆ รวมถึงการอ้างอิงขั้นตอนที่เราใช้งาน สามารถเข้าไปศึกษาเพิ่มเติมได้ที่หน้า [contributing](https://github.com/PyThaiNLP/pythainlp/blob/dev/CONTRIBUTING.md)

## ใครใช้ PyThaiNLP?

คุณสามารถอ่านได้ที่ [INTHEWILD.md](https://github.com/PyThaiNLP/pythainlp/blob/dev/INTHEWILD.md)

## สัญญาอนุญาต

| | สัญญาอนุญาต |
|:---|:----|
| ต้นรหัสซอร์สโค้ดและโน๊ตบุ๊กของ PyThaiNLP | [Apache Software License 2.0](https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE) |
| ฐานข้อมูลภาษา ชุดข้อมูล และเอกสารที่สร้างโดยโครงการ PyThaiNLP | [Creative Commons Zero 1.0 Universal Public Domain Dedication License (CC0)](https://creativecommons.org/publicdomain/zero/1.0/)|
| Language models created by PyThaiNLP | [Creative Commons Attribution 4.0 International Public License (CC-by)](https://creativecommons.org/licenses/by/4.0/)  |
| สำหรับฐานข้อมูลภาษาและโมเดลอื่นที่อาจมาพร้อมกับซอฟต์แวร์ PyThaiNLP | ดู [Corpus License](https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/corpus_license.md) |

## บัตรโมเดล

สำหรับรายละเอียดทางเทคนิค ข้อควรระวัง และข้อคำนึงทางจริยธรรมของตัวแบบ (โมเดล) ที่ใช้ใน PyThaiNLP
กรุณาดูที่ [Model cards](https://github.com/PyThaiNLP/pythainlp/wiki/Model-Cards)

## ผู้สนับสนุน

[![VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/assets/img/logo/airesearch-logo.svg)](https://airesearch.in.th/)

ตั้งแต่ปี 2562 การสมทบพัฒนา PyThaiNLP โดย กรกฎ เชาวะวณิช และ ลลิตา โล่พันธุ์ศิริกุล สนับสนุนโดย [VISTEC-depa Thailand Artificial Intelligence Research Institute](https://airesearch.in.th/)

------

<div align="center">
  สร้างด้วย ❤️ | ทีม PyThaiNLP 💻 |  "เราสร้างการประมวลผลภาษาไทย" 🇹🇭
</div>

------

<div align="center">
  <strong>เรามีที่เก็บข้อมูลอย่างเป็นทางการที่เดียวที่ https://github.com/PyThaiNLP/pythainlp และมีที่เก็บสำเนาอีกแห่งที่ https://gitlab.com/pythainlp/pythainlp</strong>
</div>

<div align="center">
  <strong>โปรดระมัดระวังซอฟต์แวร์ประสงค์ร้ายหรือมัลแวร์ ถ้าคุณใช้โค้ดจากที่เก็บข้อมูลอื่นนอกเหนือจากที่ GitHub และ GitLab ข้างต้น</strong>
</div>
