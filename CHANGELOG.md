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
  <https://github.com/PyThaiNLP/pythainlp/compare/v5.0.4...dev> (select tags to compare)

## Version 5.0.5 -> Dev

- Add Thai Discourse Treebank postag #910
- Add Thai Universal Dependency Treebank postag #916
- Add Thai G2P v2 Grapheme-to-Phoneme model #923
- Add support for list of strings as input to sent_tokenize() #927
- Add pythainlp.tools.safe_print to handle UnicodeEncodeError on console #969
- Fix collate() to consider tonemark in ordering #926

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
