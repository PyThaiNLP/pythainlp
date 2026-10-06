---
SPDX-FileCopyrightText: 2026 PyThaiNLP Project
SPDX-FileType: DOCUMENTATION
SPDX-License-Identifier: CC0-1.0
---

# Roadmap

This file, `working-docs/ROADMAP.md`, tracks known issues and planned work
that are not yet in the [change log](../CHANGELOG.md).

## Remaining refactoring work

Phase 2 lowered complexity limits to McCabe 10 and cognitive 15.
These parts still carry `# noqa: ... # phase2-todo` or were skipped.
See [refactoring notes](refactoring-notes.md) for the procedure.

Functions in the no-auto tier (torch, ONNX) that keep the noqa:

- `pythainlp/wangchanberta/core.py`: `get_ner` (two copies)
- `pythainlp/tag/wangchanberta_onnx.py`: `get_ner`
- `pythainlp/parse/transformers_ud.py`: `__call__`
- `pythainlp/parse/ud_goeswith.py`: `__call__`
- `pythainlp/parse/attaparse_engine.py`: `__call__`
- `pythainlp/transliterate/thai2rom.py`: `forward`
- `pythainlp/transliterate/thaig2p.py`: `forward`

Files in the no-auto tier were skipped: `thai2rom`, `thaig2p`,
`wangchanberta`, and the parse engines.
They need models that CI cannot install.

Three copies of the IOB-to-markup loop remain.
They can use `pythainlp.tag._utils._iob_to_markup`:

- `pythainlp/wangchanberta/core.py` (two copies)
- `pythainlp/tag/wangchanberta_onnx.py`

## Follow-up bug fixes

Bugs found while refactoring. Refactoring changes keep the current behavior.

To pin a bug, add a test that asserts the current (wrong) behavior.
Mark it with a comment `# BUG-LEDGER: <id>`.
The id must match the entry id in this file.
Keep both directions in sync: every entry has a marker,
and every marker has an entry.

To fix a bug, use its own pull request:

1. Change the code.
2. Update the pinning test to assert the correct behavior.
3. Remove the `# BUG-LEDGER` marker and the entry in this file.
4. Add a change log entry.

Output and content bugs follow the same rule.
This file tracks them until their own PR lands.

Entry format:

- **`<id>`** `file`: `function`. Input that triggers it.
  Current behavior. Expected behavior.

### Known bugs

#### Util

- **`sound-syllable-e-a`** `pythainlp/util/syllable.py`: `sound_syllable`.
  Input "เอะ" returns "live". Expected: "dead".
- **`syllable-consonant-sets`** `pythainlp/util/syllable.py`.
  The consonant sets are inconsistent between functions.
- **`thaiword-to-time-ti`** `pythainlp/util/time.py`: `thaiword_to_time`.
  Input with "ตี" has no break after it.
- **`thai-strptime-m-y`** `pythainlp/util/date.py`: `thai_strptime`.
  Directives `%m` and `%y` are handled incorrectly.
- **`count-thai-chars-double`** `pythainlp/util/thai.py`: `count_thai_chars`.
  Some characters are counted twice.
- **`numtoword-ed-duplicate`** `pythainlp/util/numtoword.py`.
  The "เอ็ด" rule is applied in both `_num_to_thaiword_block` and
  `num_to_thaiword`. Results are correct; the code is redundant.
- **`thaiword-to-time-range`** `pythainlp/util/time.py`: `thaiword_to_time`.
  Input "บ่ายโมงครึ่งตีสองสิบเอ็ด" with `padding=False` returns "13:321".
  A minute above 59 or an hour above 23 is not checked. Expected:
  `ValueError`.

#### Tokenize

- **`sent-tokenize-crfcut-segments`** `pythainlp/tokenize/core.py`:
  `sent_tokenize`. With `crfcut`, a list input ignores `segments`.
  Pinning test: `test_word_list_input_crfcut_ignores_segments`.
- **`whitespace-trailing-append`** `pythainlp/tokenize/core.py`:
  `sent_tokenize`. With `whitespace` or `whitespace+newline`, a word list
  that ends with a separator, such as `["ก", " ", "ข", " "]`, gets an extra
  empty sentence: `[["ก"], ["ข"], []]`. Expected: `[["ก"], ["ข"]]`.
  Pinning test: `test_whitespace_engines_word_list_trailing_separator`.
- **`thaisumcut-placeholder-leak`** `pythainlp/tokenize/thaisumcut.py`.
  Placeholder text can leak into the output. Overlapping protected
  phrases break the restore step. `split_into_sentences("เขามีแต่หลังจากไป")`
  returns `["เขามีแต่<langjak>ไป"]`. Expected: `["เขามีแต่หลังจากไป"]`.
  Pinning test: `test_placeholder_leak`.
- **`sent-tokenize-strip-misaligns-words`** `pythainlp/tokenize/core.py`:
  `sent_tokenize`. A word list with `keep_whitespace=False` and an engine
  other than `crfcut`, `whitespace`, or `whitespace+newline` maps word
  offsets onto the stripped sentences, so words split, merge, or vanish:
  sentences `["ก ", "ขคง"]` for words `["ก", " ", "ขค", "ง"]` give
  `[["ก"], ["ข", "คง"]]`. Expected: whole words, `[["ก"], ["ขค", "ง"]]`.
  Pinning test: `test_word_list_input` in `tests/core/test_tokenize_core.py`.
- **`longest-front-dep-typo`** `pythainlp/tokenize/longest.py`:
  `_FRONT_DEP_CHAR`. The list contains "า " with a trailing space. With
  dictionary `["ก","ข"]`, "กา" returns `["ก","า"]`. Expected: "า" joins the
  previous token.
