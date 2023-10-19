.. currentmodule:: pythainlp.transliterate

pythainlp.transliterate
=======================
The :mod:`pythainlp.transliterate` module is dedicated to the transliteration of Thai text into romanized form, effectively spelling it out with the English alphabet. This functionality is invaluable for making Thai text more accessible to non-Thai speakers and for various language processing tasks.

Modules
-------

.. autofunction:: romanize
    :noindex:

    The `romanize` function allows you to transliterate Thai text, converting it into a phonetic representation using the English alphabet. It's a fundamental tool for rendering Thai words and phrases in a more familiar format.

.. autofunction:: transliterate
    :noindex:

    The `transliterate` function serves as a versatile transliteration tool, offering a range of transliteration engines to choose from. It provides flexibility and customization for your transliteration needs.

.. autofunction:: pronunciate
    :noindex:

    This function provides assistance in generating phonetic representations of Thai words, which is particularly useful for language learning and pronunciation practice.

.. autofunction:: puan
    :noindex:

    The `puan` function offers a unique transliteration feature known as "Puan." It provides a specialized transliteration method for Thai text and is an additional option for rendering Thai text into English characters.

.. autoclass:: pythainlp.transliterate.wunsen.WunsenTransliterate
   :members:
   
   The `WunsenTransliterate` class represents a transliteration engine known as "Wunsen." It offers specific transliteration methods for rendering Thai text into a phonetic English format.

Transliteration Engines
-----------------------

**thai2rom**
  
.. automodule:: pythainlp.transliterate.thai2rom.romanize
    :members:
    
    The `thai2rom` engine specializes in transliterating Thai text into romanized form. It's particularly useful for rendering Thai words accurately in an English phonetic format.

**royin**
  
.. automodule:: pythainlp.transliterate.royin.romanize
    :members:
    
    The `royin` engine focuses on transliterating Thai text into English characters. It provides an alternative approach to transliteration, ensuring accurate representation of Thai words.

**Transliterate Engines**

This section includes multiple transliteration engines designed to suit various use cases. They offer unique methods for transliterating Thai text into romanized form:

- **icu**: Utilizes the ICU transliteration system for phonetic conversion.
- **ipa**: Provides International Phonetic Alphabet (IPA) representation of Thai text.
- **thaig2p**: Transliterates Thai text into the Grapheme-to-Phoneme (G2P) representation.
- **tltk**: Utilizes the TLTK transliteration system for a specific approach to transliteration.
- **iso_11940**: Focuses on the ISO 11940 transliteration standard.

References
----------

.. [#rtgs_transcription] Nitaya Kanchanawan. (2006). `Romanization, Transliteration, and Transcription for the Globalization of the Thai Language. <http://www.royin.go.th/wp-content/uploads/royin-ebook/276/FileUpload/758_6484.pdf>`_
        The Journal of the Royal Institute of Thailand.

The `pythainlp.transliterate` module offers a comprehensive set of tools and engines for transliterating Thai text into Romanized form. Whether you need a simple transliteration, specific engines for accurate representation, or phonetic rendering, this module provides a wide range of options. Additionally, the module references a publication that highlights the significance of Romanization, Transliteration, and Transcription in making the Thai language accessible to a global audience.
