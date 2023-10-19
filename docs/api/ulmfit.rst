.. currentmodule:: pythainlp.ulmfit

pythainlp.ulmfit
====================================
Welcome to the `pythainlp.ulmfit` module, where you'll find powerful tools for Universal Language Model Fine-tuning for Text Classification (ULMFiT). ULMFiT is a cutting-edge technique for training deep learning models on large text corpora and then fine-tuning them for specific text classification tasks.

Modules
-------

.. autoclass:: ThaiTokenizer
   :members:
   
   The `ThaiTokenizer` class is a critical component of ULMFiT, designed for tokenizing Thai text effectively. Tokenization is the process of breaking down text into individual tokens, and this class allows you to do so with precision and accuracy.

.. autofunction:: document_vector
   :noindex:

   The `document_vector` function is a powerful tool that computes document vectors for text data. This functionality is often used in text classification tasks where you need to represent documents as numerical vectors for machine learning models.

.. autofunction:: fix_html
   :noindex:

   The `fix_html` function is a text preprocessing utility that handles HTML-specific characters, making text cleaner and more suitable for text classification.

.. autofunction:: lowercase_all
   :noindex:

   The `lowercase_all` function is a text processing utility that converts all text to lowercase. This is useful for ensuring uniformity in text data and reducing the complexity of text classification tasks.

.. autofunction:: merge_wgts
   :noindex:

   The `merge_wgts` function is a tool for merging weight arrays, which can be crucial for managing and fine-tuning deep learning models in ULMFiT.

.. autofunction:: process_thai
   :noindex:

   The `process_thai` function is designed for preprocessing Thai text data, a vital step in preparing text for ULMFiT-based text classification.

.. autofunction:: rm_brackets
   :noindex:

   The `rm_brackets` function removes brackets from text, making it more suitable for text classification tasks that don't require bracket information.

.. autofunction:: rm_useless_newlines
   :noindex:

   The `rm_useless_newlines` function eliminates unnecessary newlines in text data, ensuring that text is more compact and easier to work with in ULMFiT-based text classification.

.. autofunction:: rm_useless_spaces
   :noindex:

   The `rm_useless_spaces` function removes extraneous spaces from text, making it cleaner and more efficient for ULMFiT-based text classification.

.. autofunction:: remove_space
   :noindex:

   The `remove_space` function is a utility for removing space characters from text data, streamlining the text for classification purposes.

.. autofunction:: replace_rep_after
   :noindex:

   The `replace_rep_after` function is a text preprocessing tool for replacing repeated characters in text with a single occurrence. This step helps in standardizing text data for text classification.

.. autofunction:: replace_rep_nonum
   :noindex:

   The `replace_rep_nonum` function is similar to `replace_rep_after`, but it focuses on replacing repeated characters without considering numbers.

.. autofunction:: replace_wrep_post
   :noindex:

   The `replace_wrep_post` function is used for replacing repeated words in text with a single occurrence. This function helps in reducing redundancy in text data, making it more efficient for text classification tasks.

.. autofunction:: replace_wrep_post_nonum
   :noindex:

   Similar to `replace_wrep_post`, the `replace_wrep_post_nonum` function removes repeated words without considering numbers in the text.

.. autofunction:: spec_add_spaces
   :noindex:

   The `spec_add_spaces` function is a text processing tool for adding spaces between special characters in text data. This step helps in standardizing text for ULMFiT-based text classification.

.. autofunction:: ungroup_emoji
   :noindex:

   The `ungroup_emoji` function is designed for ungrouping emojis in text data, which can be crucial for emoji recognition and classification tasks.

.. The `pythainlp.ulmfit` module provides a comprehensive set of tools for ULMFiT-based text classification. Whether you need to preprocess Thai text, tokenize it, compute document vectors, or perform various text cleaning tasks, this module has the utilities you need. ULMFiT is a state-of-the-art technique in NLP, and these tools empower you to use it effectively for text classification.
