.. currentmodule:: pythainlp.soundex

pythainlp.soundex
=================
The :class:`pythainlp.soundex` module provides soundex algorithms for the Thai language. Soundex is a phonetic algorithm used to encode words or names into a standardized representation based on their pronunciation, making it useful for tasks like name matching and search.

Modules
-------

soundex
~~~~~~~
.. autofunction:: soundex

The `soundex` function is a basic Soundex algorithm for the Thai language. It encodes a Thai word into a Soundex code, allowing for approximate matching of words with similar pronunciation.

lk82
~~~~
.. autofunction:: lk82

The `lk82` module implements the Thai Soundex algorithm proposed by Vichit Lorchirachoonkul in 1982. This module is suitable for encoding Thai words into Soundex codes for phonetic comparisons.

udom83
~~~~~~
.. autofunction:: udom83

The `udom83` module is based on a homonymic approach for sound-alike string search. It encodes Thai words using the Wannee Udompanich Soundex algorithm developed in 1983.

metasound
~~~~~~~~~
.. autofunction:: metasound

The `metasound` module implements a novel phonetic name matching algorithm with a statistical ontology for analyzing names based on Thai astrology. It offers advanced phonetic matching capabilities for Thai names.

prayut_and_somchaip
~~~~~~~~~~~~~~~~~~~
.. autofunction:: prayut_and_somchaip

The `prayut_and_somchaip` module is designed for Thai-English cross-language transliterated word retrieval using the Soundex technique. It is particularly useful for matching transliterated words in both languages.

complete_soundex
~~~~~~~~~~~~~~~~
.. autofunction:: complete_soundex

The `complete_soundex` function implements the Complete Soundex algorithm for Thai word phonetic encoding based on Tapsai et al. (2020). Unlike traditional Soundex methods, it generates variable-length codes representing every syllable in a word.

Each syllable is encoded using a 7-character block structure:

* Initial Consonant (2 chars) - Phonetic grouping
* Vowel (2 chars) - Including length markers
* Final Consonant (1 char) - Sonorant clustering
* Tone (1 char) - Tone mark encoding
* Cluster Symbol (1 char) - Second consonant in clusters

The algorithm handles complex Thai phonetic patterns including ทร transformation, รร special rules, cluster detection, and implicit vowels. Multi-syllable words are automatically tokenized and encoded. This soundex is particularly effective for handling misspelled words, character variations, and similar pronunciations.

complete_soundex_similarity
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: complete_soundex_similarity

The `complete_soundex_similarity` function calculates the similarity between two Complete Soundex codes using character-wise comparison.

The similarity is computed using the formula:

    S(X,Y) = Σ(sim(c_xi, c_yi)) / max(len(X), len(Y))

where sim = 1 if characters match at position i, else 0.

The result is normalized by the maximum length of the two codes, returning a float between 0.0 (no match) and 1.0 (perfect match). This function is useful for finding phonetically similar Thai words and handling spelling variations.

pythainlp.soundex.sound.word_approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.soundex.sound.word_approximation

The `pythainlp.soundex.sound.word_approximation` module offers word approximation functionality. It allows users to find Thai words that are phonetically similar to a given word.

pythainlp.soundex.sound.audio_vector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.soundex.sound.audio_vector

The `pythainlp.soundex.sound.audio_vector` module provides audio vector functionality for Thai words. It allows users to work with audio vectors based on phonetic properties.

pythainlp.soundex.sound.word2audio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.soundex.sound.word2audio

The `pythainlp.soundex.sound.word2audio` module is designed for converting Thai words to audio representations. It enables users to obtain audio vectors for Thai words, which can be used for various applications.

References
----------

.. [#metasound] Snae & Brückner. (2009). `Novel Phonetic Name Matching Algorithm with a Statistical Ontology for Analyzing Names Given in Accordance with Thai Astrology <https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf>`_.

.. [#udom83] Wannee Udompanich (1983). `String searching for Thai alphabet using Soundex compression technique <https://cuir.car.chula.ac.th/handle/123456789/48471>`_. Master Thesis. Chulalongkorn University, Thailand. วรรณี อุดมพาณิชย์. `การใช้หลักคำพ้องเสียง เพื่อค้นหาชุดอักขระภาษาไทยที่ออกเสียงเหมือนกัน <https://cuir.car.chula.ac.th/handle/123456789/48471>`_. วิทยานิพนธ์ (วท.ม.)--จุฬาลงกรณ์มหาวิทยาลัย, 2526.

.. [#lk82] Vichit Lorchirachoonkul. 1982. `A Thai soundex system <https://doi.org/10.1016/0306-4573(82)90003-6>`_. Information Processing & Management, 18(5):243–255. วิชิต หล่อจีระชุณห์กุล และ เจริญ คุวินทร์พันธุ์. `โปรแกรมการสืบค้นคำไทยตามเสียงอ่าน (Thai Soundex) <https://guru.sanook.com/1520/>`_.

.. [#prayut_and_somchaip] Prayut Suwanvisat, Somchai Prasitjutrakul. Thai-English Cross-Language Transliterated Word Retrieval using Soundex Technique. In 1998 [cited 2022 Sep 8]. Available from: https://www.cp.eng.chula.ac.th/~somchai/spj/papers/ThaiText/ncsec98-clir.pdf.

.. [#complete_soundex] Chalermpol Tapsai, Phayung Meesad, and Choochart Haruechaiyasak. 2020. `Complete Soundex for Thai Words Similarity Analysis <https://ph01.tci-thaijo.org/index.php/IT_Journal/article/view/241562/164358>`_. Information Technology Journal KMUTNB. 2020 June 30;16(1):46–59.

.. This enhanced documentation provides clear descriptions of all the modules within the `pythainlp.soundex` module, including their purposes and functionalities. Users can now better understand how to leverage these soundex algorithms for various phonetic matching tasks in the Thai language.
