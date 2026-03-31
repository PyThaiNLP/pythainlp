# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Translation."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from pythainlp.translate.en_th import EnThTranslator, ThEnTranslator
    from pythainlp.translate.small100 import Small100Translator
    from pythainlp.translate.th_fr import ThFrTranslator
    from pythainlp.translate.zh_th import ThZhTranslator, ZhThTranslator


def _prepare_text_with_exclusions(
    text: str, exclude_words: Optional[list[str]]
) -> tuple[str, dict[str, str]]:
    """Replace excluded words with placeholders.

    :param str text: input text
    :param list[str] exclude_words: words to exclude from translation
    :return: tuple of (modified text, placeholder mapping)
    :rtype: tuple[str, dict[str, str]]

    Note: For text that contains spaces (for example, English sentences),
    this function attempts to match whole tokens delimited by whitespace
    and common punctuation characters. If the text contains no spaces at
    all (as in many sentences in languages without explicit word
    boundaries, such as Thai), it will match the exact exclude string
    anywhere it appears using simple substring replacement.
    """
    if not exclude_words:
        return text, {}

    placeholder_map = {}
    modified_text = text

    # Remove duplicates while preserving order
    seen = set()
    unique_words = []
    for word in exclude_words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)

    # Sort by length (longest first) to handle overlapping words correctly
    # For example, if we have ["cat", "category"], we want to replace
    # "category" first
    sorted_words = sorted(unique_words, key=len, reverse=True)

    for i, word in enumerate(sorted_words):
        # Use a placeholder that is very unlikely to appear in natural text
        # and includes special markers to avoid conflicts
        placeholder = f"<<<PYTHAINLP_EXCLUDE_{i}>>>"
        placeholder_map[placeholder] = word

        # Escape the word to handle special regex characters
        escaped_word = re.escape(word)

        # Try token boundary matching for space-separated languages.
        # A token boundary is:
        # - the start or end of the string, or
        # - a delimiter character such as whitespace or common punctuation.
        # This allows matching words like "cat" in "I love cat.".
        delimiter_chars = r"\s" + re.escape(
            ".,!?;:'\"()[]{}<>/\\|`~@#$%^&*-+=''、，。！？；：（）【】《》"
        )
        pattern = (
            rf"(?:(?<=^)|(?<=[{delimiter_chars}]))"
            f"{escaped_word}"
            rf"(?:(?=$)|(?=[{delimiter_chars}]))"
        )

        # Check if there's a match with token boundaries
        if re.search(pattern, modified_text):
            # Use token boundary matching for space-separated text
            modified_text = re.sub(pattern, placeholder, modified_text)
        elif " " not in modified_text:
            # For languages without spaces (like Thai), use simple replacement.
            # Only do this if the text does not contain spaces, indicating
            # it is likely a non-space-separated language.
            modified_text = modified_text.replace(word, placeholder)

    return modified_text, placeholder_map


def _restore_excluded_words(
    translated_text: str, placeholder_map: dict[str, str]
) -> str:
    """Restore excluded words from placeholders.

    :param str translated_text: translated text with placeholders
    :param dict[str, str] placeholder_map: mapping of placeholders to
                                           original words
    :return: text with original words restored
    :rtype: str
    """
    if not placeholder_map:
        return translated_text

    result = translated_text
    # Sort by placeholder to ensure consistent replacement order
    for placeholder in sorted(placeholder_map.keys()):
        original_word = placeholder_map[placeholder]
        # Direct replacement since placeholders are very specific
        result = result.replace(placeholder, original_word)

    return result


