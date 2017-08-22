# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
'''
โมดูลถอดเสียงไทยเป็นอังกฤษ

พัฒนาต่อจาก new-thai.py

พัฒนาโดย นาย วรรณพงษ์ ภัททิยไพบูลย์

เริ่มพัฒนา 20 มิ.ย. 2560
'''
from pythainlp.tokenize import word_tokenize
from pythainlp.tokenize import tcc
#from pythainlp.tokenize import etcc
import re
consonants = { # พยัญชนะ ต้น สะกด
'ก':['k','k'],
'ข':['kh','k'],
'ฃ':['kh','k'],
'ค':['kh','k'],
'ฅ':['kh','k'],
'ฆ':['kh','k'],
'ง':['ng','ng'],
'จ':['ch','t'],
'ฉ':['ch','t'],
'ช':['ch','t'],
'ซ':['s','t'],
'ฌ':['ch','t'],
'ญ':['y','n'],
'ฎ':['d','t'],
'ฏ':['t','t'],
'ฐ':['th','t'],
'ฑ':['th','t'], #* พยัญชนะต้น เป็น d ได้
'ฒ':['th','t'],
'ณ':['n','n'],
'ด':['d','t'],
'ต':['t','t'],
'ถ':['th','t'],
'ท':['th','t'],
'ธ':['th','t'],
'น':['n','n'],
'บ':['b','p'],
'ป':['p','p'],
'ผ':['ph','p'],
'ฝ':['f','p'],
'พ':['ph','p'],
'ฟ':['f','p'],
'ภ':['ph','p'],
'ม':['m','m'],
'ย':['y',''],
'ร':['r','n'],
'ล':['l','n'],
'ว':['w',''],
'ศ':['s','t'],
'ษ':['s','t'],
'ส':['s','t'],
'ห':['h',''],
'ฬ':['l','n'],
'อ':['',''],
'ฮ':['h','']
}
consonants_thai= u'[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬฮ]'
def deletetone(data):
	'''โค้ดส่วนตัดวรรณยุกต์ออก'''
	for tone in ['่','้','๊','๋']:
		if (re.search(tone,data)):
				data = re.sub(tone,'',data)
	if re.search(u'\w'+'์',data, re.U):
		search=re.findall(u'\w'+'์',data, re.U)
		for i in search:
				data=re.sub(i,'',data,flags=re.U)
	return data
