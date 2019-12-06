.. currentmodule:: pythainlp.tag

pythainlp.tag
=====================================
The :class:`pythainlp.tag` contains functions that are used to tag different parts of a text including 
Part-of-Speech (POS) tags, and Named Entity Recognition (NER) tag.

For the POS tags, there are two set of tags including `Universal Dependencies (UD) <https://universaldependencies.org/>`_ and ORCHID [#Sornlertlamvanich_2000]_ POS tags.

The following table shows the list of Part-of-Speech (POS) tags according to Universal Dependencies (UD) POS tags:

============   ==========================   =============================
Abbreviation   Part-of-Speech tag           Examples                     
============   ==========================   =============================
 ADJ           Adjective                    ใหม่, พิเศษ , ก่อน, มาก, สูง    
 ADP           Adposition                   แม้, ว่า, เมื่อ, ของ, สำหรับ     
 ADV           Adverb                       ก่อน, ก็, เล็กน้อย, เลย, สุด     
 AUX           Auxiliary                    เป็น, ใช่, คือ, คล้าย           
 CCONJ         Coordinating conjunction     แต่, และ, หรือ                
 DET           Determiner                   ที่, นี้, ซึ่ง, ทั้ง, ทุก, หลาย      
 INTJ          Interjection                 อุ้ย, โอ้ย
 NOUN          Noun                         กำมือ, พวก, สนาม, กีฬา, บัญชี  
 NUM           Numeral                      5,000, 103.7, 2004, หนึ่ง, ร้อย
 PART          Particle                     มา ขึ้น ไม่ ได้ เข้า             
 PRON          Pronoun                      เรา, เขา, ตัวเอง, ใคร, เธอ  
 PROPN         Proper noun                  โอบามา, แคปิตอลฮิล, จีโอพี, ไมเคิล
 PUNCT         Punctuation                  (, ), ", ', :               
 SCONJ         Subordinating conjunction    หาก                         
 VERB          Verb                         เปิด, ให้, ใช้, เผชิญ, อ่าน      
============   ==========================   =============================

The following table shows the list of Part-of-Speech (POS) tags according to ORCHID POS tags from the paper:

============   =================================================      =================================
Abbreviation   Part-of-Speech tag                                     Examples                     
============   =================================================      =================================
 NPRP          Proper noun                                            วินโดวส์ 95, โคโรน่า, โค้ก
 NCNM          Cardinal number                                        หนึ่ง, สอง, สาม, 1, 2, 10
 NONM          Ordinal number                                         ที่หนึ่ง, ที่สอง, ที่สาม, ที่1, ที่2
 NLBL          Label noun                                             1, 2, 3, 4, ก, ข, a, b
 NCMN          Common noun                                            หนังสือ, อาหาร, อาคาร, คน
 NTTL          Title noun                                             ครู, พลเอก
 PPRS          Personal pronoun                                       คุณ, เขา, ฉัน
 PDMN          Demonstrative pronoun                                  นี่, นั้น, ที่นั่น, ที่นี่
 PNTR          Interrogative pronoun                                  ใคร, อะไร, อย่างไร
 PREL          Relative pronoun                                       ที่, ซึ่ง, อัน, ผู้
 VACT          Active verb Îµµ,                                       ทำงาน, ร้องเพลง, กิน
 VSTA          Stative verb                                           เห็น, รู้, คือ
 VATT          Attributive verb                                       อ้วน, ดี, สวย
 XVBM          Pre-verb auxiliary, before negator "ไม่"                เกิด, เกือบ, กำลัง
 XVAM          Pre-verb auxiliary, after negator "ไม่"                 ค่อย, น่า, ได้
 XVMM          Pre-verb, before or after negator "ไม่"                 ควร, เคย, ต้อง
 XVBB          Pre-verb auxiliary, in imperative mood                 กรุณา, จง, เชิญ, อย่า, ห้าม
 XVAE          Post-verb auxiliary Å                                  ไป, มา, ขึ้น
 DDAN          | Definite determiner, after noun without              ยี่, นั่น, โน่น, ทั้งหมด
               | classifier in between
 DDAC          | Definite determiner, allowing classifier             นี้, นั้น, โน้น, นู้น
               | in between
 DDBQ          | Definite determiner, between noun and                ทั้ง, อีก, เพียง
               | classifier or preceding quantitative expression
 DDAQ          | Definite determiner,                                 พอดี, ถ้วน
               | following quantitative expression
 DIAC          | Indefinite determiner, following noun; allowing      ไหน, อื่น, ต่างๆ
               | classifier in between
 DIBQ          | Indefinite determiner, between noun and              บาง, ประมาณ, เกือบ
               | classifier or preceding quantitative expression
 DIAQ          | Indefinite determiner,                               กว่า, เศษ
               | following quantitative expression
 DCNM          Determiner, cardinal number expression                 **หนึ่ง**\ คน, เสือ, **2** ตัว
 DONM          Determiner, ordinal number expression                  ที่หนึ่ง, ที่สอง, ที่สุดท้สย
 ADVN          Adverb with normal form                                เก่ง, เร็ว, ช้า, สม่ำเสมอ
 ADVI          Adverb with iterative form                             เร็วๆ, เสทอๆ, ช้าๆ
 ADVP          Adverb with prefixed form                              โดยเร็ว
 ADVS          Sentential adverb                                      โดยปกติ, ธรรมดา
 CNIT          Unit classifier                                        ตัว, คน, เล่ม
 CLTV          Collective classifier                                  | คู่, กลุ่ม, ฝูง, เชิง, ทาง, 
                                                                      | ด้าน, แบบ, รุ่น
 CMTR          Measurement classifier                                 กิโลกรัม, แก้ว, ชั่วโมง
 CFQC          Frequency classifier                                   ครั้ง, เที่ยว
 CVBL          Verbal classifier                                      ม้วน, มัด
 JCRG          Coordinating conjunction                               และ, หรือ, แต่
 JCMP          Comparative conjunction                                กว่า, เหมือนกับ, เท่ากับ
 JSBR          Subordinating conjunction                              เพราะว่า, เนื่องจาก ที่, แม้ว่า, ถ้า
 RPRE          Preposition                                            จาก, ละ, ของ, ใต้, บน
 INT           Interjection                                           โอ้บ, โอ้, เออ, เอ๋, อ๋อ
 FIXN          Nominal prefix                                         **การ**\ ทำงาน, **ความ**\ สนุนสนาน
 FIXV          Adverbial prefix                                       **อย่าง**\ เร็ว
 EAFF          Ending for affirmative sentence                        จ๊ะ, จ้ะ, ค่ะ, ครับ, นะ, น่า, เถอะ
 EITT          Ending for interrogative sentence                      หรือ, เหรอ, ไหม, มั้ย
 NEG           Negator                                                ไม่, มิได้, ไม่ได้, มิ
 PUNC          Punctuation                                            (, ), “, ,, ;
============   =================================================      =================================

ORCHID corpus uses different set of POS tags. Thus, we make UD POS tags version for ORCHID corpus.

The following table shows the mapping of Part-of-Speech (POS) tags from ORCHID POS tags to UD POS tags:

===============     =======================
ORCHID POS tags     Coresponding UD POS tag
===============     =======================
NOUN                NOUN
NCMN                NOUN
NTTL                NOUN
CNIT                NOUN
CLTV                NOUN
CMTR                NOUN
CFQC                NOUN
CVBL                NOUN
VACT                VERB
VSTA                VERB
PROPN               PROPN
NPRP                PROPN
ADJ                 ADJ
NONM                ADJ
VATT                ADJ
DONM                ADJ
ADV                 ADV
ADVN                ADV
ADVI                ADV
ADVP                ADV
ADVS                ADV
INT                 INTJ
PRON                PRON
PPRS                PRON
PDMN                PRON
PNTR                PRON
DET                 DET
DDAN                DET
DDAC                DET
DDBQ                DET
DDAQ                DET
DIAC                DET
DIBQ                DET
DIAQ                DET
NUM                 NUM
NCNM                NUM
NLBL                NUM
DCNM                NUM
AUX                 AUX
XVBM                AUX
XVAM                AUX
XVMM                AUX
XVBB                AUX
XVAE                AUX
ADP                 ADP
RPRE                ADP
CCONJ               CCONJ
JCRG                CCONJ
SCONJ               SCONJ
PREL                SCONJ
JSBR                SCONJ
JCMP                SCONJ
PART                PART
FIXN                PART
FIXV                PART
EAFF                PART
EITT                PART
AITT                PART
NEG                 PART
PUNCT               PUNCT
PUNC                PUNCT
===============     =======================

For the NER, we use `Inside-outside-beggining (IOB) <https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)>`_ format to tag NER for each words.
For instance, given a sentence "บารัค โอบามาเป็นประธานธิปดี", it would be tag the tokens "บารัค", "โอบามา", "เป็น", "ประธานาธิปดี" as "B-PERSON", "I-PERSON", "I-PERSON", "O", and "O" respectively.

The *B-* prefix indicates begining token for a chunk of person name, "บารัค โอบามา" and *I-* prefix indicates the intermediate token. However, the term *O* indicates that a token not belong to any NER chunk.

The following table shows the list of Named Entity Recognition (NER) tags:

============================    =================================
Named Entity Recognition tag    Examples
============================    =================================
 DATE                           2/21/2004, 16 ก.พ., จันทร์
 TIME                           16.30 น., 5 วัน, 1-3 ปี
 EMAIL                          info@nrpsc.ac.th
 LEN                            30 กิโลเมตร, 5 กม.
 LOCATION                       ไทย, จ.ปราจีนบุรี, กำแพงเพชร
 ORGANIZATION                   กรมวิทยาศาสตร์การแพทย์, อย.
 PERSON                         น.พ.จรัล, นางประนอม ทองจันทร์
 PHONE                          1200, 0 2670 8888
 URL                            http://www.bangkokhealth.com/
 ZIP                            10400, 11130
 Money                          2.7 ล้านบาท, 2,000 บาท
 LAW                            พ.ร.บ.โรคระบาด พ.ศ.2499, รัฐธรรมนูญ                    
============================    =================================   

Modules
-------

.. autofunction:: pos_tag
.. autofunction:: pos_tag_sents
.. autofunction:: tag_provinces
.. autoclass:: pythainlp.tag.named_entity.ThaiNameTagger
   :members: get_ner

Tagger Engines
--------------

perceptron
++++++++++

Perceptron tagger is the part-of-speech tagging using the averaged, structured perceptron algorithm. 

unigram
+++++++

Unigram tagger doesn't take the ordering of words in the list into account.


References
----------

.. [#Sornlertlamvanich_2000] Takahashi, Naoto & Isahara, Hitoshi & Sornlertlamvanich, Virach. (2000).
            Building a Thai part-of-speech tagged corpus (ORCHID). 
            Journal of the Acoustical Society of Japan (E). 20. 10.1250/ast.20.189. 
