.. currentmodule:: pythainlp.braille

pythainlp.braille
=================
The :mod:`pythainlp.braille` module provides Thai braille conversion functionality. It enables the conversion of Thai text into braille representation using Unicode braille characters, following international braille standards.

Modules
-------

thai_word_braille
~~~~~~~~~~~~~~~~~
.. autofunction:: thai_word_braille

The `thai_word_braille` function converts a single Thai word into its braille representation. It handles Thai consonants, vowels, tone marks, numbers, and punctuation marks, transforming them into Unicode braille characters according to Thai braille standards.

thai_text_braille
~~~~~~~~~~~~~~~~~
.. autofunction:: thai_text_braille

The `thai_text_braille` function converts Thai text into braille representation by tokenizing the text into words and converting each word separately. It returns a list of braille strings corresponding to each token in the input text.

Braille Class
~~~~~~~~~~~~~
.. autoclass:: pythainlp.braille.core.Braille
   :members:

   The `Braille` class handles the conversion of braille dot patterns to Unicode braille characters. It supports both reading braille (tobraille method) and printing braille with mirrored patterns (printbraille method) according to international braille standards.

Usage Examples
--------------

Converting Thai words to braille:

.. code-block:: python

    from pythainlp.braille import thai_word_braille

    # Convert a simple Thai word
    thai_word_braille("กก")
    # Output: '⠛⠛'

    # Convert a word with vowels
    thai_word_braille("น้ำ")
    # Output: '⠝⠲⠵'

    # Convert a greeting
    thai_word_braille("สวัสดี")
    # Output: '⠎⠺⠜⠎⠙⠆'

Converting Thai text to braille:

.. code-block:: python

    from pythainlp.braille import thai_text_braille

    # Convert a sentence
    thai_text_braille("สวัสดี ครับ")
    # Output: ['⠎⠺⠜⠎⠙⠆', ' ', '⠥⠗⠜⠧']

Features
--------

- **Complete Thai character support**: Handles all Thai consonants, vowels, tone marks, and special characters
- **Number conversion**: Automatically adds number prefixes for digit sequences
- **Complex vowel patterns**: Supports Thai vowel combinations and patterns through regex-based substitution
- **Unicode braille output**: Generates standard Unicode braille characters (U+2800 to U+28FF)
- **Edge case handling**: Properly handles empty strings and unmapped characters
- **International standards**: Follows international braille dot numbering (dots 1-8)

The `pythainlp.braille` module provides comprehensive Thai braille conversion capabilities, making Thai text accessible in braille format for various applications including accessibility tools, educational materials, and text processing pipelines.
