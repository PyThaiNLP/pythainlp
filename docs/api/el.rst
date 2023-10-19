.. currentmodule:: pythainlp.el

pythainlp.el
============
The :class:`pythainlp.el` module is an essential component of Thai Entity Linking within the PyThaiNLP library. Entity Linking is a key natural language processing task that associates mentions in text with corresponding entities in a knowledge base.

.. autoclass:: EntityLinker
   :members:

EntityLinker
------------

The :class:`EntityLinker` class is the core component of the `pythainlp.el` module, responsible for Thai Entity Linking. Entity Linking, also known as Named Entity Linking (NEL), plays a critical role in various applications, including question answering, information retrieval, and knowledge graph construction.

.. Attributes and Methods
.. ~~~~~~~~~~~~~~~~~~~~~~

.. The `EntityLinker` class offers the following attributes and methods:

.. - `__init__(text, engine="default")`
..   - The constructor for the `EntityLinker` class. It takes the input `text` and an optional `engine` parameter to specify the entity linking engine. The default engine is used if no specific engine is provided.

.. - `link()`
..   - The `link` method performs entity linking on the input text using the specified engine. It returns a list of entities linked in the text, along with their relevant information.

.. - `set_engine(engine)`
..   - The `set_engine` method allows you to change the entity linking engine during runtime. This provides flexibility in selecting different engines for entity linking based on your specific requirements.

.. - `get_linked_entities()`
..   - The `get_linked_entities` method retrieves a list of linked entities from the last entity linking operation. This is useful for extracting the entities found in the text.

.. Usage
.. ~~~~~

.. To use the `EntityLinker` class for entity linking, follow these steps:

.. 1. Initialize an `EntityLinker` object with the input text and, optionally, specify the engine.

.. 2. Call the `link` method to perform entity linking on the text.

.. 3. Utilize the `get_linked_entities` method to access the linked entities found in the text.

Example
~~~~~~~

Here's a simple example of how to use the `EntityLinker` class:

::
  from pythainlp.el import EntityLinker
  
  text = "กรุงเทพเป็นเมืองหลวงของประเทศไทย"
  el = EntityLinker()
  linked_entities = el.get_el(text)
  print(linked_entities)
