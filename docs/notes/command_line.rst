Command Line
============

You can use PyThaiNLP from Command Line.

Run Command Line and type the commands:::

    pythainlp

**Word segment**::

    pythainlp -t TEXT -seg

*Example*::

    $ pythainlp -t แมวกินปลา -seg
    แมว|กิน|ปลา

**Postag**::

    pythainlp -t TEXT -pos

*Example*::

    $ pythainlp -t แมวกินปลา -pos
    แมว/NCMN	กิน/VACT	ปลา/NCMN

**Mange corpus**::

    pythainlp -c

**Help**::

    pythainlp --help
