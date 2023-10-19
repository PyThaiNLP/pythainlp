.. currentmodule:: pythainlp.spell

pythainlp.spell
===============
The :class:`pythainlp.spell` module is a powerful tool for finding the closest correctly spelled word to a given text in the Thai language. It provides functionalities to correct spelling errors and enhance the accuracy of text processing.

Modules
-------

correct
~~~~~~~
.. autofunction:: correct

The `correct` function is designed to correct the spelling of a single Thai word. Given an input word, this function returns the closest correctly spelled word from the dictionary, making it valuable for spell-checking and text correction tasks.

correct_sent
~~~~~~~~~~~~
.. autofunction:: correct_sent

The `correct_sent` function is an extension of the `correct` function and is used to correct an entire sentence. It tokenizes the input sentence, corrects each word, and returns the corrected sentence. This is beneficial for proofreading and improving the readability of Thai text.

spell
~~~~~
.. autofunction:: spell

The `spell` function is responsible for identifying spelling errors within a given Thai word. It checks whether the input word is spelled correctly or not and returns a Boolean result. This function is useful for validating the correctness of Thai words.

spell_sent
~~~~~~~~~~
.. autofunction:: spell_sent

The `spell_sent` function extends the spell-checking functionality to entire sentences. It tokenizes the input sentence and checks the spelling of each word. It returns a list of Booleans indicating whether each word in the sentence is spelled correctly or not.

NorvigSpellChecker
~~~~~~~~~~~~~~~~~~
.. autoclass:: NorvigSpellChecker
   :special-members:
   :members:

The `NorvigSpellChecker` class is a fundamental component of the `pythainlp.spell` module. It implements a spell-checking algorithm based on the work of Peter Norvig. This class is designed for more advanced spell-checking and provides customizable settings for spell correction.

DEFAULT_SPELL_CHECKER
~~~~~~~~~~~~~~~~~~~~~
.. autodata:: DEFAULT_SPELL_CHECKER
   :annotation: = Default instance of the standard NorvigSpellChecker, using word list data from the Thai National Corpus: http://www.arts.chula.ac.th/ling/tnc/

The `DEFAULT_SPELL_CHECKER` is an instance of the `NorvigSpellChecker` class with default settings. It is pre-configured to use word list data from the Thai National Corpus, making it a reliable choice for general spell-checking tasks.

References
----------

.. [#norvig_spellchecker]  Peter Norvig (2007). `How to Write a Spelling Corrector <http://norvig.com/spell-correct.html>`_.
