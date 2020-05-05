Command Line
============

You can use some thainlp functions directly from command line.

**Tokenization**::

    thainlp tokenize <word|syllable|subword|sent> [-w] [-nw] [-a newmm|attacut|longest] [-s SEPARATOR] TEXT

*Example*::

    $ thainlp tokenize word สภาพการจ้างและสภาพการทำงาน
    สภาพการจ้าง|และ|สภาพ|การทำงาน|

    $ thainlp tokenize syllable สภาพการจ้างและสภาพการทำงาน
    สภาพ~การ~จ้าง~และ~สภาพ~การ~ทำ~งาน~

    $ thainlp tokenize subword สภาพการจ้างและสภาพการทำงาน
    ส/ภา/พ/กา/ร/จ้า/ง/และ/ส/ภา/พ/กา/ร/ทำ/งา/น/

    $ thainlp tokenize word -a longest "แรงงานกะดึก: ฟันเฟืองที่ยังหมุนในคำ่คืนมีเคอร์ฟิว"
    แรงงาน|กะ|ดึก|:| |ฟันเฟือง|ที่|ยัง|หมุน|ใน|คำ่|คืน|มี|เคอร์ฟิว|

    $ thainlp tokenize word -nw -s # "5 เหตุผล 'ไม่ควร' ต่อพ.ร.ก.ฉุกเฉิน"
    5#เหตุผล#'#ไม่#ควร#'#ต่อ#พ.ร.ก.#ฉุกเฉิน#

**Part-Of-Speech tagging**::

    pythainlp tagg pos [-s SEPARATOR] TEXT

*Example*::

    $ thainlp tag pos -s . ผม.ไม่.กิน.เผ็ด

**Soundex**::

    thainlp soundex [-a udom83|lk82|metasound] TEXT

*Example*::

    $ thainlp soundex วรรณ
    ว330000

    $ thainlp soundex -a lk82 วัน
    ว4000

    $ thainlp soundex -a lk82 วรรณ
    ว4000

**Corpus management**::

    thainlp data <catalog|info|get|rm|path>

*Example*::

    $ thainlp data path
    /Users/user1/pythainlp-data

    $ thainlp data catalog
    Dataset/corpus available for download:
    - crfcut 0.1
    - thai-g2p 0.1  (Local: 0.1)
    - thai2fit_wv 0.1
    - thainer-1-3 1.3

    $ thainlp data get thai2fit_wv
    Corpus: thai2fit_wv
    - Downloading: thai2fit_wv 0.1
    36%|█████████████████▉                                |

    $ thainlp data --help

**Help**::

    thainlp --help
