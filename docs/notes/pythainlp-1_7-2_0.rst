From PyThaiNLP 1.7 to PyThaiNLP 2.0
===================================

Sentiment Analysis
------------------

We are removing sentiment analysis in PyThaiNLP 2.0
https://github.com/PyThaiNLP/pythainlp/issues/172#issuecomment-457456966

Soundex
-------

-  from ``pythainlp.soundex.LK82`` to ``pythainlp.soundex.lk82``
-  from ``pythainlp.soundex.Udom83`` to ``pythainlp.soundex.udom83``

Romanization
------------

-  from ``pythainlp.romanization.romanization`` to
   ``pythainlp.transliterate.romanize``

collation
---------

from ``pythainlp.collation.collation`` to ``pythainlp.util.collate``

change
------

-  from ``pythainlp.change.texttothai`` to
   ``pythainlp.util.thai_to_eng``
-  from ``pythainlp.change.texttoeng`` to ``pythainlp.util.eng_to_thai``

rank
----

from ``pythainlp.rank.rank`` to ``pythainlp.util.rank``

number
------

-  from ``pythainlp.number.thai_num_to_num`` to
   ``pythainlp.util.thai_digit_to_arabic_digit``
-  from ``pythainlp.number.num_to_thai_num`` to
   ``pythainlp.util.arabic_digit_to_thai_digit``
-  from ``pythainlp.number.num_to_text`` to
   ``pythainlp.util.num_to_thaiword``
-  from ``pythainlp.number.text_to_num`` to
   ``pythainlp.util.text_to_arabic_digit``
-  from ``pythainlp.number.numtowords`` to
   ``pythainlp.util.num_to_thaiword``

Named Entity Recognition
------------------------

from ``pythainlp.ner.thainer`` to
``pythainlp.tag.named_entity.ThaiNameTagger``

MetaSound
---------

from ``pythainlp.MetaSound.MetaSound(name)`` to
``pythainlp.soundex.metasound(name)``

Corpus
------

stopword
~~~~~~~~

from ``pythainlp.corpus.stopwords.words("thai")`` to
``pythainlp.corpus.common.thai_stopwords()``

Tone in Thai
~~~~~~~~~~~~

from ``pythainlp.corpus.tone.get_data()`` to
``pythainlp.thai_tonemarks``

Consonant in thai
~~~~~~~~~~~~~~~~~

from ``pythainlp.corpus.alphabet.get_data()`` to
``pythainlp.thai_consonants``

Word list in thai
~~~~~~~~~~~~~~~~~

from ``pythainlp.corpus.thaiword.get_data()`` to
``pythainlp.corpus.thai_words()``

Thai country name
~~~~~~~~~~~~~~~~~

from ``pythainlp.corpus.country.get_data()`` to
``pythainlp.corpus.countries()``