class Translate:
    """Machine Translation"""

    def __init__(
        self,
        src_lang: str,
        target_lang: str,
        engine: str = "default",
        use_gpu: bool = False,
    ) -> None:
        """:param str src_lang: source language
        :param str target_lang: target language
        :param str engine: machine translation engine
        :param bool use_gpu: load model using GPU (Default is False)

        **Options for engine**
            * *default* - The default engine for each language.
            * *small100* - A multilingual machine translation model (covering 100 languages)

        **Options for source & target language**
            * *th* - *en* - Thai to English
            * *en* - *th* - English to Thai
            * *th* - *zh* - Thai to Chinese
            * *zh* - *th* - Chinese to Thai
            * *th* - *fr* - Thai to French
            * *th* - *xx* - Thai to xx (xx is language code). It uses small100 model.
            * *xx* - *th* - xx to Thai (xx is language code). It uses small100 model.

        :Example:

        Translate text from Thai to English:

            >>> from pythainlp.translate import Translate  # doctest: +SKIP

            >>> th2en = Translate("th", "en")  # doctest: +SKIP

            >>> th2en.translate("ฉันรักแมว")  # doctest: +SKIP
            I love cat.

        Translate text with excluded words:

            >>> th2en.translate("ฉันรักแมว", exclude_words=["แมว"])  # doctest: +SKIP
            I love แมว.
        """
        self.model: Union[
            Small100Translator,
            ThEnTranslator,
            EnThTranslator,
            ThZhTranslator,
            ZhThTranslator,
            ThFrTranslator,
        ]
        self.engine: str = engine
        self.src_lang: str = src_lang
        self.use_gpu: bool = use_gpu
        self.target_lang: str = target_lang
        self.load_model()

    def load_model(self) -> None:
        src_lang = self.src_lang
        target_lang = self.target_lang
        use_gpu = self.use_gpu
        if self.engine == "small100":
            from .small100 import Small100Translator

            self.model = Small100Translator(use_gpu)
        elif src_lang == "th" and target_lang == "en":
            from pythainlp.translate.en_th import ThEnTranslator

            self.model = ThEnTranslator(use_gpu)
        elif src_lang == "en" and target_lang == "th":
            from pythainlp.translate.en_th import EnThTranslator

            self.model = EnThTranslator(use_gpu)
        elif src_lang == "th" and target_lang == "zh":
            from pythainlp.translate.zh_th import ThZhTranslator

            self.model = ThZhTranslator(use_gpu)
        elif src_lang == "zh" and target_lang == "th":
            from pythainlp.translate.zh_th import ZhThTranslator

            self.model = ZhThTranslator(use_gpu)
        elif src_lang == "th" and target_lang == "fr":
            from pythainlp.translate.th_fr import ThFrTranslator

            self.model = ThFrTranslator(use_gpu)
        else:
            raise ValueError("Not support language!")

    def translate(
        self, text: str, exclude_words: Optional[list[str]] = None
    ) -> str:
        """Translate text

        :param str text: input text in source language
        :param list[str] exclude_words: words to exclude from translation
                                        (optional)
        :return: translated text in target language
        :rtype: str
        """
        if self.engine == "small100":
            return self.model.translate(  # type: ignore[call-arg]
                text, tgt_lang=self.target_lang, exclude_words=exclude_words
            )
        return self.model.translate(text, exclude_words=exclude_words)


def word_translate(
    word: str, src: str, target: str, engine: str = "word2word"
) -> Optional[list[str]]:
    """Translate word from source language to target language.

    :param str word: text
    :param str src: src language
    :param str target: target language
    :param str engine: Word translate engine (the default engine is word2word)
    :return: list of translated words or None
    :rtype: list[str] or None

    :Example:

    Translate word from Thai to English:

        >>> from pythainlp.translate import word_translate  # doctest: +SKIP

        >>> print(word_translate("แมว", "th", "en"))  # doctest: +SKIP
        ['cat', 'cats', 'kitty', 'kitten', 'Cat']

    Translate word from English to Thai:

        >>> from pythainlp.translate import word_translate  # doctest: +SKIP

        >>> print(word_translate("cat", "en", "th"))  # doctest: +SKIP
        ['แมว', 'แมวป่า', 'ข่วน', 'เลี้ยง', 'อาหาร']

    """
    if engine == "word2word":
        from .word2word_translate import translate

        return translate(word=word, src=src, target=target)
    else:
        raise NotImplementedError(
            f"pythainlp.translate.word_translate isn't support {engine}."
        )
