# -*- coding: utf-8 -*-
def vowel_list_clean(segmenteds):
    '''
    ใช้ clean สระ หลังการ tokenize\n
    vowel_list_clean(segmenteds)
    - segmenteds คือ list ของคำ
    '''
    output = []
    for segmented in segmenteds:
        segmented = vowel_replace(segmented)
        segmented = vowel_clean(segmented)
        output.append(segmented)
    return output

def vowel_clean(text):
    '''
    ใช้ clean สระ ก่อนการ tokenize\n
    vowel_clean(text)
    - text คือ string
    '''
    text = vowel_replace(text)
    text_cleaned = ''
    previous_chr = ''
    for chr in text:
        if not chr >= 'ฯ' and chr <= '์':
            text_cleaned = text_cleaned + chr
            previous_chr = chr
            continue
        if chr == previous_chr:
            continue
        text_cleaned = text_cleaned + chr
        previous_chr = chr
    return text_cleaned

def vowel_replace(text):
    '''
    ใช้ replace สระบางตัว เช่น สระเอ 2 ตัว ให้เป็นสระแอ\n
    vowel_replace(text)\n
    - text คือ string ที่ต้องการ replace สระ
    '''
    vowel_for_replaces = [['เเ', 'แ']]
    for mark in vowel_for_replaces:
        text = text.replace(mark[0], mark[1])
    return text