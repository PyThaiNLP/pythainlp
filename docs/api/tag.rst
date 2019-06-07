.. currentmodule:: pythainlp.tag

pythainlp.tag
=====================================
The :class:`pythainlp.tag` contains functions that are used to tag different parts of a text including 
Part-of-Speech (POS) tags, and Named Entity Recognition (NER) tag.


The following table shows the list of Part-of-Speech (POS) tags:

============   ==========================   =============================
Abbreviation   Part-of-Speech tag           Examples                     
============   ==========================   =============================
 ADJ           Adjective                    ใหม่, พิเศษ , ก่อน, มาก, สูง    
 ADP           Adposition                   แม้, ว่า, เมื่อ, ของ, สำหรับ     
 ADV           Adverb                       ก่อน, ก็, เล็กน้อย, เลย, สุด     
 AUX           Auxilisary                   เป็น, ใช่, คือ, คล้าย           
 CCONJ         Coordinating conjunction     แต่, และ, หรือ                
 DET           Determiner                   ที่, นี้, ซึ่ง, ทั้ง, ทุก, หลาย      
 NOUN          Nounn                        กำมือ, พวก, สนาม, กีฬา, บัญชี  
 NUM           Numeral                      5,000, 103.7, 2004, หนึ่ง, ร้อย
 PART          Particle                     มา ขึ้น ไม่ ได้ เข้า             
 PRON          Pronoun                      เรา, เขา, ตัวเอง, ใคร, เธอ  
 PROPN         Proper noun                  โอบามา, แคปิตอลฮิล, จีโอพี, ไมเคิล
 PUNCT         Punctuation                  (, ), ", ', :               
 SCONJ         Subordinating conjunction    หาก                         
 VERB          Verb                         เปิด, ให้, ใช้, เผชิญ, อ่าน      
============   ==========================   =============================


For the NER, we use `Inside-outside-beggining (IOB) <https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)>` format to tag NER for each words.
For instance, given a sentence "บารัค โอบามาเป็นประธานธิปดี", it would be tag the tokens "บารัค", " ", "โอบามา", "เป็น", "ประธานาธิปดี" as "B-PERSON", "I-PERSON", "I-PERSON", "O", and "O" respectively.
The B- prefix indicates begining token for a chunk of person name, "บารัค โอบามา" and I- prefix indicates the intermediate token. However, the term 'O' indicates that a token not belong to any NER chunk.

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
=============================   =================================   

Modules
-------

.. autofunction:: pos_tag
.. autofunction:: pos_tag_sents
.. autofunction:: tag_provinces
.. autoclass:: pythainlp.tag.named_entity.ThaiNameTagger
   :members: get_ner
