Command Line
============

You can use PyThaiNLP from Command Line.

Run Command Line and type the commands:::

    thainlp

**Word tokenization**::

    thainlp tokenize word TEXT

*Example*::

    $ thainlp tokenize word สภาพการจ้างและสภาพการทำงาน
    สภาพการจ้าง|และ|สภาพ|การทำงาน|

**Syllable tokenization**::

    thainlp tokenize syllable TEXT

*Example*::

    $ thainlp tokenize syllable สภาพการจ้างและสภาพการทำงาน
    สภาพ~การ~จ้าง~และ~สภาพ~การ~ทำ~งาน~

**Subword tokenization**::

    thainlp tokenize subword TEXT

*Example*::

    $ thainlp tokenize subword สภาพการจ้างและสภาพการทำงาน
    ส/ภา/พ/กา/ร/จ้า/ง/และ/ส/ภา/พ/กา/ร/ทำ/งา/น/

**Part-Of-Speech tagging**::

    pythainlp tagg pos -s SEPARATOR TEXT

*Example*::

    $ thainlp tag pos -s . ผม.ไม่.กิน.เผ็ด

**Soundex**::

    thainlp soundex TEXT

*Example*::

    $ thainlp soundex บรรณการ
    บ319000

**Mange corpus**::

    thainlp data

**Help**::

    thainlp --help
