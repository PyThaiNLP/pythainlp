Command Line
============

You can use PyThaiNLP from Command Line.

Run Command Line and type the commands:::

    pythainlp

**Word tokenization**::

    pythainlp tokenization word --text TEXT

*Example*::

    $ pythainlp tokenization word --text "ผมร<0e31>กประเทศไทย? สามารถ" --engine newmm
    ผม|รัก|ประเทศไทย|?| |สามารถ


**Syllable tokenization**::

    pythainlp tokenization syllable --text TEXT

*Example*::

    $ pythainlp tokenization syllable --text "ผมร<0e31>กประเทศไทย? สามารถ"
    ผม~รัก~ประ~เทศ~ไทย~? ~สา~มารถ

**Part-Of-Speech tagging**::

    pythainlp tagging pos --text TEXT

*Example*::

    $ pythainlp tagging pos --text "ผม|ไม่|กิน|เผ็ด"

**Soundex**::

    pythainlp soundex --text TEXT

*Example*::

    $ pythainlp soundex --text "บ<0e39>รณการ" --engine lk82
    บE419

**Mange corpus**::

    pythainlp corpus

**Help**::

    pythainlp --help
