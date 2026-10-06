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

### Complexity ranking

Measured on 2026-10-06. No function is over the limits (McCabe 10,
cognitive 15). The totals add up the complexity of every function in a
file, so a high total means many functions, not one hard function.
The top 20 files are ranked by McCabe total plus cognitive total.

| # | File | Lines | Functions | McCabe total | McCabe max | Cognitive total | Cognitive max |
|---|------|-------|-----------|--------------|------------|-----------------|---------------|
| 1 | `pythainlp/corpus/core.py` | 1276 | 49 | 152 | 10 | 143 | 15 |
| 2 | `pythainlp/khavee/core.py` | 1117 | 24 | 117 | 9 | 163 | 13 |
| 3 | `pythainlp/soundex/complete_soundex.py` | 708 | 20 | 77 | 7 | 104 | 14 |
| 4 | `pythainlp/util/time.py` | 395 | 17 | 70 | 8 | 87 | 12 |
| 5 | `pythainlp/tokenize/core.py` | 864 | 18 | 60 | 6 | 66 | 10 |
| 6 | `pythainlp/util/syllable.py` | 367 | 14 | 44 | 8 | 51 | 12 |
| 7 | `pythainlp/corpus/common.py` | 516 | 16 | 51 | 7 | 43 | 14 |
| 8 | `pythainlp/util/trie.py` | 228 | 10 | 39 | 9 | 50 | 15 |
| 9 | `pythainlp/benchmarks/metrics.py` | 518 | 13 | 39 | 7 | 44 | 12 |
| 10 | `pythainlp/util/thai_lunar_date.py` | 478 | 13 | 40 | 6 | 42 | 14 |
| 11 | `pythainlp/tokenize/newmm.py` | 272 | 7 | 34 | 6 | 47 | 11 |
| 12 | `pythainlp/generate/core.py` | 381 | 12 | 42 | 6 | 38 | 10 |
| 13 | `pythainlp/tag/_tag_perceptron.py` | 338 | 13 | 39 | 6 | 40 | 11 |
| 14 | `pythainlp/tokenize/multi_cut.py` | 210 | 9 | 32 | 6 | 43 | 13 |
| 15 | `pythainlp/transliterate/royin.py` | 342 | 9 | 29 | 8 | 44 | 14 |
| 16 | `pythainlp/util/wordtonum.py` | 232 | 8 | 31 | 10 | 40 | 11 |
| 17 | `pythainlp/util/thai.py` | 425 | 13 | 37 | 7 | 34 | 10 |
| 18 | `pythainlp/tokenize/longest.py` | 210 | 10 | 30 | 6 | 41 | 13 |
| 19 | `pythainlp/tokenize/thaisumcut.py` | 380 | 9 | 30 | 7 | 39 | 15 |
| 20 | `pythainlp/util/numtoword.py` | 236 | 5 | 29 | 9 | 38 | 11 |

Functions at the cognitive limit (15):
`util/trie.py:87`, `tokenize/thaisumcut.py:268`, `corpus/core.py:1140`.

Functions at the McCabe limit (10): `corpus.remove`,
`tag.named_entity.load_engine`, `tools.misspell.find_misspell_candidates`,
`util.spell_words._clean`, and `util.wordtonum.thaiword_to_num`.

Commands:

```bash
ruff check --isolated --select C901 \
    --config 'lint.mccabe.max-complexity=0' pythainlp
flake8 --isolated --select CCR001 --max-cognitive-complexity=1 pythainlp
```

### Lint tightening candidates

Ranked by value for effort. Counts are from 2026-10-06, run with the project
config on `pythainlp`, `tests`, `examples`, and `notebooks`
(`ruff check --select <rule> --config pyproject.toml ...`).
Enable a rule in `[tool.ruff.lint]` in the same PR that fixes its findings.