def romanization(text):
    '''
    romanization(str)
    '''
    text=deletetone(text)
    text1=word_tokenize(text,engine='newmm')
    textdata=[]
    #print(text1)
    for text in text1:
        #a1=etcc.etcc(text)
        a2=tcc.tcc(text)
        text=re.sub('//','/',a2)
        if re.search(u'เ\w'+'ี'+'ย/ว',text, re.U):
            '''
            จัดการกับ เอียว
            '''
            #print('เอียว')
            search=re.findall(u'เ\w'+'ี'+'ย/ว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'iao',text,flags=re.U)

        if re.search(u'แ\w'+'็'+'ว',text, re.U):
            '''
            จัดการกับ แอ็ว
            '''
            #print('แอ็ว')
            search=re.findall(u'แ\w'+'็'+'ว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'aeo',text,flags=re.U)
        if re.search(u'แ\w/\w'+'็/'+'ว',text, re.U):
            '''
            จัดการกับ แออ็ว
            '''
            #print('แออ็ว')
            search=re.findall(u'แ\w/\w'+'็/'+'ว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+list(i)[3]+'aeo',text,flags=re.U)
        if re.search(u'แ\w/'+'ว',text, re.U):
            '''
            จัดการกับ แอว
            '''
            #print('แอว')
            search=re.findall(u'แ\w/'+'ว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'aeo',text,flags=re.U)
        if re.search(u'เ\w/ว',text, re.U):
            '''
            จัดการกับ เอว
            '''
            #print('เอว')
            search=re.findall(u'เ\w/ว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'eo',text,flags=re.U)
        if re.search(u'เ\w็ว',text, re.U):
            '''
            จัดการกับ เอ็ว
            '''
            #print('เอ็ว')
            search=re.findall(u'เ\w็ว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'eo',text,flags=re.U)
        if re.search(u'เ\wียะ',text, re.U):
            '''
            จัดการกับ เอียะ
            '''
            #print('เอียะ')
            search=re.findall(u'เ\wียะ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ia',text,flags=re.U)
        if re.search(u'เ\wีย',text, re.U):
            '''
            จัดการกับ เอีย (1)
            '''
            #print('เอีย 1')
            search=re.findall(u'เ\wีย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ia',text,flags=re.U)
        if re.search(u'เ\w/ีย',text, re.U):
            '''
            จัดการกับ เอีย (2)
            '''
            #print('เอีย 2')
            search=re.findall(u'เ\w/ีย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ia',text,flags=re.U)
        if re.search(u'เ\wือ/ย',text, re.U):
            '''
            จัดการกับ เอือย
            '''
            #print('เอือย')
            search=re.findall(u'เ\wือ/ย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ueai',text,flags=re.U)
        if re.search(u'เ\wือะ',text, re.U):
            '''
            จัดการกับ เอือะ
            '''
            #print('เอือะ')
            search=re.findall(u'เ\wือะ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'uea',text,flags=re.U)
        if re.search(u'เ\wือ',text, re.U):
            '''
            จัดการกับ เอือ
            '''
            #print('เอือ')
            search=re.findall(u'เ\wือ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'uea',text,flags=re.U)
        if re.search(u'โ\w/ย',text, re.U):
            '''
            จัดการกับ โอย
            '''
            #print('โอย')
            search=re.findall(u'โ\w/ย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'oi',text,flags=re.U)
        if re.search(u'\w/อ/ย',text, re.U):
            '''
            จัดการกับ ออย
            '''
            #print('ออย')
            search=re.findall(u'\w/อ/ย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'oi',text,flags=re.U)
        if re.search(u'โ\wะ',text, re.U):
            '''
            จัดการกับ โอะ
            '''
            #print('โอะ')
            search=re.findall(u'โ\wะ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'o',text,flags=re.U)
        if re.search(u'โ\w',text, re.U):
            '''
            จัดการกับ โอ
            '''
            #print('โอ')
            search=re.findall(u'โ\w',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'o',text,flags=re.U)
        if re.search(u'เ/\wา/ะ/',text, re.U):
            '''
            จัดการกับ เอาะ (1)
            '''
            #print('เอาะ 1')
            search=re.findall(u'เ/\wา/ะ/',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[2]+'o',text,flags=re.U)
        if re.search(u'เ\wาะ',text, re.U):
            '''
            จัดการกับ เอาะ (2)
            '''
            #print('เอาะ 2')
            search=re.findall(u'เ\wาะ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'o',text,flags=re.U)
        if re.search(u'อำ',text, re.U):
            '''
            จัดการกับ อำ
            '''
            #print('อำ')
            search=re.findall(u'อำ',text, re.U)
            for i in search:
                text=re.sub(i,'am',text,flags=re.U)
        if re.search(u'อี',text, re.U):
            '''
            จัดการกับ อี
            '''
            #print('"อี"')
            search=re.findall(u'อี',text, re.U)
            for i in search:
                text=re.sub(i,'i',text,flags=re.U)
        # เออ
        if re.search(u'เ\w/อ',text, re.U):
            '''
            จัดการกับ เออ
            '''
            #print('เออ')
            search=re.findall(u'เ\w/อ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'oe',text,flags=re.U)
        if re.search(u'\w/อ',text, re.U):
            '''
            จัดการกับ ออ
            '''
            #print('ออ')
            search=re.findall(u'\w/อ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'o',text,flags=re.U)
        if re.search(u'\wัวะ',text, re.U):
            '''
            จัดการกับ อัวะ
            '''
            #print('อัวะ')
            search=re.findall(u'\wัวะ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ua',text,flags=re.U)
        if re.search(u'\wัว',text, re.U):
            '''
            จัดการกับ อัว
            '''
            #print('อัว')
            search=re.findall(u'\wัว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ua',text,flags=re.U)
        # ใอ,อัย , อาย
        if re.search(u'ใ\w',text, re.U):
            '''
            จัดการกับ ใอ
            '''
            #print('ใอ')
            search=re.findall(u'ใ\w',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ai',text,flags=re.U)
        if re.search(u'\wัย',text, re.U):
            '''
            จัดการกับ อัย
            '''
            #print('อัย')
            search=re.findall(u'\wัย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ai',text,flags=re.U)
        if re.search(u'\wา/ย',text, re.U):
            '''
            จัดการกับ อาย
            '''
            #print('อาย')
            search=re.findall(u'\wา/ย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ai',text,flags=re.U)
        #เอา, อาว
        if re.search(u'เ\wา',text, re.U):
            '''
            จัดการกับ เอา
            '''
            #print('เอา')
            search=re.findall(u'เ\wา',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ao',text,flags=re.U)
        if re.search(u'\wา/ว',text, re.U):
            '''
            จัดการกับ อาว
            '''
            #print('อาว')
            search=re.findall(u'\wา/ว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ao',text,flags=re.U)
        #อุย
        if re.search(u'\wุ/ย',text, re.U):
            '''
            จัดการกับ อุย
            '''
            #print('อุย')
            search=re.findall(u'\wุ/ย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ui',text,flags=re.U)
        #เอย
        if re.search(u'เ\w/ย',text, re.U):
            '''
            จัดการกับ เอย
            '''
            #print('เอย')
            search=re.findall(u'เ\w/ย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'oei',text,flags=re.U)
        # แอะ, แอ
        if re.search(u'แ\wะ',text, re.U):
            '''
            จัดการกับ แอะ
            '''
            #print('แอะ')
            search=re.findall(u'แ\wะ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ae',text,flags=re.U)
        if re.search(u'แ\w',text, re.U):
            '''
            จัดการกับ แอ
            '''
            #print('แอ')
            search=re.findall(u'แ\w',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ae',text,flags=re.U)
        # เอะ
        if re.search(u'เ\wะ',text, re.U):
            '''
            จัดการกับ เอะ
            '''
            #print('เอะ')
            search=re.findall(u'เ\wะ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'e',text,flags=re.U)
        # อิว
        if re.search(u'\wิ/ว',text, re.U):
            '''
            จัดการกับ อิว
            '''
            #print('อิว')
            search=re.findall(u'\wิ/ว',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'io',text,flags=re.U)
        # อวย
        if re.search(u'\w/ว/ย',text, re.U):
            '''
            จัดการกับ อวย
            '''
            #print('อวย')
            search=re.findall(u'\w/ว/ย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'uai',text,flags=re.U)
        # -ว-
        if re.search(u'\w/ว/\w',text, re.U):
            '''
            จัดการกับ -ว-
            '''
            #print('-ว-')
            search=re.findall(u'\w/ว/\w',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ua'+list(i)[4],text,flags=re.U)
        # เ–็,เอ
        if re.search(u'เ\w'+'็',text, re.U):
            '''
            จัดการกับ เ–็
            '''
            #print('เ–็')
            search=re.findall(u'เ\w'+'็',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'e',text,flags=re.U)
        if re.search(u'เ\w/',text, re.U):
            '''
            จัดการกับ เอ
            '''
            #print('เอ')
            search=re.findall(u'เ\w/',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'e',text,flags=re.U)
        #ไอย
        if re.search(u'ไ\w/ย',text, re.U):
            '''
            จัดการกับ ไอย
            '''
            #print('ไอย')
            search=re.findall(u'ไ\w/ย',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ai',text,flags=re.U)
        #ไอ
        if re.search(u'ไ\w',text, re.U):
            '''
            จัดการกับ ไอ
            '''
            #print('ไอ')
            search=re.findall(u'ไ\w',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[1]+'ai',text,flags=re.U)
        #อะ
        if re.search(u'\wะ',text, re.U):
            '''
            จัดการกับ อะ
            '''
            #print('อะ')
            search=re.findall(u'\wะ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'a',text,flags=re.U)
        # –ั
        if re.search(u'\wั',text, re.U):
            '''
            จัดการกับ –ั
            '''
            #print('–ั ')
            search=re.findall(u'\wั',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'a',text,flags=re.U)
        # รร
        if re.search(u'\w/ร/ร/\w[^ก-ฮ]',text, re.U):
            '''
            จัดการกับ -รร-
            '''
            #print('-รร- 1')
            search=re.findall(u'\w/ร/ร/\w[^ก-ฮ]',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'an'+list(i)[6]+list(i)[7],text,flags=re.U)
        if re.search(u'\w/ร/ร/',text, re.U):
            '''
            จัดการกับ -รร-
            '''
            #print('-รร- 2')
            search=re.findall(u'\w/ร/ร/',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'a',text,flags=re.U)
        #อา
        if re.search(u'อา',text, re.U):
            '''
            จัดการกับ อา 1
            '''
            #print('อา 1')
            search=re.findall(u'อา',text, re.U)
            for i in search:
                text=re.sub(i,'a',text,flags=re.U)
        if re.search(u'\wา',text, re.U):
            '''
            จัดการกับ อา 2
            '''
            #print('อา 2')
            search=re.findall(u'\wา',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'a',text,flags=re.U)
                #อำ
        if re.search(u'\wำ',text, re.U):
            '''
            จัดการกับ อำ 1
            '''
            #print('อำ 1')
            search=re.findall(u'\wำ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'am',text,flags=re.U)
        #อิ , อี
        if re.search(u'\wิ',text, re.U):
            '''
            จัดการกับ อิ
            '''
            #print('อิ')
            search=re.findall(u'\wิ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'i'+'/',text,flags=re.U)
        if re.search(u'\wี',text, re.U):
            '''
            จัดการกับ อี
            '''
            #print('อี')
            search=re.findall(u'\wี',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'i'+'/',text,flags=re.U)
        #อึ , อื
        if re.search(u'\wึ',text, re.U):
            '''
            จัดการกับ อึ
            '''
            #print('อึ')
            search=re.findall(u'\wึ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ue'+'/',text,flags=re.U)
        if re.search(u'\wื',text, re.U):
            '''
            จัดการกับ อื
            '''
            #print('อื')
            search=re.findall(u'\wื',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'ue'+'/',text,flags=re.U)
        #อุ , อู
        if re.search(u'\wุ',text, re.U):
            '''
            จัดการกับ อุ
            '''
            #print('อุ')
            search=re.findall(u'\wุ',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'u'+'/',text,flags=re.U)
        if re.search(u'\wู',text, re.U):
            '''
            จัดการกับ อู
            '''
            #print('อู')
            search=re.findall(u'\wู',text, re.U)
            for i in search:
                text=re.sub(i,list(i)[0]+'u'+'/',text,flags=re.U)
        if re.search(r'[^กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬฮ]',text, re.U):
            '''
             ใช้ในกรณีคำนั้นมีสระด้วย จะได้เอาพยัญชนะตัวแรกไปเทียบ
            '''
            d=re.search(consonants_thai,text,re.U)
            text=re.sub(d.group(0),consonants[d.group(0)][0],text,flags=re.U)
        listtext=list(text)
        #print(listtext,0)
        if re.search(consonants_thai,listtext[0], re.U):
	        '''
	        จัดการกับพยัญชนะต้น
	        '''
	        listtext[0]=consonants[listtext[0]][0]
	        two=False
	        #print(listtext,1)
	        if len(listtext)==2:
		        if  re.search(consonants_thai,listtext[1], re.U):
			        '''
			        จัดการกับพยัญชนะ 2 ตัว และมีแค่ 2 ตั   และมีแค่ 2 ตัวติดกันในคำ
			        '''
			        listtext.append(consonants[listtext[1]][1])
			        listtext[1]='o'
			        two=True
        elif (len(listtext)==3 and listtext[1]=='/'):
	        #print(listtext,2)
	        if re.search(consonants_thai,listtext[2], re.U) and re.search(r'[ก-ฮ]',listtext[2], re.U):
		        '''
		        กร
		        ผ่าน tcc เป็น ก/ร แก้ไขในกรณีนี้
		        '''
		        listtext[1]='o'
		        listtext[2]=consonants[listtext[2]][1]
		        two=True
        else:
	        two=False
        i=0
        while i<len(listtext) and two==False:
	        if re.search(consonants_thai,listtext[i], re.U):
		        '''
		        ถ้าหากเป็นพยัญชนะ
		        '''
		        listtext[i]=consonants[listtext[i]][1]
	        i+=1
        text=''.join(listtext) # คืนค่ากลับสู่ str
        #print(text)
        textdata.append(re.sub('/','',text))
    return ''.join(textdata)
if __name__ == '__main__':
    print(romanization('วัน')+romanization('นะ')+romanization('พง'))
    print(romanization('นัด')+romanization('ชะ')+romanization('โนน'))
    print(romanization('สรรพ'))
    print(romanization('สรร')+romanization('หา'))
    print(romanization('สรร')+romanization('หา'))
    print(romanization('แมว'))
    print(romanization('กร')==romanization('กอน'))
