.. currentmodule:: pythainlp.util

pythainlp.util
==============
The :mod:`pythainlp.util` module serves as a treasure trove of utility functions designed to aid text conversion, formatting, and various language processing tasks in the context of Thai language.

Modules
-------

.. autofunction:: abbreviation_to_full_text
    :noindex:

    The `abbreviation_to_full_text` function is a text processing tool for converting common Thai abbreviations into their full, expanded forms. It's invaluable for improving text readability and clarity.

.. autofunction:: arabic_digit_to_thai_digit
    :noindex:

    The `arabic_digit_to_thai_digit` function allows you to transform Arabic numerals into their Thai numeral equivalents. This utility is especially useful when working with Thai numbers in text data.

.. autofunction:: bahttext
    :noindex:

    The `bahttext` function specializes in converting numerical values into Thai Baht text, an essential feature for rendering financial data or monetary amounts in a user-friendly Thai format.

.. autofunction:: convert_years
    :noindex:

    The `convert_years` function is designed to facilitate the conversion of Western calendar years into Thai Buddhist Era (BE) years. This is significant for presenting dates and years in a Thai context.

.. autofunction:: collate
    :noindex:

    The `collate` function is a versatile tool for sorting Thai text in a locale-specific manner. It ensures that text data is sorted correctly, taking into account the Thai language's unique characteristics.

.. autofunction:: count_thai_chars
    :noindex:

    The `count_thai_chars` function is a character counting tool specifically tailored for Thai text. It helps in quantifying Thai characters, which can be useful for various text processing tasks.

.. autofunction:: countthai
    :noindex:

    The `countthai` function is a text processing utility for counting the occurrences of Thai characters in text data. This is useful for understanding the prevalence of Thai language content.

.. autofunction:: dict_trie
    :noindex:

    The `dict_trie` function implements a Trie data structure for efficient dictionary operations. It's a valuable resource for dictionary management and fast word lookup.

.. autofunction:: digit_to_text
    :noindex:

    The `digit_to_text` function is a numeral conversion tool that translates Arabic numerals into their Thai textual representations. This is vital for rendering numbers in Thai text naturally.

.. autofunction:: display_thai_char
    :noindex:

    The `display_thai_char` function is designed to present Thai characters with diacritics and tonal marks accurately. This is essential for displaying Thai text with correct pronunciation cues.

.. autofunction:: emoji_to_thai
    :noindex:

    The `emoji_to_thai` function focuses on converting emojis into their Thai language equivalents. This is a unique feature for enhancing text communication with Thai-language emojis.

.. autofunction:: eng_to_thai
    :noindex:

    The `eng_to_thai` function serves as a text conversion tool for translating English text into its Thai transliterated form. It is beneficial for rendering English words and phrases in a Thai context.

.. autofunction:: find_keyword
    :noindex:

    The `find_keyword` function is a powerful utility for identifying keywords and key phrases in text data. It is a fundamental component for text analysis and information extraction tasks.

.. autofunction:: ipa_to_rtgs
    :noindex:

    The `ipa_to_rtgs` function focuses on converting International Phonetic Alphabet (IPA) transcriptions into Royal Thai General System of Transcription (RTGS) format. This is valuable for phonetic analysis and pronunciation guides.

.. autofunction:: is_native_thai
    :noindex:

    The `is_native_thai` function is a language detection tool that identifies whether text is predominantly in the Thai language or not. It aids in language identification and text categorization tasks.

.. autofunction:: isthai
    :noindex:

    The `isthai` function is a straightforward language detection utility that determines if text contains Thai language content. This function is essential for language-specific text processing.

.. autofunction:: isthaichar
    :noindex:

    The `isthaichar` function is designed to check if a character belongs to the Thai script. It helps in character-level language identification and text processing.

.. autofunction:: maiyamok
    :noindex:

    The `maiyamok` function is a text processing tool that assists in identifying and processing Thai character characters with a 'mai yamok' tone mark.

.. autofunction:: nectec_to_ipa
    :noindex:

    The `nectec_to_ipa` function focuses on converting text from the NECTEC phonetic transcription system to the International Phonetic Alphabet (IPA). This conversion is vital for linguistic analysis and phonetic representation.

.. autofunction:: normalize
    :noindex:

    The `normalize` function is a text processing utility that standardizes text by removing diacritics, tonal marks, and other modifications. It is valuable for text normalization and linguistic analysis.

.. autofunction:: now_reign_year
    :noindex:

    The `now_reign_year` function computes the current Thai Buddhist Era (BE) year and provides it in a human-readable format. This function is essential for displaying the current year in a Thai context.

.. autofunction:: num_to_thaiword
    :noindex:

    The `num_to_thaiword` function is a numeral conversion tool for translating Arabic numerals into Thai word form. It is crucial for rendering numbers in a natural Thai textual format.

.. autofunction:: rank
    :noindex:

    The `rank` function is designed for ranking and ordering a list of items. It is a general-purpose utility for ranking items based on various criteria.

.. autofunction:: reign_year_to_ad
    :noindex:

    The `reign_year_to_ad` function facilitates the conversion of Thai Buddhist Era (BE) years into Western calendar years. This is useful for displaying historical dates in a globally recognized format.

.. autofunction:: remove_dangling
    :noindex:

    The `remove_dangling` function is a text processing tool for removing dangling characters or diacritics from text. It is useful for text cleaning and normalization.

.. autofunction:: remove_dup_spaces
    :noindex:

    The `remove_dup_spaces` function focuses on removing duplicate space characters from text data, making it more consistent and readable.

.. autofunction:: remove_repeat_vowels
    :noindex:

    The `remove_repeat_vowels` function is designed to eliminate repeated vowel characters in text, improving text readability and consistency.