- **`nercut-combined-word-dropped`** `pythainlp/tokenize/nercut.py`:
  `segment`. A pending entity is lost when the next token is another "B-"
  tag in `taglist` or a tag outside it:
  `[("a","B-PERSON"),("b","B-PERSON")]` returns `["b"]`. Expected: keep "a".

#### Transliterate

- **`royin-j-overrun`** `pythainlp/transliterate/royin.py`:
  `_replace_consonants`. A consonants string shorter than the word, such
  as `_replace_consonants("กข", "ก")`, raises `IndexError`. `romanize`
  does not trigger it.
- **`wiktionary-ho-rule-unreachable`** `pythainlp/transliterate/wiktionary.py`:
  `_apply_ho_rule`. The `^ห.$` check never matches, so the re-splitting of
  "ห" plus a sonorant is dead code.

#### Khavee

- **`khavee-sara-leftover-maitaikhu`** `pythainlp/khavee/core.py`:
  `check_sara`. Input "ก็็" or "เป็นหลักเป็นฐาน" returns the bare mark "็",
  because only one ไม้ไต่คู้ is consumed. Expected: a vowel name such as
  "เอาะ".
- **`khavee-sumpus-empty-after-strip`** `pythainlp/khavee/core.py`:
  `is_sumpus`, `check_karu_lahu`. A word that is empty after stripping tone
  marks or การันต์ gets sara and marttra "". `is_sumpus("้", "์")` returns
  True and `check_karu_lahu("้")` returns "karu". Expected: False.

#### Soundex

- **`prayut-last-length`** `pythainlp/soundex/prayut_and_somchaip.py`:
  `prayut_and_somchaip`. Keeps the last `length` characters of the code
  (`[-length:]`) instead of the first. `length=0` returns the whole code.
  Example: `("kingkong", 2)` returns "52"; the first two codes are "27".

#### Corpus

- **`download-last-version`** `pythainlp/corpus/core.py`: `download`.
  With catalog versions 0.2, 0.3 (unsupported), 0.1 it installs 0.1, the
  last compatible one. Expected: the highest compatible version.
- **`version2int-single-component`** `pythainlp/corpus/core.py`:
  `_version2int`. "9" becomes 900 but "9.0.0" becomes 90000, so
  `_check_version(">=9")` is True on 5.4.0. A component with 3 or more
  digits breaks the ordering the same way. Expected: compare version tuples.

#### Benchmarks, generate, lm, augment, morpheme

- **`wordnetaug-pos-ignored`** `pythainlp/augment`: `WordNetAug`.
  The part-of-speech filter is ignored.
- **`remove-repeated-ngrams-zero`** `pythainlp/lm/text_util.py`:
  `remove_repeated_ngrams`. Slice `[-0:]` returns the whole list.
- **`remove-repeated-ngrams-tail`** `pythainlp/lm/text_util.py`:
  `remove_repeated_ngrams`. With `n` longer than the list,
  `(["a","b","c"], 5)` returns `["a","b","c","b","c"]`. Expected:
  `["a","b","c"]`.
- **`ngram-gen-tie-bias`** `pythainlp/generate/core.py`:
  `Trigram.gen_sentence` and `Bigram.gen_sentence`. With equal
  probabilities, `probs.index(random.choice(...))` always picks the first
  candidate. Expected: a random choice among ties.
- **`ngram-gen-flatten-dedup`** `pythainlp/generate/core.py`:
  `Trigram.gen_sentence`. Flattening the output drops repeated words, so
  `duplicate=True` has no effect. Expected: keep repeated words.
- **`nighit-w1-prefix`** `pythainlp/morpheme/word_formation.py`: `nighit`.
  Only the first character of `w1` is used. `nighit("สงฆํ", "คา")` returns
  "สังคา", the same as `nighit("สํ", "คา")`; the characters between the
  first one and "ํ" are dropped. Expected: keep the stem or reject it.
  Pinning test: `test_w1_prefix_dropped`.

### Security notes (not yet bugs)

- The corpus MD5 checksum comes from the same HTTPS catalog as the file.
- Tar extraction with `tarfile.data_filter` is only as safe as the CPython
  filter. Releases without the 2025 fixes (CVE-2025-4517, CVE-2025-4330,
  CVE-2025-4138) can be escaped through symlinks. Use a recent patch
  release.
- `_safe_extract_tar` without `tarfile.data_filter` assumes an empty
  destination: it does not check symlinks already on disk.
- `db.json` writes are atomic but not locked against concurrent writers;
  the last writer wins.
- Concurrent downloads of one corpus: the last swap wins. If two swaps
  race, one can fail and leave a hidden `.<folder>.<hex>.old` folder.
- `_swap_in_folder` renames the existing corpus folder aside. A folder
  that is a mount point (EBUSY) or busy on Windows cannot be re-extracted,
  and there is no retry.
- A corpus folder that is a symlink is replaced by a real folder
  (intentional).
- A crash, a failed cleanup, or a failed rollback in `_swap_in_folder` can
  leave hidden `.<name>.<hex>.part`, `.tmp`, or `.old` entries in the data
  directory. Nothing sweeps them.
- `_is_within_directory` is used only by tests.

### Other observations

- `nercut.segment` has a mutable default `taglist` and does not type-check
  `text`.
- The `longest._tokenizers` cache is keyed by `id(custom_dict)` and never
  evicted.
- `multi_cut` is exponential on lattices with many overlapping words.
