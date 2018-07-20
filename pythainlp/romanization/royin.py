# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from __future__ import unicode_literals
from __future__ import print_function
import re
import copy
vowel_data_py3 = """เ*ียว,\\1iao
แ*็ว,\\1aeo
เ*ือย,\\1ueai
แ*ว,\\1aeo
เ*็ว,\\1eo
เ*ว,\\1eo
*ิว,\\1io
*วย,\\1uai
เ*ย,\\1oei
*อย,\\1oi
โ*ย,\\1oi
*ุย,\\1ui
*าย,\\1ai
ไ*ย,\\1ai
*ัย,\\1ai
ไ*,\\1ai
ใ*,\\1ai
*ว*,\\1ua\\2
*ัวะ,\\1ua
*ัว,\\1ua
เ*ือะ,\\1uea
เ*ือ,\\1uea
เ*ียะ,\\1ia
เ*ีย,\\1ia
เ*อะ,\\1oe
เ*อ,\\1oe
เ*ิ,\\1oe
*อ,\\1o
เ*าะ,\\1o
เ*็,\\1e
โ*ะ,\\1o
โ*,\\1o
แ*ะ,\\1ae
แ*,\\1ae
เ*าะ,\\1e
*าว,\\1ao
เ*า,\\1ao
เ*,\\1e
*ู,\\1u
*ุ,\\1u
*ื,\\1ue
*ึ,\\1ue
*ี,\\1i
*ิ,\\1i
*ำ,\\1am
*า,\\1a
*ั,\\1a
*ะ,\\1a
#ฤ,\\1rue
$ฤ,\\1ri"""
vowel_data = vowel_data_py3.replace('*', '([ก-ฮ])')
vowel_data = vowel_data.replace('#', '([คนพมห])')
vowel_data = vowel_data.replace('$', '([กตทปศส])')
reader = [x.split(',') for x in vowel_data.split('\n')]


def delete(data):
    # ลบตัวการันต์
    data = re.sub('จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์', "", data)
    data = re.sub("[ๆฯ]", "", data)
    '''โค้ดส่วนตัดวรรณยุกต์ออก'''
    # ลบวรรณยุกต์
    data = re.sub("[่-๋]", "", data)
    if re.search(u'\w'+'์', data, re.U):
        search = re.findall(u'\w'+'์', data, re.U)
        for i in search:
                data = re.sub(i, '', data, flags=re.U)
    return data
# พยัญชนะ ต้น สะกด
consonants_data = {
    'ก': ['k', 'k'],
    'ข': ['kh', 'k'],
    'ฃ': ['kh', 'k'],
    'ค': ['kh', 'k'],
    'ฅ': ['kh', 'k'],
    'ฆ': ['kh', 'k'],
    'ง': ['ng', 'ng'],
    'จ': ['ch', 't'],
    'ฉ': ['ch', 't'],
    'ช': ['ch', 't'],
    'ซ': ['s', 't'],
    'ฌ': ['ch', 't'],
    'ญ': ['y', 'n'],
    'ฎ': ['d', 't'],
    'ฏ': ['t', 't'],
    'ฐ': ['th', 't'],
    # ฑ พยัญชนะต้น เป็น d ได้
    'ฑ': ['th', 't'],
    'ฒ': ['th', 't'],
    'ณ': ['n', 'n'],
    'ด': ['d', 't'],
    'ต': ['t', 't'],
    'ถ': ['th', 't'],
    'ท': ['th', 't'],
    'ธ': ['th', 't'],
    'น': ['n', 'n'],
    'บ': ['b', 'p'],
    'ป': ['p', 'p'],
    'ผ': ['ph', 'p'],
    'ฝ': ['f', 'p'],
    'พ': ['ph', 'p'],
    'ฟ': ['f', 'p'],
    'ภ': ['ph', 'p'],
    'ม': ['m', 'm'],
    'ย': ['y', ''],
    'ร': ['r', 'n'],
    'ฤ': ['rue', ''],
    'ล': ['l', 'n'],
    'ว': ['w', ''],
    'ศ': ['s', 't'],
    'ษ': ['s', 't'],
    'ส': ['s', 't'],
    'ห': ['h', ''],
    'ฬ': ['l', 'n'],
    'อ': ['', ''],
    'ฮ': ['h', '']
}


def vowel(word):
    i = 0
    while i < len(reader):
        word = re.sub(reader[i][0], reader[i][1], word)
        i += 1
    return word


def consonants(word, res):
    if res is None:
        pass
    elif len(res) == 1:
        word = word.replace(res[0], consonants_data[res[0]][0])
    else:
        i = 0
        lenword = len(res)
        while i < lenword:
            if i == 0 and res[0] == "ห":
                word = word.replace(res[0], consonants_data[res[0]][0])
                i += 1
            elif i == 0 and res[0] != "ห":
                word = word.replace(res[0], consonants_data[res[0]][0])
                i += 1
            elif res[i] == "ร" and (word[i] == "ร" and len(word) == i+1):
                word = word.replace(res[i], consonants_data[res[i]][1])
            elif res[i] == "ร" and (word[i] == "ร" and word[i+1] == "ร"):
                word = list(word)
                del word[i+1]
                if i+2 == lenword:
                    word[i] = "an"
                else:
                    word[i] = "a"
                word = "".join(word)
                i += 1
            else:
                word = word.replace(res[i], consonants_data[res[i]][1])
                i += 1
    return word


def romanization(word):
    pattern = re.compile(r"[ก-ฮ]", re.U)
    word2 = vowel(delete(word))
    res = re.findall(pattern, word2)
    if len(word2) == 2 and len(res) == 2:
        word2 = list(word2)
        word2.insert(1, 'o')
        word2 = ''.join(word2)
    word2 = consonants(word2, res)
    return word2
if __name__ == "__main__":
    print(romanization("แมว") == "maeo")
    print(romanization("น้าว") == "nao")
    print(romanization("รวม") == "ruam")
    print(romanization("ไทย") == "thai")
    print(romanization("ผัวะ") == "phua")
    print(romanization("ใย") == "yai")
    print(romanization("ไล่") == "lai")
    print(romanization("เมา") == "mao")
    print(romanization("ต้น") == "ton")
    print(romanization("ตาล") == "tan")
    print(romanization("แสง") == "saeng")
    print(romanization("เลียน") == "lian")
    print(romanization("เลือก") == "lueak")
    print(romanization("เธอ") == "thoe")
    print(romanization("หรู") == "ru")
    print(romanization("ลอม") == "lom")
    print(romanization("และ") == "lae")
    print(romanization("เลาะ") == "lo")
    print(romanization("ลอม") == "lom")
    print(romanization("เล็ง") == "leng")
    print(romanization("นึก") == "nuek")
    print(romanization("มัว") == "mua")
    print(romanization("มีด") == "mit")
    print(romanization("โค") == "kho")
    print(romanization("ขอ") == "kho")
    print(romanization("วรร") == "wan")
    print(romanization("สรรพ") == "sap")
    print(romanization('วัน') + romanization('นะ') + romanization('พง'))
    print(romanization('นัด') + romanization('ชะ') + romanization('โนน'))
    print(romanization('สรรพ'))
    print(romanization('สรร') + romanization('หา'))
    print(romanization('สรร') + romanization('หา'))
    print(romanization('แมว'))
    print(romanization('กร') == romanization('กอน'))
    print(romanization('คฤ') + romanization('หาสน์'))
    print(romanization('กฤ') + romanization('ศะ') + romanization('ฎา'))
    print(romanization('ฤกษ์'))
    print(romanization('ฤ')+romanization('ดู')+romanization('กาล'))