| # | Rule | Found | Fix | Note |
|---|------|-------|-----|------|
| 1 | `D213`, `D300`, `D2` subset (`D200`, `D205`, `D202`, `D209`, `D214`) | 0 + 42 | manual | `D213` is free now: it locks in the new docstring style. Keep `D203`, `D212` off. |
| 2 | `PLE` | 1 | auto | A zero-width space in `tests/core/test_util_time.py:281`; write it as `\u200b`. |
| 3 | `PGH003` | 12 | manual | Blanket `# type: ignore`; use `[code]`, as the style guide asks. |
| 4 | `RUF100`, `RUF102` | 84 + 8 | auto | Unused and invalid `noqa`. Set `lint.external = ["CCR"]` first, so flake8's `CCR001` is kept. |
| 5 | `UP015`, `UP031`, `UP033` | 4 + 6 + 5 | auto and manual | Redundant `open` mode, `%` formatting, `lru_cache(maxsize=None)`. |
| 6 | `RUF022` | 17 | auto | Sort `__all__`, as the style guide asks. |
| 7 | `UP037` | 140 | auto | Remove quotes from annotations. Needs `from __future__ import annotations` in each file. |
| 8 | `D415`, `D400`, `D401`, `D413` | 76 + 76 + 4 + 2 | manual | Summary ends with a period, in the imperative mood. The first two flag the same lines. |
| 9 | `EXE001`, `ICN001`, `INP001`, `SLOT000`, `PYI034`, `A002`, `FA100` | 13 | manual | One-off fixes, a few lines each. |
| 10 | `RUF012` | 17 | manual | Mutable class attribute without `ClassVar`. Can hide shared-state bugs. |
| 11 | `FLY002`, `RUF010`, `RUF015` | 22 | manual | Small readability fixes. |
| 12 | `PLW2901` | 15 | manual | A loop variable is reassigned in the loop body. |
| 13 | `BLE001` | 13 | manual | Blind `except`. Narrow it or add `# noqa: BLE001` with a reason. Related to PR 1542. |
| 14 | `UP006`, `UP035` | 27 + 19 | manual | `typing.List` and similar. Safe with `from __future__ import annotations`. |
| 15 | `RUF005` | 22 | manual | List concatenation; use unpacking. |
| 16 | `PERF401`, `PERF402`, `PERF403` | 16 | manual | Loop to comprehension. Readability can get worse. |
| 17 | `W505` (max 79) | 65 | manual | Doctest output and comment lines cannot always wrap. Needs `# noqa`. |
| 18 | `TID252` | 27 | manual | Relative imports. The package uses them on purpose. Decide first. |
| 19 | `T201`, `ERA001` | 75 + 132 | manual | `print` in the CLI and examples is intended. Many `ERA001` hits are false positives. |
| 20 | `DTZ`, `PLW0603`, `PLR2004`, `PLR0913` | 17 + 49 + 86 + 22 | manual | Naive datetimes, `global` for lazy loading, magic numbers, and many arguments are intended in this code. Skip. |

Do not enable `RUF001` and `RUF002` (256 findings). They flag Thai and
look-alike characters on purpose. Skip `EM`, `TRY003`, and `N` rules:
they are style choices, and `N` renames would break the public API.

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
- **`wunsen-stale-model`** `pythainlp/transliterate/wunsen.py`:
  `WunsenTransliterate.transliterate`. `_set_options` stores the new options
  before `ThapSap(...)` is created. If `ThapSap` raises, the old model stays
  in `thap_value`, and a repeated call with the same options skips the
  re-creation and silently uses the old model. Expected: keep the options and
  the model consistent. Pinning test: `test_failed_creation_keeps_old_model`.

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
  A bare "ํ" is also accepted: `nighit("ํ", "คา")` returns "ํังคา".
  Expected: require a consonant before "ํ".
  Pinning test: `test_w1_prefix_dropped`.
- **`nighit-message-format`** `pythainlp/morpheme/word_formation.py`:
  `nighit`. The `NotImplementedError` message for an unsupported `w2`
  consonant has a newline and indentation inside. Expected: a one-line
  message like the one for `w1`.
  Pinning tests: `ADVERSARIAL` and `test_unsupported_consonants`.

### Docstring and doctest issues

Found while standardizing the docstrings. The docstring or doctest and
the code disagree. The code was not changed. No test pins them.

#### Wrong or non-runnable doctests

- `phayathaibert.NamedEntityTagger.get_ner`: the doctest calls `ner.tag(...)`.
  No `ner` object and no `tag` method exist.
- `phayathaibert.ThaiTextAugmenter.augment` and
  `augment.lm.phayathaibert`: the doctest passes `num_args=5`. The
  parameter is `num_augs`.
- `phayathaibert.ThaiTextProcessor`: the doctests of `replace_url`,
  `rm_brackets`, `rm_useless_spaces`, `replace_spaces`,
  `replace_rep_after`, `replace_wrep_post`, `remove_space`, and
  `replace_newlines` call bare names. They are methods. Some outputs are
  unquoted, and the `replace_spaces` doctest ignores the default
  `space_token` (`<_>`).
- `ulmfit.replace_wrep_post`: the doctest imports `replace_wrep_post_nonum`
  but calls `replace_wrep_post`.
