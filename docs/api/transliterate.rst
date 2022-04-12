.. currentmodule:: pythainlp.transliterate

pythainlp.transliterate
====================================
The :class:`pythainlp.transliterate` turns Thai text into a romanized one (put simply, spelled with English).

Modules
-------

.. autofunction:: romanize
.. autofunction:: transliterate
.. autofunction:: pronunciate
.. autofunction:: puan

Romanize Engines
----------------
thai2rom
++++++++
.. automodule:: pythainlp.transliterate.thai2rom.romanize
royin
+++++
.. automodule:: pythainlp.transliterate.royin.romanize

Transliterate Engines
---------------------

icu
+++
.. automodule::  pythainlp.transliterate.pyicu

.. autofunction:: pythainlp.transliterate.pyicu.transliterate

ipa
+++
.. automodule::  pythainlp.transliterate.ipa
.. autofunction::  pythainlp.transliterate.ipa.transliterate
.. autofunction::  pythainlp.transliterate.ipa.trans_list
.. autofunction::  pythainlp.transliterate.ipa.xsampa_list

thaig2p
+++++++
.. automodule::  pythainlp.transliterate.thaig2p.transliterate
.. autofunction::  pythainlp.transliterate.thaig2p.transliterate

iso_11940
+++++++++
.. automodule::  pythainlp.transliterate.iso_11940

References
----------

.. [#rtgs_transcription] Nitaya Kanchanawan. (2006). `Romanization, Transliteration, and Transcription for the Globalization of the Thai Language. <http://www.royin.go.th/wp-content/uploads/royin-ebook/276/FileUpload/758_6484.pdf>`_
        The Journal of the Royal Institute of Thailand.
