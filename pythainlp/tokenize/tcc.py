'''
โปรแกรม TCC ใน Python

พัฒนาโดย นาย วรรณพงษ์  ภัททิยไพบูลย์

19 มิ.ย. 2560

วิธีใช้งาน
tcc(คำ)
คืนค่า โดยมี / แบ่งกลุ่มคำ
'''
import re
C=['ก','ข','ฃ','ค','ฅ','ฆ','ง','จ','ฉ','ช','ฌ','ซ','ศ','ษ','ส','ญ','ฎ','ฑ','ด','ฏ','ต','ฐ','ฑ','ฒ','ถ','ท','ธ','ณ','น','บ','ป','ผ','พ','ภ','ฝ','ฟ','ม','ย','ร','ล','ฬ','ว','ห','ฮ']
UV=['ิ','ี','ึ','ื','ั','็','่','้','๊','๋']
LV=['ุ','ู']
FV=['เ','แ','โ','ใ','ไ']
RV=['ะ','า','ำ']
def rulestcc(r1,r2,data):
    rules='['+''.join(r1)+']'+'['+''.join(r2)+']'
    if (re.search(rules,data,re.U)):
        search=re.findall(rules,data,re.U)
        for i in search:
            data=re.sub(i, '/'+i+'/', data)
    return data
def tcc(text):
    '''
    วิธีใช้งาน
    tcc(คำ)
    คืนค่า โดยมี / แบ่งกลุ่มคำ
    '''
    text=rulestcc(C,RV,text)
    text=rulestcc(FV,C,text)
    text=rulestcc(C,UV,text)
    text=rulestcc(C,LV,text)
    return re.sub('//','/',text)
if __name__ == '__main__':
    print(tcc('แมวกิน'))
    print(tcc('ประชาชน'))
    print(tcc('ขุด')+'/'+tcc('หลุม'))
    print(tcc('ยินดี'))