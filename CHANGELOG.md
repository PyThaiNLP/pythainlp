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
- Commit history: <https://github.com/PyThaiNLP/pythainlp/compare/v5.3.0...v5.3.1>

## [5.3.1] - 2026-03-15

This release focuses on security issues related to corpus file loading.

### Security

- thai2fit: Use JSON model instead of pickle (#1325)
- Defensive corpus loading: validate fields before processing (#1327)
- w2p: Use npz model instead of pickle (#1328)

## [5.3.0] - 2026-03-10

This release focuses on stability and performance, featuring optimized memory
efficiency, better read-only environment support, and standardized error
messaging.
We’ve expanded our test suite to include Python 3.14 and broadened type hint
support for a better developer experience.

The minimum requirement is now Python 3.9.

### Added

- Tapsai et al. 2020 soundex (#1175)
- Thai profanity detection (#1183)
- Qwen3-0.6B language model (#1217)
- Thai-NNER integration with top-level entity filtering (#1221)
- `pythainlp.braille` module for Thai braille conversion (#1287)
- BLEU, ROUGE, WER, and CER metrics to `pythainlp.benchmarks` (#1295)
- Attaparse engine to dependency parser
  (`dependency_parsing`, engine="attaparse") (#1303)
- `pythainlp.is_offline_mode()` helper function;
  use `PYTHAINLP_OFFLINE=1` to disable automatic corpus downloads (#1306)
- Thai consonant cluster detection (`check_khuap_klam`) (#1308)
- `pythainlp.is_read_only_mode()` helper function;
  use `PYTHAINLP_READ_ONLY=1` to prevent all write operations (#1317)

### Changed

- Optimized for performance (#1182, #1237, #1320)
- Lazy load dictionaries to reduce memory usage (#1186)
- Migrate configurations to `pyproject.toml` (#1188, #1190, #1226, #1239)
- Update type hints; use Python 3.9 features (#1189, #1190, #1232,
  #1262, #1263, #1264, #1274, etc.)
- Make package zip-safe (#1212)
- Ensure thread-safety for tokenizers (#1213)
- Replace TNC word frequency dataset with Phupha filtered by ORST words (#1284)
- Reorganize "noauto" test suite by dependency groups
  (torch, tensorflow, onnx, cython, network) (#1290)
- `get_corpus_path()` now respects `PYTHAINLP_OFFLINE` env var
  (follows `HF_HUB_OFFLINE` convention from Hugging Face):
  raises `FileNotFoundError` if the corpus is not cached locally
  when the var is set; auto-downloads otherwise (#1306)
- Callers raise `FileNotFoundError` with download instructions when
  a corpus path cannot be resolved (#1306)
- Migrate build backend to `hatchling` (#1311)

### Deprecated

- `PYTHAINLP_DATA_DIR` env var; use `PYTHAINLP_DATA` instead
  (follows `NLTK_DATA` convention from NLTK)
  `PYTHAINLP_DATA_DIR` will be removed in a future version (#1306)
- `PYTHAINLP_READ_MODE` env var; use `PYTHAINLP_READ_ONLY` instead
  `PYTHAINLP_READ_MODE` will be removed in a future version (#1317)

### Removed

- Duplicated entries in Volubilis dictionary (#1200)
- Star imports (#1207)
- `requests` dependency (#1211)
- `pythainlp.util.is_native_thai` (deprecated since v5.0);
  use `pythainlp.morpheme.is_native_thai` instead (#1315)

### Fixed

- `royin` romanization: Consonant cluster boundary (#1172)
- `check_marttra()`: Final consonant classification (#1173)
- Base dependencies (#1185)
- `tltk` transliteration: Kho Khon alphabet issue in (#1187)
- Fix tone_detector and sound_syllable bugs (#1197)
- `normalize()`: Remove spaces before tone marks and non-base
  characters (#1222)
- Suppress Gensim duplicate-word warnings when loading word2vec
  binary files (#1316)
- `db.json`: created lazily only when a corpus is first
  downloaded (#1317)
- `newmm` tokenization: Exponential-time explosion when text has
  many ambiguous breaking points (#1319)
- `Trie`: Reduce memory usage and faster TCC boundary lookups (#1323)

### Security

- Prevent path traversal and symlink attacks in archive extraction
  (#1225)

## [5.2.0] - 2025-12-20

### Added

- `pythainlp.translate.word_translate` (#1102)
- Words spelling correction using Char2Vec (#1075)
- Thailand ancient currency converter (#1113)
- B-K/umt5-thai-g2p-v2-0.5k model (#1140)
- budoux integration (#1161)
- Docker Compose file for convenience (#1132)

### Changed

- Update Dockerfile (#1049)

### Removed

- ConceptNet integration (#1103)

### Fixed

- Connectivity of CLI commands (#1154)
- Docker build failure (#1132)

## [5.1.2] - 2025-05-09

### Changed

- Romanize docs; keep space (#1110)

## [5.1.1] - 2025-03-31

### Changed

- Refactor `thai_consonants_all` to use set in `syllable.py` (#1087)
- `ThaiTransliterator`: select 1D CPU int64 tensor device (#1089)

## [5.1.0] - 2025-02-25

### Added

- Thai Discourse Treebank POS tag (#910)
- Thai Universal Dependency Treebank POS tag (#916)
- Thai G2P v2 grapheme-to-phoneme model (#923)
- Support for list of strings as input to `sent_tokenize()` (#927)
- `pythainlp.tools.safe_print` to handle `UnicodeEncodeError`
  on console (#969)
- Thai Solar Date to Thai Lunar Date conversion (#998)
- Thai pangram text (#1045)

### Removed

- `clause_tokenize` (#1024)

### Fixed

- `collate()` to consider tone mark in ordering (#926)
- `nlpo3.load_dict()` not printing error when unsuccessful (#979)

## [5.0.5] - 2024-12-14

### Changed

- Add `clause_tokenize` deprecation warnings (#1026)

### Fixed

- `maiyamok()` expanding the wrong word (#962)

## [5.0.4] - 2024-06-02

### Fixed

- `pythainlp.util.maiyamok` not duplicating words when more
  than one Maiyamok is used (#917)

## [5.0.3] - 2024-05-12

### Fixed

- Empty string added when using `word_tokenize` with
  `join_broken_num=True` (#912)

## [5.0.2] - 2024-04-03

### Fixed

- `crfcut`: ensure splitting of sentences using terminal
  punctuation (#905)

## [5.0.1] - 2024-02-10

### Fixed

- Delay calling `syllable_tokenize` to avoid
  `pycrfsuite` import error (#901)

## [5.0.0] - 2024-02-10

- See <https://github.com/PyThaiNLP/pythainlp/releases/tag/v5.0.0>

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
