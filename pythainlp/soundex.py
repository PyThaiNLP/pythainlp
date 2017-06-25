'''
Thai soundex

โค้ดพัฒนาโดย คุณ Korakot Chaovavanich (จาก https://gist.github.com/korakot/0b772e09340cac2f493868da035597e8)
'''
import re
def LK82(s):
    '''
    LK82 - กฎการเข้ารหัสซาวน์เด็กซ์ของ  วิชิตหล่อจีระชุณห์กุล  และ  เจริญ  คุวินทร์พันธุ์
    LK82(str)
    '''
    t1 = str.maketrans("กขฃคฅฆงจฉชฌซศษสญยฎดฏตณนฐฑฒถทธบปผพภฝฟมรลฬฤฦวหฮอ","กกกกกกงจชชชซซซซยยดดตตนนททททททบปพพพฟฟมรรรรรวหหอ")
    t2 = str.maketrans("กขฃคฅฆงจฉชซฌฎฏฐฑฒดตถทธศษสญณนรลฬฤฦบปพฟภผฝมำยวไใหฮาๅึืเแโุูอ","1111112333333333333333333444444445555555667777889AAABCDEEF")
    res = []
    s = re.sub("[่-๋]", "", s)  # 4.ลบวรรณยุกต์
    if re.search("[ก-ฮ][ิุู]?์",s):
        # 4.ลบการันต์
        # เนื่องจากภาษาไทยมีตัวการ์รันต์ เช่น ตร์ ทร์  ดร์ อยู่ด้วย จึงต้องเอาออกไปด้วย
        if re.search("ตร์",s):
            s = re.sub("ตร์","",s)
        elif re.search("ทร์",s):
            s = re.sub("ทร์","",s)
        elif re.search("ดร์",s):
            s = re.sub("ทร์","",s)
        else:
            s = re.sub("[ก-ฮ][ิุู]?์", "", s)
    s = re.sub("[็ํฺๆฯ]", "", s)  # 5.ทิ้งไม้ไต่คู่ ฯลฯ
    # 6.เข้ารหัสตัวแรก
    if 'ก'<=s[0]<='ฮ':
        res.append(s[0].translate(t1))
        s = s[1:]
    else:
        s = s[1:]
        res.append(s[0].translate(t2))
        s = s[2:]
    # เข้ารหัสตัวที่เหลือ
    i_v = None # ตำแหน่งตัวคั่นล่าสุด (สระ)
    for i,c in enumerate(s):
        if c in "ะัิี": # 7. ตัวคั่นเฉยๆ
            i_v = i
            res.append('')
        elif c in "าๅึืู": # 8.คั่นและใส่
            i_v = i
            res.append(c.translate(t2))
        elif c == 'ุ': # 9.สระอุ
            i_v = i
            if i==0 or (s[i-1] not in "ตธ"):
                res.append(c.translate(t2))
            else:
                res.append('')
        elif c in 'หอ':
            if i+1<len(c) and (c[i+1] in "ึืุู"):
                res.append(c.translate(t2))
        elif c in 'รวยฤฦ':
            if i_v == i-1 or (i+1<len(c) and (c[i+1] in "ึืุู")):
                res.append(c.translate(t2))
        else:
            res.append(c.translate(t2)) # 12.
    # 13. เอาตัวซ้ำออก
    res2 = [res[0]]
    for i in range(1, len(res)):
        if res[i] != res[i-1]:
            res2.append(res[i])
    # 14. เติมศูนย์ให้ครบ ถ้าเกินก็ตัด
    return ("".join(res2)+"0000")[:5]

if __name__ == '__main__':
    print(LK82('รถ'))
    print(LK82('รส'))
    print(LK82('รด'))
    print(LK82('จัน'))
    print(LK82('จันทร์'))