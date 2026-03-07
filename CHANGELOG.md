---
SPDX-FileCopyrightText: 2025-2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# Changelog

Notable changes between versions.

- For full release notes, see:
  <https://github.com/PyThaiNLP/pythainlp/releases>
- For detailed commit changes, see:
  <https://github.com/PyThaiNLP/pythainlp/compare/v5.2.0...dev>
  (select tags to compare)

## Version 5.2.0 -> dev

Minimum required version is now 3.9.
Support for Python 3.7 and 3.8 has been removed.
Added official support and CI testing for Python 3.14.

Some features and fixes in this version are AI-assisted.
See PR for prompt and details.

- Fix `royin` romanization #1172
- Fix final consonant classification in `check_marttra()` #1173
- Lazy load dictionaries to reduce memory usage #1186
- Fix Kho Khon alphabet issue in `tltk` transliteration #1187
- Migrate configurations to pyproject.toml #1188 #1226 #1239
- Update type hints; Use Python 3.9 features #1189 #1190 & etc.
- Remove duplicated entries in volubilis dictionary #1200
- Remove star imports #1207
- Remove `requests` dependency #1211
- Make package zip-safe #1212
- Ensure thread-safety for tokenizers #1213
- Add Thai-NNER integration with top-level entity filtering #1221
- Reorganize noauto test suite by dependency groups
  (torch, tensorflow, onnx, cython, network) #1290
- Add BLEU, ROUGE, WER, and CER metrics to pythainlp.benchmarks #1295
- Add Attaparse engine to dependency parser
  (`dependency_parsing`, engine="attaparse") #1303
- `get_corpus_path()` no longer auto-downloads missing corpus files;
  callers now raise `FileNotFoundError` with download instructions #1306
- Improved documentation; code cleanup; more tests

## Version 5.1.2 -> 5.2.0

- Add pythainlp.translate.word_translate #1102
- Update Dockerfile #1049
- Add Words Spelling Correction using Char2Vec #1075
- Add Thailand Ancient Currency Converter #1113
- Add B-K/umt5-thai-g2p-v2-0.5k #1140
- Add budoux #1161
- Remove conceptnet #1103
- fix the connectivity of cli commands #1154
- Fix Docker build failure, add docker compose file
  for convenience #1132

## Version 5.1.1 -> 5.1.2

- Update romanize docs and keep space #1110

## Version 5.1.0 -> 5.1.1

- PR Description: Refactor thai_consonants_all to
  use set in syllable.py #1087
- ThaiTransliterator: Select 1D CPU int64 tensor device #1089

## Version 5.0.5 -> 5.1.0

- Add Thai Discourse Treebank postag #910
- Add Thai Universal Dependency Treebank postag #916
- Add Thai G2P v2 Grapheme-to-Phoneme model #923
- Add support for list of strings as input
  to sent_tokenize() #927
- Add pythainlp.tools.safe_print to handle UnicodeEncodeError
  on console #969
- Fix collate() to consider tonemark in ordering #926
- Fix nlpo3.load_dict() that never print error msg when
  not success #979
- Add Thai Solar Date convert to Thai Lunar Date #998
- Add Thai pangram text #1045
- Remove clause_tokenize #1024

## Version 5.0.4 -> 5.0.5

- Add clause_tokenize warnings #1026
- Fix maiyamok() that expanding the wrong word #962

## Version 5.0.3 -> 5.0.4

- Fix: pythainlp.util.maiyamok does not duplicate words
  when more than one Maiyamok is used #917

## Version 5.0.2 -> 5.0.3

- Fix: empty string ('') added when using word_tokenize with
  join_broken_num=True #912

## Version 5.0.1 -> 5.0.2

- Fix: crfcut: Ensure splitting of sentences using terminal
  punctuation #905

## Version 5.0.0 -> 5.0.1

- Fix: delay calling syllable_tokenize to avoid
  pycrfsuite ImportError #901
