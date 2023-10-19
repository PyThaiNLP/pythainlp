.. currentmodule:: pythainlp.tokenize
.. _tokenize-doc:

pythainlp.tokenize
==================
The :mod:`pythainlp.tokenize` module contains a comprehensive set of functions and classes for tokenizing Thai text into various units, such as sentences, words, subwords, and more. This module is a fundamental component of the PyThaiNLP library, providing tools for natural language processing in the Thai language.

Modules
-------

.. autofunction:: clause_tokenize
    :noindex:
    
    Tokenizes text into clauses. This function allows you to split text into meaningful sections, making it useful for more advanced text processing tasks.

.. autofunction:: sent_tokenize
    :noindex:
    
    Splits Thai text into sentences. This function identifies sentence boundaries, which is essential for text segmentation and analysis.

.. autofunction:: paragraph_tokenize
    :noindex:
    
    Segments text into paragraphs, which can be valuable for document-level analysis or summarization.

.. autofunction:: subword_tokenize
    :noindex:
    
    Tokenizes text into subwords, which can be helpful for various NLP tasks, including subword embeddings.

.. autofunction:: syllable_tokenize
    :noindex:
    
    Divides text into syllables, allowing you to work with individual Thai language phonetic units.

.. autofunction:: word_tokenize
    :noindex:
    
    Splits text into words. This function is a fundamental tool for Thai language text analysis.

.. autofunction:: word_detokenize
    :noindex:
    
    Reverses the tokenization process, reconstructing text from tokenized units. Useful for text generation tasks.

.. autoclass:: Tokenizer
    :members:
    
    The `Tokenizer` class is a versatile tool for customizing tokenization processes and managing tokenization models. It provides various methods and attributes to fine-tune tokenization according to your specific needs.

Tokenization Engines
--------------------

This module offers multiple tokenization engines designed for different levels of text analysis.

Sentence level
--------------

**crfcut**
  
.. automodule:: pythainlp.tokenize.crfcut
    :members:
    
    A tokenizer that operates at the sentence level using Conditional Random Fields (CRF). It is suitable for segmenting text into sentences accurately.

**thaisumcut**
  
.. automodule:: pythainlp.tokenize.thaisumcut
    :members:
    
    A sentence tokenizer based on a maximum entropy model. It's a great choice for sentence boundary detection in Thai text.

Word level
----------

**attacut**
  
.. automodule:: pythainlp.tokenize.attacut
    :members:
    
    A tokenizer designed for word-level segmentation. It provides accurate word boundary detection in Thai text.

**deepcut**
  
.. automodule:: pythainlp.tokenize.deepcut
    :members:
    
    Utilizes deep learning techniques for word segmentation, achieving high accuracy and performance.

**multi_cut**
  
.. automodule:: pythainlp.tokenize.multi_cut
    :members:
    
    An ensemble tokenizer that combines multiple tokenization strategies for improved word segmentation.

**nlpo3**
  
.. automodule:: pythainlp.tokenize.nlpo3
    :members:
    
    A word tokenizer based on the NLPO3 model. It offers advanced word boundary detection and is suitable for various NLP tasks.

**longest**
  
.. automodule:: pythainlp.tokenize.longest
    :members:
    
    A tokenizer that identifies word boundaries by selecting the longest possible words in a text.

**pyicu**
  
.. automodule:: pythainlp.tokenize.pyicu
    :members:
    
    An ICU-based word tokenizer offering robust support for Thai text segmentation.

**nercut**
  
.. automodule:: pythainlp.tokenize.nercut
    :members:
    
    A tokenizer optimized for Named Entity Recognition (NER) tasks, ensuring accurate tokenization for entity recognition.

**sefr_cut**
  
.. automodule:: pythainlp.tokenize.sefr_cut
    :members:
    
    An advanced word tokenizer for segmenting Thai text, with a focus on precision.

**oskut**
  
.. automodule:: pythainlp.tokenize.oskut
    :members:
    
    A tokenizer that uses a pre-trained model for word segmentation. It's a reliable choice for general-purpose text analysis.

**newmm (Default)**
  
.. automodule:: pythainlp.tokenize.newmm
    :members:
    
    The default word tokenization engine that provides a balance between accuracy and efficiency for most use cases.

Subword level
-------------

**tcc**
  
.. automodule:: pythainlp.tokenize.tcc
    :members:
    
    Tokenizes text into Thai Character Clusters (TCCs), a subword level representation.

**tcc+**
  
.. automodule:: pythainlp.tokenize.tcc_p
    :members:
    
    A subword tokenizer that includes additional rules for more precise subword segmentation.

**etcc**
  
.. automodule:: pythainlp.tokenize.etcc
    :members:
    
    Enhanced Thai Character Clusters (eTCC) tokenizer for subword-level analysis.

**han_solo**
  
.. automodule:: pythainlp.tokenize.han_solo
    :members:
    
    A subword tokenizer specialized for Han characters and mixed scripts, suitable for various text processing scenarios.