.. autofunction:: remove_tone_ipa
    :noindex:

    The `remove_tone_ipa` function serves as a phonetic conversion tool for removing tone marks from IPA transcriptions. This is crucial for phonetic analysis and linguistic research.

.. autofunction:: remove_tonemark
    :noindex:

    The `remove_tonemark` function is a utility for removing tonal marks and diacritics from text data, making it suitable for various text processing tasks.

.. autofunction:: remove_zw
    :noindex:

    The `remove_zw` function is designed to remove zero-width characters from text data, ensuring that text is free from invisible or unwanted characters.

.. autofunction:: reorder_vowels
    :noindex:

    The `reorder_vowels` function is a text processing utility for reordering vowel characters in Thai text. It is essential for phonetic analysis and pronunciation guides.

.. autofunction:: rhyme
    :noindex:


    The `rhyme` function is a utility for find rhyme of Thai word.

.. autofunction:: sound_syllable
    :noindex:

    The `sound_syllable` function specializes in identifying and processing Thai characters that represent sound syllables. This is valuable for phonetic and linguistic analysis.

.. autofunction:: syllable_length
    :noindex:

    The `syllable_length` function is a text analysis tool for calculating the length of syllables in Thai text. It is significant for linguistic analysis and language research.

.. autofunction:: syllable_open_close_detector
    :noindex:

    The `syllable_open_close_detector` function is designed to detect syllable open and close statuses in Thai text. This information is vital for phonetic analysis and linguistic research.

.. autofunction:: text_to_arabic_digit
    :noindex:

    The `text_to_arabic_digit` function is a numeral conversion tool that translates Thai text numerals into Arabic numeral form. It is useful for numerical data extraction and processing.

.. autofunction:: text_to_num
    :noindex:

    The `text_to_num` function focuses on extracting numerical values from text data. This is essential for converting textual numbers into numerical form for computation.

.. autofunction:: text_to_thai_digit
    :noindex:

    The `text_to_thai_digit` function serves as a numeral conversion tool for translating Arabic numerals into Thai numeral form. This is important for rendering numbers in Thai text naturally.

.. autofunction:: thai_digit_to_arabic_digit
    :noindex:

    The `thai_digit_to_arabic_digit` function allows you to transform Thai numeral text into Arabic numeral format. This is valuable for numerical data extraction and computation tasks.

.. autofunction:: thai_strftime
    :noindex:

    The `thai_strftime` function is a date formatting tool tailored for Thai culture. It is essential for displaying dates and times in a format that adheres to Thai conventions.

.. autofunction:: thai_strptime
    :noindex:

    The `thai_strptime` function focuses on parsing dates and times in a Thai-specific format, making it easier to work with date and time data in a Thai context.

.. autofunction:: thai_to_eng
    :noindex:

    The `thai_to_eng` function is a text conversion tool for translating Thai text into its English transliterated form. This is beneficial for rendering Thai words and phrases in an English context.

.. autofunction:: to_idna
    :noindex:

    The `to_idna` function is a text conversion tool for translating Thai text into its  International Domain Name (IDN) for Thai domain name.

.. autofunction:: thai_word_tone_detector
    :noindex:

    The `thai_word_tone_detector` function specializes in detecting and processing tonal marks in Thai words. It is essential for phonetic analysis and pronunciation guides.

.. autofunction:: thaiword_to_date
    :noindex:

    The `thaiword_to_date` function facilitates the conversion of Thai word representations of dates into standardized date formats. This is important for date data extraction and processing.

.. autofunction:: thaiword_to_num
    :noindex:

    The `thaiword_to_num` function is a numeral conversion tool for translating Thai word numerals into numerical form. This is essential for numerical data extraction and computation.

.. autofunction:: thaiword_to_time
    :noindex:

    The `thaiword_to_time` function is designed for converting Thai word representations of time into standardized time formats. It is crucial for time data extraction and processing.

.. autofunction:: time_to_thaiword
    :noindex:

    The `time_to_thaiword` function focuses on converting time values into Thai word representations. This is valuable for rendering time in a natural Thai textual format.

.. autofunction:: tis620_to_utf8
    :noindex:

    The `tis620_to_utf8` function serves as a character encoding conversion tool for converting TIS-620 encoded text into UTF-8 format. This is significant for character encoding compatibility.

.. autofunction:: tone_detector
    :noindex:

    The `tone_detector` function is a text processing tool for detecting tone marks and diacritics in Thai text. It is essential for phonetic analysis and pronunciation guides.

.. autofunction:: words_to_num
    :noindex:

    The `words_to_num` function is a numeral conversion utility that translates Thai word numerals into numerical form. It is important for numerical data extraction and computation.

.. autofunction:: pythainlp.util.spell_words.spell_syllable
    :noindex:

    The `pythainlp.util.spell_words.spell_syllable` function focuses on spelling syllables in Thai text, an important feature for phonetic analysis and linguistic research.

.. autofunction:: pythainlp.util.spell_words.spell_word
    :noindex:

    The `pythainlp.util.spell_words.spell_word` function is designed for spelling individual words in Thai text, facilitating phonetic analysis and pronunciation guides.

.. autoclass:: Trie
    :members:

    The `Trie` class is a data structure for efficient dictionary operations. It's a valuable resource for managing and searching word lists and dictionaries in a structured and efficient manner.

.. autofunction:: pythainlp.util.morse.morse_encode
    :noindex:

    The `pythainlp.util.morse.morse_encode` function is convert text to Morse code.

.. autofunction:: pythainlp.util.morse.morse_decode
    :noindex:

    The `pythainlp.util.morse.morse_decode` function is convert Morse code to text.
