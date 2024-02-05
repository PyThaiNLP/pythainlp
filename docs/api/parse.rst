.. currentmodule:: pythainlp.parse

pythainlp.parse
===============
The :class:`pythainlp.parse` module provides dependency parsing for the Thai language. Dependency parsing is a fundamental task in natural language processing that involves identifying the grammatical relationships between words in a sentence, which helps to analyze sentence structure and meaning.

Modules
-------

dependency_parsing
~~~~~~~~~~~~~~~~~
.. autofunction:: dependency_parsing

The `dependency_parsing` function is the core component of the `pythainlp.parse` module. It offers dependency parsing capabilities for the Thai language. Given a Thai sentence as input, this function parses the sentence to identify the grammatical relationships between words, creating a dependency tree that represents the sentence's structure.

Usage
~~~~~

To use the `dependency_parsing` function for Thai dependency parsing, follow these steps:

1. Import the `pythainlp.parse` module.
2. Use the `dependency_parsing` function with a Thai sentence as input.
3. The function will return the dependency parsing results, which include information about the grammatical relationships between words.

Example
~~~~~~~

Here's a basic example of how to use the `dependency_parsing` function:

::

    from pythainlp.parse import dependency_parsing
    
    # Input Thai sentence
    sentence = "พี่น้องชาวบ้านกำลังเลี้ยงสตางค์ในสวน"
    
    # Perform dependency parsing
    parsing_result = dependency_parsing(sentence)
    
    # Print the parsing result
    print(parsing_result)
