.. currentmodule:: pythainlp.khavee

pythainlp.khavee
================
The :class:`pythainlp.khavee` module is a powerful toolkit designed for working with Thai poetry. The term "khavee" corresponds to "กวี" in the Thai language, which translates to "Poetry" in English. This toolkit equips users with the tools and utilities necessary for the creation, analysis, and verification of Thai poetry.

Modules
-------

KhaveeVerifier
~~~~~~~~~~~~~~
.. autoclass:: KhaveeVerifier
   :special-members:
   :members:

The :class:`KhaveeVerifier` class is the primary component of the `pythainlp.khavee` module, dedicated to the verification of Thai poetry. It offers a range of functions and methods for analyzing and validating Thai poetry, ensuring its adherence to the rules and structure of classical Thai poetic forms.

.. Attributes and Methods
.. ~~~~~~~~~~~~~~~~~~~~~~

.. The `KhaveeVerifier` class provides a variety of attributes and methods to facilitate the verification of Thai poetry. Some of its key features include:

.. - `__init__(rules: dict = None, stanza_rules: dict = None, verbose: bool = False)`
..   - The constructor for the `KhaveeVerifier` class, allowing you to initialize an instance with custom rules, stanza rules, and verbosity settings.

.. - `is_khavee(text: str, rules: dict = None)`
..   - The `is_khavee` method checks whether a given text conforms to the rules of Thai poetry. It returns `True` if the text is a valid Thai poem according to the specified rules, and `False` otherwise.

.. - `get_rules()`
..   - The `get_rules` method retrieves the current set of rules being used by the verifier. This is helpful for inspecting and modifying the rules during runtime.

.. - `set_rules(rules: dict)`
..   - The `set_rules` method allows you to set custom rules for the verifier, offering flexibility in defining specific constraints for Thai poetry.

.. Usage
.. ~~~~~

.. To use the `KhaveeVerifier` class for Thai poetry verification, follow these steps:

.. 1. Initialize an instance of the `KhaveeVerifier` class, optionally specifying custom rules and verbosity settings.

.. 2. Use the `is_khavee` method to verify whether a given text adheres to the rules of Thai poetry. The method returns a Boolean value indicating the result.

.. 3. Utilize the `get_rules` and `set_rules` methods to inspect and modify the rules as needed.

Example
~~~~~~~

Here's a basic example of how to use the `KhaveeVerifier` class to verify Thai poetry:

::
  from pythainlp.khavee import KhaveeVerifier
  
  # Initialize a KhaveeVerifier instance
  verifier = KhaveeVerifier()
  
  # Text to verify
  poem_text = "ดอกไม้สวยงาม แสนสดใส"
  
  # Verify if the text is Thai poetry
  is_poetry = verifier.is_khavee(poem_text)
  
  print(f"The provided text is Thai poetry: {is_poetry}")
