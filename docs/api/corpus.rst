.. currentmodule:: pythainlp.corpus

pythainlp.corpus
================
The :class:`pythainlp.corpus` module provides access to various Thai language corpora and resources that come bundled with PyThaiNLP. These resources are essential for natural language processing tasks in the Thai language.

Modules
-------

countries
~~~~~~~~~~
.. autofunction:: countries
   :noindex:

get_corpus
~~~~~~~~~~
.. autofunction:: get_corpus
   :noindex:

get_corpus_db
~~~~~~~~~~~~~~
.. autofunction:: get_corpus_db
   :noindex:

get_corpus_db_detail
~~~~~~~~~~~~~~~~~~~~
.. autofunction:: get_corpus_db_detail
   :noindex:

get_corpus_default_db
~~~~~~~~~~~~~~~~~~~~
.. autofunction:: get_corpus_default_db
   :noindex:

get_corpus_path
~~~~~~~~~~~~~~
.. autofunction:: get_corpus_path
   :noindex:

download
~~~~~~~~~~
.. autofunction:: download
   :noindex:

remove
~~~~~~~
.. autofunction:: remove
   :noindex:

provinces
~~~~~~~~~~
.. autofunction:: provinces
   :noindex:

thai_dict
~~~~~~~~~~
.. autofunction:: thai_dict
   :noindex:

thai_stopwords
~~~~~~~~~~~~~~
.. autofunction:: thai_stopwords
   :noindex:

thai_words
~~~~~~~~~~
.. autofunction:: thai_words
   :noindex:

thai_wsd_dict
~~~~~~~~~~~~~~
.. autofunction:: thai_wsd_dict
   :noindex:

thai_orst_words
~~~~~~~~~~~~~~~~~
.. autofunction:: thai_orst_words
   :noindex:

thai_synonym
~~~~~~~~~~~~~~
.. autofunction:: thai_synonym
   :noindex:

thai_syllables
~~~~~~~~~~~~~~
.. autofunction:: thai_syllables
   :noindex:

thai_negations
~~~~~~~~~~~~~~
.. autofunction:: thai_negations
   :noindex:

thai_family_names
~~~~~~~~~~~~~~~~~~~
.. autofunction:: thai_family_names
   :noindex:

thai_female_names
~~~~~~~~~~~~~~~~~~~
.. autofunction:: thai_female_names
   :noindex:

thai_male_names
~~~~~~~~~~~~~~~~
.. autofunction:: thai_male_names
   :noindex:

pythainlp.corpus.th_en_translit.get_transliteration_dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.th_en_translit.get_transliteration_dict
   :noindex:

ConceptNet
----------

ConceptNet is an open, multilingual knowledge graph used for various natural language understanding tasks. For more information, refer to the `ConceptNet documentation <https://github.com/commonsense/conceptnet5/wiki/API>`_.

pythainlp.corpus.conceptnet.edges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.conceptnet.edges
   :noindex:

TNC (Thai National Corpus)
---

The Thai National Corpus (TNC) is a collection of text data in the Thai language. This module provides access to word frequency data from the TNC corpus.

pythainlp.corpus.tnc.word_freqs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.tnc.word_freqs
   :noindex:

pythainlp.corpus.tnc.unigram_word_freqs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.tnc.unigram_word_freqs
   :noindex:

pythainlp.corpus.tnc.bigram_word_freqs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.tnc.bigram_word_freqs
   :noindex:

pythainlp.corpus.tnc.trigram_word_freqs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.tnc.trigram_word_freqs
   :noindex:

TTC (Thai Textbook Corpus)
---

The Thai Textbook Corpus (TTC) is a collection of Thai language text data, primarily sourced from textbooks.

pythainlp.corpus.ttc.word_freqs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.ttc.word_freqs
   :noindex:

pythainlp.corpus.ttc.unigram_word_freqs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.ttc.unigram_word_freqs
   :noindex:

OSCAR
-----

OSCAR is a multilingual corpus that includes Thai text data. This module provides access to word frequency data from the OSCAR corpus.

pythainlp.corpus.oscar.word_freqs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.oscar.word_freqs
   :noindex:

pythainlp.corpus.oscar.unigram_word_freqs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.oscar.unigram_word_freqs
   :noindex:

Util
----

Utilities for working with the corpus data.

pythainlp.corpus.util.find_badwords
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.util.find_badwords
   :noindex:

pythainlp.corpus.util.revise_wordset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.util.revise_wordset
   :noindex:

pythainlp.corpus.util.revise_newmm_default_wordset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.util.revise_newmm_default_wordset
   :noindex:

WordNet
-------

PyThaiNLP API includes the WordNet module, which is an exact copy of NLTK's WordNet API for the Thai language. WordNet is a lexical database for English and other languages.

For more details on WordNet, refer to the `NLTK WordNet documentation <https://www.nltk.org/howto/wordnet.html>`_.

pythainlp.corpus.wordnet.synsets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.synsets
   :noindex:

pythainlp.corpus.wordnet.synset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.synset
   :noindex:

pythainlp.corpus.wordnet.all_lemma_names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.all_lemma_names
   :noindex:

pythainlp.corpus.wordnet.all_synsets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.all_synsets
   :noindex:

pythainlp.corpus.wordnet.langs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.langs
   :noindex:

pythainlp.corpus.wordnet.lemmas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.lemmas
   :noindex:

pythainlp.corpus.wordnet.lemma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.lemma
   :noindex:

pythainlp.corpus.wordnet.lemma_from_key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.lemma_from_key
   :noindex:

pythainlp.corpus.wordnet.path_similarity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.path_similarity
   :noindex:

pythainlp.corpus.wordnet.lch_similarity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.lch_similarity
   :noindex:

pythainlp.corpus.wordnet.wup_similarity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.wup_similarity
   :noindex:

pythainlp.corpus.wordnet.morphy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.morphy
   :noindex:

pythainlp.corpus.wordnet.custom_lemmas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pythainlp.corpus.wordnet.custom_lemmas
   :noindex:

Definition
++++++++++

Synset
~~~~~~~
A synset is a set of synonyms that share a common meaning. The WordNet module provides functionality to work with these synsets.

This documentation is designed to help you navigate and use the various resources and modules available in the `pythainlp.corpus` package effectively. If you have any questions or need further assistance, please refer to the PyThaiNLP documentation or reach out to the PyThaiNLP community for support.

We hope you find this documentation helpful for your natural language processing tasks in the Thai language.
