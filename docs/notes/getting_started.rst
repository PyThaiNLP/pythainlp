Getting Started
=====================================
PyThaiNLP is a Python library for natural language processing (NLP) of Thai language. With this package, you can NLP tasks such as classify texts and tokenize words.

**Tokenization Example**::

    from pythainlp.tokenize import word_tokenize
    text='ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด'
    a=word_tokenize(text,engine='icu') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอ', 'เค', 'บ่', 'พวก', 'เรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้าน', 'เกิด']
    b=word_tokenize(text,engine='mm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
    c=word_tokenize(text,engine='pylexto') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
    d=word_tokenize(text,engine='newmm') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คนไทย', 'รัก', 'ภาษาไทย', 'ภาษา', 'บ้านเกิด']
    e=word_tokenize(text,engine='wordcutpy') # ['ผม', 'รัก', 'คุณ', 'นะ', 'ครับ', 'โอเค', 'บ่', 'พวกเรา', 'เป็น', 'คน', 'ไทย', 'รัก', 'ภาษา', 'ไทย', 'ภาษา', 'บ้านเกิ

Thai has historically faced a lot of NLP challenges. A quick list of them include as follows:

#. **Start-end of sentence marking** - This is arguably the biggest problem for the field of Thai NLP. The lack of end of sentence marking (EOS) makes it hard for researchers to create training sets, the basis of most research in this field. The root of the problem is two-pronged. In terms of writing system, Thai uses space to indicate both commas and periods. No letter indicates an end of a sentence. In terms of language use, Thais have a habit of starting their sentences with connector terms such as 'because', 'but', 'following', etc, making it often hard even for natives to decide where the end of sentence should be when translating.

#. **Word segmentation** - Thai does not use space and word segmentation is not easy. It boils down to understanding the context and ruling out words that do not make sense. This is a similar issue that other Asian languages such as Japanese and Chinese face in different degrees. For languages with space, a similar but less extreme problem would be multi-word expressions, like the French word for potato — 'pomme de terre'. In Thai, the best known example is "ตา-กลม" and "ตาก-ลม". As of recent, new techniques that capture words, subwords, and letters in vectors seem poised to overcome to issue.

**Example for classification**

https://colab.research.google.com/drive/1cnJ6O3b1jwaHwvsMWW3oQw7f8X2Ka7Sp



