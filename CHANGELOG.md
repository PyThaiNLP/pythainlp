---
SPDX-FileCopyrightText: 2025 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# Changelog

Notable changes between versions.

- For full release notes, see:
  <https://github.com/PyThaiNLP/pythainlp/releases>
- For detailed commit changes, see:
  <https://github.com/PyThaiNLP/pythainlp/compare/v5.1.2...dev> (select tags to compare)

## Version 5.1.2 -> Dev

[WIP]

## Version 5.1.1 -> 5.1.2

- Update romanize docs and keep space #1110

## Version 5.1.0 -> 5.1.1

- PR Description: Refactor thai_consonants_all to Use set in syllable.py #1087
- ThaiTransliterator: Select 1D CPU int64 tensor device #1089

## Version 5.0.5 -> 5.1.0

- Add Thai Discourse Treebank postag #910
- Add Thai Universal Dependency Treebank postag #916
- Add Thai G2P v2 Grapheme-to-Phoneme model #923
- Add support for list of strings as input to sent_tokenize() #927
- Add pythainlp.tools.safe_print to handle UnicodeEncodeError on console #969
- Fix collate() to consider tonemark in ordering #926
- Fix nlpo3.load_dict() that never print error msg when not success #979
- Add Thai Solar Date convert to Thai Lunar Date #998
- Add Thai pangram text #1045
- Remove clause_tokenize #1024

## Version 5.0.4 -> 5.0.5

- Add clause_tokenize warnings #1026
- Fix maiyamok() that expanding the wrong word #962

## Version 5.0.3 -> 5.0.4

- Fix: pythainlp.util.maiyamok does not duplicate words when more than one
  Maiyamok is used #917

## Version 5.0.2 -> 5.0.3

- Fix: empty string ('') added when using word_tokenize with
  join_broken_num=True #912

## Version 5.0.1 -> 5.0.2

- Fix: crfcut: Ensure splitting of sentences using terminal punctuation #905

## Version 5.0.0 -> 5.0.1

- Fix: delay calling syllable_tokenize to avoid pycrfsuite ImportError #901
