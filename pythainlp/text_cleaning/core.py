"""
    text cleaning in  NLP
"""
from nlp import extract_tokens, insert_tokens
import re

"""
_____________________________________________________________________________
| ประเภทข้อมูล    | ตัวอย่างที่ต้องจัดการ                                            |
| ------------  | -------------------------------------------------------   |
| อักขระพิเศษ     |               !!!, ..., \~, ^\_^                          |
| อีโมจิ          |               😊, 😊, ^\_^                               |
| ตัวเลข         |                   3                                       |
| URL           | [https://example.com](https://example.com)               |
| Hashtag       | #เที่ยวไทย, #สนุกสุดๆ                                         |
| ตัวพิมพ์ใหญ่     | “สวัสดีค่ะ” → “สวัสดีค่ะ” (เปลี่ยนทั้งหมดเป็นพิมพ์เล็ก)                  |
| คำซ้ำ/คำยืด     | “มากกกกกก” → “มาก” หรือ “ดีมาก”                             |
| ช่องว่างเกิน      | (เช่นเว้นหลายช่อง)                                            |
| stopwords     | เช่น “แล้วก็”, “แบบว่า”, “คือ”                                 |
_____________________________________________________________________________

"""


test = """
    example 1 : 

      สวัสดีค่ะ!!! วันนี้อากาศดีมากๆๆ 😊😊  จะไปเที่ยวกับเพื่อนๆมา 3 คน ที่จังหวัดเชียงใหม่!!!  
      ลองเข้าไปดูรูปได้นะที่ https://facebook.com #เที่ยวไทย #สนุกสุดๆ  
      แล้วก็แบบว่า...คือมันดีมากกกกกก~   ขอบคุณค่ะ ^_^  
    """
"""
    example 2 :

    OMG!!! This is sooooo AMAZING!!! 😍😍😍 Check it out: https://wow.com/article/123
    I can't believe it..... @john_doe was right all along!!! 😂😂😂
    Go to https://example.com RIGHT NOW!!! You won't regret it. #unbelievable #wowww
    Sooooo goooooddddddd.... I'm in loooooveeee 💕💕💕
    Visit www.testsite.org to learn more. This is just... WOW!!! 😱😱

"""

thai_special_chars_unicode = {
    "ๆ": "\u0E46",
    "ฯ": "\u0E2F",
    "ฯลฯ": "\u0E2Fล\u0E2F",
    "๏": "\u0E4F",
    "๛": "\u0E5B",
    "๚": "\u0E5A",
    "๚ะ": "\u0E5Aะ",
}

emoji_sentiment = {
    "positive": [
        "😊", "😁", "😂", "🤣", "😄", "😍", "😘", "😻", "👍", "👏", "💕", "❤️", "😇", "😎", "🥰", "😃", "☺️"
    ],

    "negative": [
        "😢", "😭", "😠", "😡", "😤", "👎", "💔", "😞", "😖", "😩", "😣", "😫", "😓", "😰", "😱", "😿"
    ],

    "neutral": [
        "😐", "😶", "🤔", "😑", "😬", "😴", "😕", "😒", "🙄", "😮", "🤨", "😲"
    ]
}

def replace_emoji_with_sentiment(sentence: str, emoji_dict: dict) -> str:
    for emo in emoji_dict["positive"]:
        sentence = sentence.replace(emo, " <<EMO_POS>> ")
    for emo in emoji_dict["negative"]:
        sentence = sentence.replace(emo, " <<EMO_NEG>> ")
    for emo in emoji_dict["neutral"]:
        sentence = sentence.replace(emo, " <<EMO_NEU>> ")
    return sentence

def remove_thai_special_chars(text: str, pattern : str) -> str:
    return re.sub(pattern, '', text)

def normalize_text(
    text: str,
    emoji_dict: dict = None,
    url_mode: str = "token",  # "token", "keep", "remove"
    replace_url_token: str = "<<URL>>"
) -> str:
    import re

    def extract_tokens(text: str) -> tuple[str, list[str]]:
        pattern = r'<<[^<>]+>>'
        tokens = re.findall(pattern, text)
        text_wo_tokens = re.sub(pattern, '', text)
        return text_wo_tokens, tokens

    def insert_tokens(text: str, tokens: list[str]) -> str:
        return (text + ' ' + ' '.join(tokens)).strip()

    text = text.lower()

    url_pattern = r'https?://\S+|www\.\S+'

    if url_mode == "token":
        text = re.sub(url_pattern, replace_url_token, text)
    elif url_mode == "remove":
        text = re.sub(url_pattern, '', text)

    text = re.sub(r'@\w+', '<<MENTION>>', text)
    text = re.sub(r'#([\wก-๙]+)', r'<<HASHTAG_\1>>', text)

    # Emoji → Sentiment token
    if emoji_dict:
        text = replace_emoji_with_sentiment(sentence=text, emoji_dict=emoji_dict)

    # แยก token ก่อน clean
    text_wo_tokens, tokens = extract_tokens(text)

    # Clean ส่วนที่ไม่ใช่ token
    text_wo_tokens = re.sub(r'[^\w\sก-๙.:/]', '', text_wo_tokens)

    # ลบอักขระพิเศษเฉพาะไทย
    th_special_chars_to_remove = [k for k in thai_special_chars_unicode if len(k) == 1 and k != 'ะ']
    pattern = '[' + ''.join(re.escape(c) for c in th_special_chars_to_remove) + ']'
    text_wo_tokens = re.sub(pattern, '', text_wo_tokens)

    # Normalize คำยืด
    text_wo_tokens = re.sub(r'(.)\1{2,}', r'\1\1', text_wo_tokens)
    text_wo_tokens = re.sub(r'\s+', ' ', text_wo_tokens).strip()

    return insert_tokens(text_wo_tokens, tokens)

print("Original")
print(test)

print("แบบเก็บ URL เต็ม:")
print(normalize_text(test, emoji_dict=emoji_sentiment, url_mode="keep"))

print("แบบแปลงเป็น <<URL>>:")
print(normalize_text(test, emoji_dict=emoji_sentiment, url_mode="token"))

print("แบบลบ URL ทิ้ง:")
print(normalize_text(test, emoji_dict=emoji_sentiment, url_mode="remove"))