- `ulmfit.process_thai`: the doctest has multi-line `>>>` calls without
  `...` prompts. A `:Note:` names `pythainlp.util.normalize`, but the rules
  use `reorder_vowels`.
- `word_vector.most_similar_cosmul` and `doesnt_match`: some outputs
  probably do not match a real run.
- `summarize.keybert`: the doctest calls `kb.extract_keyword(...)`. The
  method is `extract_keywords`.
- `util.keywords.rank`: the "Exclude stopwords" example calls `rank(words)`
  without `exclude_stopwords=True`, and the output is not what a plain call
  returns.
- `util.date.thaiword_to_date`: the example has no `>>>`, so it is not a
  doctest.
- `transliterate.pali.pronunciate_pali("สฺวากฺขา")`: the doctest expects
  "สวากขาโต" and gets "สวากขา".
- `transliterate.romanize("ก็อปปี้", engine="lookup")`: the doctest expects
  "copy". It fails when the lookup corpus is not present.

#### Docstring does not match the code

- `util.remove_trailing_repeat_consonants`: documents `dictionary`; the
  parameter is `custom_dict`. The private helpers
  `_remove_repeat_trailing_consonants_from_segment`,
  `_update_consonant_repeaters`, and
  `_find_longest_consonant_repeaters_match` have the same kind of wrong
  parameter names (`consonant`, `dictionary`, `segment`).
- `util.keywords.find_keyword`: the parameter `min_len` means a minimum
  frequency.
- `transliterate.transliterate`: the `:return:` says "phonetic alphabet",
  but the *icu* and *iso_11940* engines return Latin transliteration.
- `generate.thai2fit.gen_sentence`: the docstring lists `duplicate`, which
  is not a parameter.
- `benchmarks.word_tokenization.preprocessing`: the docstring says `text`;
  the parameter is `txt`.
- `translate.tokenization_small100.set_lang_special_tokens`: the docstring
  says there is no prefix; the code sets `prefix_tokens=[cur_lang_id]`.
- `tokenize.core._sent_tokenize_words` (`crfcut`) and
  `_split_at_separators`: the behavior in their code comments is not in
  the docstrings.
- `transliterate.transliterate`: the options list `icu` as a phonetic
  engine. It returns Latin script.
- `spell.get_words_spell_suggestion`: the docstring parameter is
  `list_word`; the code parameter is `list_words`.
- `tag.NNER`: the class docstring lists `corpus`; `__init__` has only
  `engine`. `load_engine` ignores its `engine` argument.
- `tag.pos_tag`: the docstring lists the *wangchanberta* engine, but the code
  raises `ValueError` for it. `pos_tag_sents` lists corpus *tnc*, which is
  not in the supported list. `pos_tag_transformers` names *phayathaibert*;
  the engine key is `"phayathai"`, and its `sentence` is a string.
- `tag.thainer.ThaiNameTagger`: an unknown `version` does not raise. The CRF
  model is left unopened. `tag.tltk.get_ner` and `ThaiNameTagger.get_ner`
  ignore `pos` when `tag=True`.
- `cli.data.App.path`: the docstring says "print the path of a local
  dataset"; the code prints the PyThaiNLP data directory.
- `wsd.get_score` returns `1 - cos_sim`, a distance, not a similarity.
- `spell.wanchanberta_thai_grammarly.evaluate_one_text`: the `model`
  parameter is unused; the function calls the module-level `tagging_model`.
- `spell.phunspell.correct` and `spell.symspellpy.correct` raise
  `IndexError` when there is no suggestion.
- `augment.lm.phayathaibert.ThaiTextAugmenter.generate`: with `sample=True`
  the index is always 0 to 4 and `word_rank` is ignored.
- `augment.wordnet.WordNetAug.find_synonyms` iterates all synsets of the
  word and ignores the POS-filtered `list_synsets`.
- `parse.spacy_thai_engine.Parse.__init__`: `model` is ignored; the code
  always calls `spacy_thai.load()`. `parse.dependency_parsing` lists it.
- `tag.wangchanberta_onnx.WngchanBerta_ONNX`: the class name has a typo.
- `util.thai_lunar_date`: `athikamas`, `athikavar`, `deviation`, and
  `last_day_in_year` do not state the era of `year` (the code uses
  `year - 78`).
- Missing `:raises:` for `TypeError` in `thai_digit_to_arabic_digit` and
  similar functions.
- `phayathaibert.core.replace_newlines` and some other docstrings with `\n`
  in a non-raw string (pydocstyle D301); making them raw strings changes
  the doctest source.

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
