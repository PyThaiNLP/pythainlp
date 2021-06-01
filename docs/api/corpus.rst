.. currentmodule:: pythainlp.corpus

pythainlp.corpus
====================================
The :class:`pythainlp.corpus` provides access to corpus that comes with PyThaiNLP.

Modules
-------

.. autofunction:: countries
.. autofunction:: get_corpus
.. autofunction:: get_corpus_db
.. autofunction:: get_corpus_db_detail
.. autofunction:: get_corpus_default_db
.. autofunction:: get_corpus_path
.. autofunction:: download
.. autofunction:: remove
.. autofunction:: provinces
.. autofunction:: thai_stopwords
.. autofunction:: thai_words
.. autofunction:: thai_syllables
.. autofunction:: thai_negations
.. autofunction:: thai_family_names
.. autofunction:: thai_female_names
.. autofunction:: thai_male_names

ConceptNet
----------

ConceptNet is an open, multilingual knowledge graph
See: https://github.com/commonsense/conceptnet5/wiki/API

.. autofunction:: pythainlp.corpus.conceptnet.edges

TNC
---

.. autofunction:: pythainlp.corpus.tnc.word_freqs

TTC
---

.. autofunction:: pythainlp.corpus.ttc.word_freqs

Util
----

.. autofunction:: pythainlp.corpus.util.find_badwords
.. autofunction:: pythainlp.corpus.util.revise_wordset
.. autofunction:: pythainlp.corpus.util.revise_newmm_default_wordset

WordNet
-------

PyThaiNLP API is an exact copy of NLTK WordNet API.
See: https://www.nltk.org/howto/wordnet.html

.. autofunction:: pythainlp.corpus.wordnet.synsets
.. autofunction:: pythainlp.corpus.wordnet.synset
.. autofunction:: pythainlp.corpus.wordnet.all_lemma_names
.. autofunction:: pythainlp.corpus.wordnet.all_synsets
.. autofunction:: pythainlp.corpus.wordnet.langs
.. autofunction:: pythainlp.corpus.wordnet.lemmas
.. autofunction:: pythainlp.corpus.wordnet.lemma
.. autofunction:: pythainlp.corpus.wordnet.lemma_from_key
.. autofunction:: pythainlp.corpus.wordnet.path_similarity
.. autofunction:: pythainlp.corpus.wordnet.lch_similarity
.. autofunction:: pythainlp.corpus.wordnet.wup_similarity
.. autofunction:: pythainlp.corpus.wordnet.morphy
.. autofunction:: pythainlp.corpus.wordnet.custom_lemmas

Definition
++++++++++

Synset
    a set of synonyms that share a common meaning.
