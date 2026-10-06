---
SPDX-FileCopyrightText: 2025-2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

<!-- markdownlint-disable MD024 -->

# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- Full release notes: <https://github.com/PyThaiNLP/pythainlp/releases>
- Commit history: <https://github.com/PyThaiNLP/pythainlp/compare/v5.3.8...dev>

## [Unreleased]

### Changed

- `pythainlp.tokenize.deepcut`: built-in ONNX engine replaces the
  TensorFlow-based `deepcut`; `custom_dict` is no longer applied ([#1372])
- Improve guardrails in `check_sara()` and `nighit()` ([#1453])

### Fixed

- `pythainlp.corpus.wordnet`: Thai WordNet with NLTK 3.10+; `all_synsets()`
  `NameError`; `langs()` missing `tha` ([#1541])
- `check_klon()` and `get_corpus_db()` no longer swallow unexpected
  exceptions ([#1542])
- `download()`: download and extract via temporary paths, so a failed
  download keeps the installed corpus; handle empty `db.json` keys ([#NNNN])
- `db.json` is written atomically and keeps its mode and symlink ([#NNNN])

### Security

- Tar and zip extraction rejects absolute and escaping links; unsafe tar
  members raise `ValueError` ([#NNNN])
- Without `tarfile.data_filter`, tar extraction rejects all links and special
  files and drops owners ([#NNNN])

[#1372]: https://github.com/PyThaiNLP/pythainlp/pull/1372
[#1453]: https://github.com/PyThaiNLP/pythainlp/pull/1453
[#1541]: https://github.com/PyThaiNLP/pythainlp/pull/1541
[#1542]: https://github.com/PyThaiNLP/pythainlp/pull/1542
[#NNNN]: https://github.com/PyThaiNLP/pythainlp/pull/NNNN

## [5.3.8] - 2026-09-25

### Deprecated

- `pythainlp.generate.thai2fit`, `pythainlp.generate.wangchanglm`, and
  `pythainlp.chat` ([#1519])

### Fixed

- `thai2rom`, `thai2rom_onnx`, and `thaig2p` transliteration: stop decoding at
  a repeating cycle, not at the 100-character cap ([#1500], [#1501])
- `pythainlp.util.text_to_num`: handle Thai zero ("ศูนย์") in floats ([#1503])

[#1500]: https://github.com/PyThaiNLP/pythainlp/pull/1500
[#1501]: https://github.com/PyThaiNLP/pythainlp/pull/1501
[#1503]: https://github.com/PyThaiNLP/pythainlp/pull/1503
[#1519]: https://github.com/PyThaiNLP/pythainlp/pull/1519

## [5.3.7] - 2026-08-14

Same as 5.3.6, with the release problem fixed.

## [5.3.6] - 2026-08-14

### Fixed

- `num_to_thaiword`: fix "เอ็ด" rule ([#1461])
- `romanize` with `royin`: handle words containing "ฤ" ([#1473])

[#1461]: https://github.com/PyThaiNLP/pythainlp/pull/1461
[#1473]: https://github.com/PyThaiNLP/pythainlp/pull/1473

## [5.3.5] - 2026-07-30

### Fixed

- `Seq2Seq`: remove unconditional overwrite that disabled teacher forcing
  ([#1380])
- `ulmfit` `replace_url`: fix ReDoS found by CodeQL ([#1400])
- `_clean_ipa`: remove duplicate mid-tone `.replace` ([#1409])
- Change loop limit from 20 to `dec_maxlen` ([#1464])

[#1380]: https://github.com/PyThaiNLP/pythainlp/pull/1380
[#1400]: https://github.com/PyThaiNLP/pythainlp/pull/1400
[#1409]: https://github.com/PyThaiNLP/pythainlp/pull/1409
[#1464]: https://github.com/PyThaiNLP/pythainlp/pull/1464

## [5.3.4] - 2026-04-02

### Fixed

- Value range checks ([#1374], [#1379], [#1382])
- "1001" to "หนึ่งพันเอ็ด" rule ([#1386])
- Build WSD `Trie` after populating the dictionary ([#1388])

[#1374]: https://github.com/PyThaiNLP/pythainlp/pull/1374
[#1379]: https://github.com/PyThaiNLP/pythainlp/pull/1379
[#1382]: https://github.com/PyThaiNLP/pythainlp/pull/1382
[#1386]: https://github.com/PyThaiNLP/pythainlp/pull/1386
[#1388]: https://github.com/PyThaiNLP/pythainlp/pull/1388

## [5.3.3] - 2026-03-26

### Added

- `EntitySpan` `TypedDict` for type checking of tagged entities ([#1363])

### Fixed

- `thai2rom_onnx`: fix ONNX encoder model and inference ([#1349])
- `wordnet`: fix `AttributeError` ([#1354])

### Security

- Replace `os.path.join` with `safe_path_join` to prevent path
  traversal (CWE-22) ([#1369])

[#1349]: https://github.com/PyThaiNLP/pythainlp/pull/1349
[#1354]: https://github.com/PyThaiNLP/pythainlp/pull/1354
[#1363]: https://github.com/PyThaiNLP/pythainlp/pull/1363
[#1369]: https://github.com/PyThaiNLP/pythainlp/pull/1369

## [5.3.2] - 2026-03-19

### Added

- `pythainlp.chunk` module for chunking, following the NLTK `nltk.chunk`
  convention ([#1339])

### Deprecated

Removed in 6.0 ([#1339]):

- `pythainlp.util.isthaichar()`: use `is_thai_char()`
- `pythainlp.util.isthai()`: use `is_thai()`
- `pythainlp.util.countthai()`: use `count_thai()`
- `pythainlp.tag.crfchunk.CRFchunk`: use `pythainlp.chunk.CRFChunkParser`
- `pythainlp.tag.chunk_parse()`: use `pythainlp.chunk.chunk_parse()`

### Security

- Prevent path traversal: keep paths within their base directory ([#1342])

[#1339]: https://github.com/PyThaiNLP/pythainlp/pull/1339
[#1342]: https://github.com/PyThaiNLP/pythainlp/pull/1342

## [5.3.1] - 2026-03-14

### Security

- `thai2fit`: use JSON model instead of pickle ([#1325])
- Validate fields before processing in corpus loading ([#1327])
- `w2p`: use npz model instead of pickle ([#1328])

[#1325]: https://github.com/PyThaiNLP/pythainlp/pull/1325
[#1327]: https://github.com/PyThaiNLP/pythainlp/pull/1327
[#1328]: https://github.com/PyThaiNLP/pythainlp/pull/1328

## [5.3.0] - 2026-03-10

The minimum Python version is now 3.9.

### Added

- Tapsai et al. 2020 soundex ([#1175])
- Thai profanity detection ([#1183])
- Qwen3-0.6B language model ([#1217])
- Thai-NNER integration with top-level entity filtering ([#1221])
- `pythainlp.braille` module for Thai braille conversion ([#1287])
- BLEU, ROUGE, WER, and CER metrics in `pythainlp.benchmarks` ([#1295])
- `attaparse` engine for `dependency_parsing` ([#1303])
- `pythainlp.is_offline_mode()`; `PYTHAINLP_OFFLINE=1` disables corpus
  downloads; `get_corpus_path()` raises `FileNotFoundError` ([#1306])
- Thai consonant cluster detection (`check_khuap_klam`) ([#1308])
- `pythainlp.is_read_only_mode()`; `PYTHAINLP_READ_ONLY=1` blocks writes
  ([#1317])

### Changed

- Optimize performance ([#1182], [#1237], [#1320])
- Lazy-load dictionaries to reduce memory use ([#1186])
- Move configuration to `pyproject.toml` ([#1188], [#1190], [#1226], [#1239])
- Update type hints to Python 3.9 features ([#1189], [#1190], [#1232], [#1262],
  [#1263], [#1264], [#1274])
- Make the package zip-safe ([#1212])
- Make tokenizers thread-safe ([#1213])
- Replace the TNC word frequency dataset with Phupha filtered by ORST words
  ([#1284])
- Migrate build backend to `hatchling` ([#1311])

### Deprecated

- `PYTHAINLP_DATA_DIR`: use `PYTHAINLP_DATA` ([#1306])
- `PYTHAINLP_READ_MODE`: use `PYTHAINLP_READ_ONLY` ([#1317])

### Removed

- Duplicate entries in the Volubilis dictionary ([#1200])
- Star imports ([#1207])
- `requests` dependency ([#1211])
- `pythainlp.util.is_native_thai`: use `pythainlp.morpheme.is_native_thai`
  ([#1315])

### Fixed

- `royin` romanization: consonant cluster boundary ([#1172])
- `check_marttra()`: final consonant classification ([#1173])
- Base dependencies ([#1185])
- `tltk` transliteration: Kho Khon alphabet ([#1187])
- `tone_detector()` and `sound_syllable()` bugs ([#1197])
- `normalize()`: remove spaces before tone marks and non-base characters
  ([#1222])
- Suppress Gensim duplicate-word warnings when loading word2vec ([#1316])
- Create `db.json` lazily, on the first corpus download ([#1317])
- `newmm`: exponential time on text with many ambiguous breaks ([#1319])
- `Trie`: reduce memory use and speed up TCC boundary lookups ([#1323])

### Security

- Prevent path traversal and symlink attacks in archive extraction ([#1225])

[#1172]: https://github.com/PyThaiNLP/pythainlp/pull/1172
[#1173]: https://github.com/PyThaiNLP/pythainlp/pull/1173
[#1175]: https://github.com/PyThaiNLP/pythainlp/pull/1175
[#1182]: https://github.com/PyThaiNLP/pythainlp/pull/1182
[#1183]: https://github.com/PyThaiNLP/pythainlp/pull/1183
[#1185]: https://github.com/PyThaiNLP/pythainlp/pull/1185
[#1186]: https://github.com/PyThaiNLP/pythainlp/pull/1186
[#1187]: https://github.com/PyThaiNLP/pythainlp/pull/1187
[#1188]: https://github.com/PyThaiNLP/pythainlp/pull/1188
[#1189]: https://github.com/PyThaiNLP/pythainlp/pull/1189
[#1190]: https://github.com/PyThaiNLP/pythainlp/pull/1190
[#1197]: https://github.com/PyThaiNLP/pythainlp/pull/1197
[#1200]: https://github.com/PyThaiNLP/pythainlp/pull/1200
[#1207]: https://github.com/PyThaiNLP/pythainlp/pull/1207
[#1211]: https://github.com/PyThaiNLP/pythainlp/pull/1211
[#1212]: https://github.com/PyThaiNLP/pythainlp/pull/1212
[#1213]: https://github.com/PyThaiNLP/pythainlp/pull/1213
[#1217]: https://github.com/PyThaiNLP/pythainlp/pull/1217
[#1221]: https://github.com/PyThaiNLP/pythainlp/pull/1221
[#1222]: https://github.com/PyThaiNLP/pythainlp/pull/1222
[#1225]: https://github.com/PyThaiNLP/pythainlp/pull/1225
[#1226]: https://github.com/PyThaiNLP/pythainlp/pull/1226
[#1232]: https://github.com/PyThaiNLP/pythainlp/pull/1232
[#1237]: https://github.com/PyThaiNLP/pythainlp/pull/1237
[#1239]: https://github.com/PyThaiNLP/pythainlp/pull/1239
[#1262]: https://github.com/PyThaiNLP/pythainlp/pull/1262
[#1263]: https://github.com/PyThaiNLP/pythainlp/pull/1263
[#1264]: https://github.com/PyThaiNLP/pythainlp/pull/1264
[#1274]: https://github.com/PyThaiNLP/pythainlp/pull/1274
[#1284]: https://github.com/PyThaiNLP/pythainlp/pull/1284
[#1287]: https://github.com/PyThaiNLP/pythainlp/pull/1287
[#1295]: https://github.com/PyThaiNLP/pythainlp/pull/1295
[#1303]: https://github.com/PyThaiNLP/pythainlp/pull/1303
[#1306]: https://github.com/PyThaiNLP/pythainlp/pull/1306
[#1308]: https://github.com/PyThaiNLP/pythainlp/pull/1308
[#1311]: https://github.com/PyThaiNLP/pythainlp/pull/1311
[#1315]: https://github.com/PyThaiNLP/pythainlp/pull/1315
[#1316]: https://github.com/PyThaiNLP/pythainlp/pull/1316
[#1317]: https://github.com/PyThaiNLP/pythainlp/pull/1317
[#1319]: https://github.com/PyThaiNLP/pythainlp/pull/1319
[#1320]: https://github.com/PyThaiNLP/pythainlp/pull/1320
[#1323]: https://github.com/PyThaiNLP/pythainlp/pull/1323

## [5.2.0] - 2025-12-20

### Added

- Words spelling correction using Char2Vec ([#1075])
- `pythainlp.translate.word_translate` ([#1102])
- Thailand ancient currency converter ([#1113])
- Docker Compose file ([#1132])
- B-K/umt5-thai-g2p-v2-0.5k model ([#1140])
- `budoux` integration ([#1161])

### Changed

- Update Dockerfile ([#1049])

### Removed

- ConceptNet integration ([#1103])

### Fixed

- Docker build failure ([#1132])
- Connectivity of CLI commands ([#1154])

[#1049]: https://github.com/PyThaiNLP/pythainlp/pull/1049
[#1075]: https://github.com/PyThaiNLP/pythainlp/pull/1075
[#1102]: https://github.com/PyThaiNLP/pythainlp/pull/1102
[#1103]: https://github.com/PyThaiNLP/pythainlp/pull/1103
[#1113]: https://github.com/PyThaiNLP/pythainlp/pull/1113
[#1132]: https://github.com/PyThaiNLP/pythainlp/pull/1132
[#1140]: https://github.com/PyThaiNLP/pythainlp/pull/1140
[#1154]: https://github.com/PyThaiNLP/pythainlp/pull/1154
[#1161]: https://github.com/PyThaiNLP/pythainlp/pull/1161

## [5.1.2] - 2025-05-09

### Changed

- Romanize docs; keep space ([#1110])

[#1110]: https://github.com/PyThaiNLP/pythainlp/pull/1110

## [5.1.1] - 2025-03-31

### Changed

- Refactor `thai_consonants_all` to use set in `syllable.py` ([#1087])
- `ThaiTransliterator`: select 1D CPU int64 tensor device ([#1089])

[#1087]: https://github.com/PyThaiNLP/pythainlp/pull/1087
[#1089]: https://github.com/PyThaiNLP/pythainlp/pull/1089

## [5.1.0] - 2025-02-25

### Added

- Thai Discourse Treebank POS tag ([#910])
- Thai Universal Dependency Treebank POS tag ([#916])
- Thai G2P v2 grapheme-to-phoneme model ([#923])
- Support for list of strings as input to `sent_tokenize()` ([#927])
- `pythainlp.tools.safe_print` to handle `UnicodeEncodeError`
  on console ([#969])
- Thai Solar Date to Thai Lunar Date conversion ([#998])
- Thai pangram text ([#1045])

### Removed

- `clause_tokenize` ([#1024])

### Fixed

- `collate()` to consider tone mark in ordering ([#926])
- `nlpo3.load_dict()` not printing error when unsuccessful ([#979])

[#910]: https://github.com/PyThaiNLP/pythainlp/pull/910
[#916]: https://github.com/PyThaiNLP/pythainlp/pull/916
[#923]: https://github.com/PyThaiNLP/pythainlp/pull/923
[#926]: https://github.com/PyThaiNLP/pythainlp/pull/926
[#927]: https://github.com/PyThaiNLP/pythainlp/pull/927
[#969]: https://github.com/PyThaiNLP/pythainlp/pull/969
[#979]: https://github.com/PyThaiNLP/pythainlp/pull/979
[#998]: https://github.com/PyThaiNLP/pythainlp/pull/998
[#1024]: https://github.com/PyThaiNLP/pythainlp/pull/1024
[#1045]: https://github.com/PyThaiNLP/pythainlp/pull/1045

## [5.0.5] - 2024-12-14

### Changed

- Add `clause_tokenize` deprecation warnings ([#1026])

### Fixed

- `maiyamok()` expanding the wrong word ([#962])

[#962]: https://github.com/PyThaiNLP/pythainlp/pull/962
[#1026]: https://github.com/PyThaiNLP/pythainlp/pull/1026

## [5.0.4] - 2024-06-02

### Fixed

- `pythainlp.util.maiyamok` not duplicating words when more
  than one Maiyamok is used ([#917])

[#917]: https://github.com/PyThaiNLP/pythainlp/pull/917

## [5.0.3] - 2024-05-12

### Fixed

- Empty string added when using `word_tokenize` with
  `join_broken_num=True` ([#912])

[#912]: https://github.com/PyThaiNLP/pythainlp/pull/912

## [5.0.2] - 2024-04-03

### Fixed

- `crfcut`: ensure splitting of sentences using terminal
  punctuation ([#905])

[#905]: https://github.com/PyThaiNLP/pythainlp/pull/905

## [5.0.1] - 2024-02-10

### Fixed

- Delay calling `syllable_tokenize` to avoid
  `pycrfsuite` import error ([#901])

[#901]: https://github.com/PyThaiNLP/pythainlp/pull/901

## [5.0.0] - 2024-02-10

- See <https://github.com/PyThaiNLP/pythainlp/releases/tag/v5.0.0>

---

[5.3.8]: https://github.com/PyThaiNLP/pythainlp/compare/v5.3.7...v5.3.8
[5.3.7]: https://github.com/PyThaiNLP/pythainlp/compare/v5.3.6...v5.3.7
[5.3.6]: https://github.com/PyThaiNLP/pythainlp/compare/v5.3.5...v5.3.6
[5.3.5]: https://github.com/PyThaiNLP/pythainlp/compare/v5.3.4...v5.3.5
[5.3.4]: https://github.com/PyThaiNLP/pythainlp/compare/v5.3.3...v5.3.4
[5.3.3]: https://github.com/PyThaiNLP/pythainlp/compare/v5.3.2...v5.3.3
[5.3.2]: https://github.com/PyThaiNLP/pythainlp/compare/v5.3.1...v5.3.2
[5.3.1]: https://github.com/PyThaiNLP/pythainlp/compare/v5.3.0...v5.3.1
[5.3.0]: https://github.com/PyThaiNLP/pythainlp/compare/v5.2.0...v5.3.0
[5.2.0]: https://github.com/PyThaiNLP/pythainlp/compare/v5.1.2...v5.2.0
[5.1.2]: https://github.com/PyThaiNLP/pythainlp/compare/v5.1.1...v5.1.2
[5.1.1]: https://github.com/PyThaiNLP/pythainlp/compare/v5.1.0...v5.1.1
[5.1.0]: https://github.com/PyThaiNLP/pythainlp/compare/v5.0.5...v5.1.0
[5.0.5]: https://github.com/PyThaiNLP/pythainlp/compare/v5.0.4...v5.0.5
[5.0.4]: https://github.com/PyThaiNLP/pythainlp/compare/v5.0.3...v5.0.4
[5.0.3]: https://github.com/PyThaiNLP/pythainlp/compare/v5.0.2...v5.0.3
[5.0.2]: https://github.com/PyThaiNLP/pythainlp/compare/v5.0.1...v5.0.2
[5.0.1]: https://github.com/PyThaiNLP/pythainlp/compare/v5.0.0...v5.0.1
[5.0.0]: https://github.com/PyThaiNLP/pythainlp/releases/tag/v5.0.0
