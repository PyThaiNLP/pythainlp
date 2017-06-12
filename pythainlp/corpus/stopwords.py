from __future__ import absolute_import,unicode_literals
import os
import codecs
import pythainlp
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'stopwords-th.txt')
"""
ข้อมูลตัวเก่า
def words(lang):
    '''
    stopword ภาษาไทย
    วิธีใช้
    from pythainlp.corpus import stopwords
    stopwords = stopwords.words('thai')
    '''
    words = {'thai' :
                 ["นี้", "นํา", "นั้น", "นัก", "นอกจาก", "ทุก", "ที่สุด", "ที่", "ทําให้", "ทํา", "ทาง", "ทั้งนี้",
                 "ดัง", "ซึ่ง", "ช่วง", "จาก", "จัด", "จะ", "คือ", "ความ", "ครั้ง", "คง", "ขึ้น", "ของ", "ขอ",
                 "รับ", "ระหว่าง", "รวม", "ยัง", "มี", "มาก", "มา", "พร้อม", "พบ", "ผ่าน", "ผล", "บาง", "น่า",
                 "เปิดเผย", "เปิด", "เนื่องจาก", "เดียวกัน", "เดียว", "เช่น", "เฉพาะ", "เข้า",
                 "ถ้า", "ถูก", "ถึง", "ต้อง", "ต่างๆ", "ต่าง", "ต่อ", "ตาม", "ตั้งแต่", "ตั้ง", "ด้าน", "ด้วย",
                 "อีก", "อาจ", "ออก", "อย่าง", "อะไร","อยู่", "อยาก", "หาก", "หลาย", "หลังจาก",
                 "แต่", "เอง", "เห็น", "เลย", "เริ่ม", "เรา", "เมื่อ", "เพื่อ", "เพราะ", "เป็นการ", "เป็น",
                 "หลัง", "หรือ", "หนึ่ง", "ส่วน", "ส่ง", "สุด", "สําหรับ", "ว่า", "ลง", "ร่วม", "ราย",
                 "ขณะ", "ก่อน", "ก็", "การ", "กับ", "กัน", "กว่า", "กล่าว", "จึง", "ไว้", "ไป", "ได้",
                 "ให้", "ใน", "โดย", "แห่ง", "แล้ว", "และ", "แรก", "แบบ", "ๆ"]
            }

    if lang == 'thai': return words['thai'] #ถ้า argument ที่ได้เป็น 'thai' ก็จะ return stopwords
"""
def words(lang):
    '''
    stopword ภาษาไทย
    วิธีใช้
    from pythainlp.corpus import stopwords
    stopwords = stopwords.words('thai')
    '''
    if lang == 'thai':
        with codecs.open(template_file, 'r',encoding='utf8') as f:
            lines = f.read().splitlines()
        return lines