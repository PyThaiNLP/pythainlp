.. currentmodule:: pythainlp.chunk

pythainlp.chunk
===============
The :mod:`pythainlp.chunk` module provides phrase structure chunking for Thai
text, following the NLTK :mod:`nltk.chunk` naming convention.

Chunking groups POS-tagged tokens into phrase structure chunks and returns
labels in Inside-Outside-Beginning (IOB) format.

*B-* prefix indicates the beginning token of a chunk. *I-* prefix indicates
a token inside (continuing) a chunk. *O* indicates that the token does not
belong to any chunk.

Modules
-------

chunk_parse
~~~~~~~~~~~
.. autofunction:: chunk_parse

CRFChunkParser
~~~~~~~~~~~~~~
.. autoclass:: CRFChunkParser
   :members:
