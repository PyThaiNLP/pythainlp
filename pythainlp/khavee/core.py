from pythainlp.tokenize import subword_tokenize

class KhaveeVerifier:
    def check_sara(self,word):
        sara = []
        countoa = 0
        # In case การันย์
        if '์' in word[-1]:
            word = word[:-2]
        # In case สระเดี่ยว
        for i in word:
            if i == 'ะ' or i == 'ั':
                sara.append('อะ')
            elif i == 'ิ':
                sara.append('อิ')
            elif i == 'ุ':
                sara.append('อุ')
            elif i == 'ึ':
                sara.append('อึ')
            elif i == 'ี':
                sara.append('อี')
            elif i == 'ู':
                sara.append('อู')
            elif i == 'ื':
                sara.append('อือ')
            elif i == 'เ':
                sara.append('เอ')
            elif i == 'แ':
                sara.append('แอ')
            elif i == 'า':
                sara.append('อา') 
            elif i == 'โ':
                sara.append('โอ')
            elif i == 'ำ':
                sara.append('อำ')
            elif i == 'อ':
                countoa += 1
                sara.append('ออ')
            elif i == 'ั' and 'ว' in word:
                sara.append('อัว')
            elif i == 'ไ' or i == 'ใ':
                sara.append('ไอ') 
            elif 'รร' in word:
                if self.check_marttra(word) == 'กม':
                    sara.append('อำ')
                else:
                    sara.append('อะ')
        # Incase ออ
        if countoa == 1 and 'อ' in word[-1]:
            sara.remove('ออ')
        # In case เอ เอ 
        countA = 0
        for i in sara:
            if i == 'เอ':
                countA = countA + 1
            if countA > 1:
                sara.remove('เอ')
                sara.remove('เอ')
                sara.append('แ')
        # In case สระประสม
        if 'เอ' in sara and 'อะ' in sara:
            sara.remove('เอ')
            sara.remove('อะ')
            sara.append('เอะ')
        elif 'แอ' in sara and 'อะ' in sara:
            sara.remove('แอ')
            sara.remove('อะ')
            sara.append('แอะ')
        if 'เอะ' in sara and 'ออ' in sara:
            sara.remove('เอะ')
            sara.remove('ออ')
            sara.append('เออะ')
        elif 'เอ' in sara and 'อิ' in sara:
            sara.remove('เอ')
            sara.remove('อิ')
            sara.append('เออ')        
        elif 'เอะ' in sara and 'อา' in sara:
            sara.remove('เอะ')
            sara.remove('ออ')
            sara.append('เอาะ')
        elif 'เอ' in sara and 'ออ' in sara and 'อ' in word[-1]:
            sara.remove('เอ')
            sara.remove('ออ')
            sara.append('เออ')
        elif 'โอ' in sara and 'อะ' in sara: 
            sara.remove('โอ')
            sara.remove('อะ')
            sara.append('โอะ')
        elif 'เอ' in sara and 'อี' in sara: 
            sara.remove('เอ')
            sara.remove('อี')
            sara.append('เอีย')
        elif 'เอ' in sara and 'อือ' in sara: 
            sara.remove('เอ')
            sara.remove('อือ')
            sara.append('อัว')   
        elif 'เอ' in sara and 'อา' in sara: 
            sara.remove('เอ')
            sara.remove('อา')
            sara.append('เอา') 
        if 'อือ' in sara and 'เออ' in sara: 
            sara.remove('เออ')
            sara.remove('อือ')
            sara.append('เอือ')  
        elif 'ออ' in sara and len(sara) > 1:
            sara.remove('ออ')        
        elif 'ว' in word and len(sara) == 0:
            sara.append('อัว')
        if 'ั' in word and self.check_marttra(word) == 'กา':
            sara = []
            sara.append('ไอ')
        # In case อ
        if word == 'เออะ':
            sara = []
            sara.append('เออะ')
        elif word == 'เออ':
            sara = []
            sara.append('เออ')
        elif word == 'เอ':
            sara = []
            sara.append('เอ')
        elif word == 'เอะ':
            sara = []
            sara.append('เอะ')
        elif word == 'เอา':
            sara = []
            sara.append('เอา')
        if 'ฤา' in word or 'ฦา' in word:
            sara = []
            sara.append('อือ') 
        elif 'ฤ' in word or 'ฦ' in word:
            sara = []
            sara.append('อึ') 
        # In case กน
        if sara == [] and len(word) == 2:
            if word[-1] != 'ร':
                sara.append('โอะ')
            else:
                sara.append('ออ') 
        elif sara == [] and len(word) == 3:
            sara.append('ออ') 
        if sara == []:
            return 'Cant find Sara in this word'
        else:
            return sara[0]


    def check_marttra(self,word):
        if word[-1] == 'ร' and word[-2] in ['ต','ท'] :
            word = word[:-1]
            # print(word)
        if '์' in word[-1]:
            if 'ิ' in word[-2] or 'ุ' in word[-2]:
                word = word[:-3]
            else:
                word = word[:-2]
        if 'ำ' in word or ('ํ' in word and 'า' in word) or 'ไ' in word or 'ใ' in word:
            return 'กา'
        elif word[-1] in ['า','ะ','ิ','ี','ุ','ู','อ'] or ('ี' in word and 'ย' in word[-1]) or ('ื' in word and 'อ' in word[-1]):
            return 'กา'
        elif word[-1] in ['ง']:
            return 'กง'
        elif word[-1] in ['ม']:
            return 'กม'
        elif word[-1] in ['ย']:
            if 'ั' in word:
                return 'กา'
            else:
                return 'เกย'
        elif word[-1] in ['ว']:
            return 'เกอว'
        elif word[-1] in ['ก','ข','ค','ฆ']:
            return 'กก'
        elif word[-1] in ['จ','ช','ซ','ฎ','ฏ','ฐ','ฑ','ฒ','ด','ต','ถ','ท','ธ','ศ','ษ','ส'] :
            return 'กด'
        elif word[-1] in ['ญ',', ณ' ,'น' ,'ร' ,'ล' ,'ฬ']:
            return 'กน'
        elif word[-1] in ['บ', 'ป', 'พ', 'ฟ', 'ภ']:
            return 'กบ'
        else:
           return 'Cant find Marttra in this word'

    def check_sumpus(self,word1,word2):
        marttra1 = self.check_marttra(word1)
        marttra2 = self.check_marttra(word2)
        sara1 = self.check_sara(word1)
        sara2 = self.check_sara(word2)
        if sara1 == 'อะ' and marttra1 == 'เกย':
            sara1 = 'ไอ'
            marttra1 = 'กา'
        elif sara2 == 'อะ' and marttra2 == 'เกย':
            sara2 = 'ไอ'
            marttra2 = 'กา'
        if sara1 == 'อำ' and marttra1 == 'กม':
            sara1 = 'อำ'
            marttra1 = 'กา'
        elif sara2 == 'อำ' and marttra2 == 'กม':
            sara2 = 'อำ'
            marttra2 = 'กา'
        # print(marttra1,marttra2)
        # print(sara1,sara2)
        if marttra1 == marttra2 and sara1 == sara2:
            return True
        else:
            return False

    def check_klon(self,text,k_type=8):
        if k_type == 8:
            try:
                error = []
                list_sumpus_sent1 = []
                list_sumpus_sent2h = []
                list_sumpus_sent2l = []
                list_sumpus_sent3 = []
                list_sumpus_sent4 = []
                for i, sent in enumerate(text.split()):
                    sub_sent = subword_tokenize(sent, engine='dict')
                    # print(i)
                    if len(sub_sent) > 10:
                        error.append('In the sentence'+str(i+2)+'there are more than 10 words.'+str(sub_sent))
                    if (i+1) % 4 == 1:
                        list_sumpus_sent1.append(sub_sent[-1])
                    elif (i+1) % 4 == 2:
                        list_sumpus_sent2h.append([sub_sent[1],sub_sent[2],sub_sent[3],sub_sent[4]])
                        list_sumpus_sent2l.append(sub_sent[-1])
                    elif (i+1) % 4 == 3:
                        list_sumpus_sent3.append(sub_sent[-1])
                    elif (i+1) % 4 == 0:
                        list_sumpus_sent4.append(sub_sent[-1])
                if len(list_sumpus_sent1) != len(list_sumpus_sent2h) or len(list_sumpus_sent2h) != len(list_sumpus_sent2l) or len(list_sumpus_sent2l) != len(list_sumpus_sent3) or len(list_sumpus_sent3) != len(list_sumpus_sent4)  or len(list_sumpus_sent4) != len(list_sumpus_sent1):
                    return 'The poem does not complete 4 sentences.'
                else:
                    for i in range(len(list_sumpus_sent1)):
                        countwrong = 0
                        for j in list_sumpus_sent2h[i]:
                            if self.check_sumpus(list_sumpus_sent1[i],j) == False:
                                    countwrong +=1
                        if  countwrong > 3:
                            error.append('Cant find rhyme between paragraphs '+str((list_sumpus_sent1[i],list_sumpus_sent2h[i]))+'in paragraph '+str(i+1))
                        if self.check_sumpus(list_sumpus_sent2l[i],list_sumpus_sent3[i]) == False:
                            # print(sumpus_sent2l,sumpus_sent3)
                            error.append('Cant find rhyme between paragraphs '+str((list_sumpus_sent2l[i],list_sumpus_sent3[i]))+'in paragraph '+str(i+1))
                        if i > 0:
                            if self.check_sumpus(list_sumpus_sent2l[i],list_sumpus_sent4[i-1]) == False:
                                error.append('Cant find rhyme between paragraphs '+str((list_sumpus_sent2l[i],list_sumpus_sent4[i-1]))+'in paragraph '+str(i+1))
                    if error == []:
                        return 'The poem is correct according to the principle.'
                    else:
                        return error
            except:
                return 'Something went wrong Make sure you enter it in correct form of klon4.'
        elif k_type == 4:
            try:
                error = []
                list_sumpus_sent1 = []
                list_sumpus_sent2h = []
                list_sumpus_sent2l = []
                list_sumpus_sent3 = []
                list_sumpus_sent4 = []
                for i, sent in enumerate(text.split()):
                    sub_sent = subword_tokenize(sent, engine='dict')
                    if len(sub_sent) > 5:
                        error.append('In the sentence'+str(i+2)+'there are more than 4 words.'+str(sub_sent))
                    if (i+1) % 4 == 1:
                        list_sumpus_sent1.append(sub_sent[-1])
                    elif (i+1) % 4 == 2:
                        # print([sub_sent[1],sub_sent[2]])
                        list_sumpus_sent2h.append([sub_sent[1],sub_sent[2]])
                        list_sumpus_sent2l.append(sub_sent[-1])
                    elif (i+1) % 4 == 3:
                        list_sumpus_sent3.append(sub_sent[-1])
                    elif (i+1) % 4 == 0:
                        list_sumpus_sent4.append(sub_sent[-1])
                if len(list_sumpus_sent1) != len(list_sumpus_sent2h) or len(list_sumpus_sent2h) != len(list_sumpus_sent2l) or len(list_sumpus_sent2l) != len(list_sumpus_sent3) or len(list_sumpus_sent3) != len(list_sumpus_sent4)  or len(list_sumpus_sent4) != len(list_sumpus_sent1):
                    return 'The poem does not complete 4 sentences.'
                else:
                    for i in range(len(list_sumpus_sent1)):
                        countwrong = 0
                        for j in list_sumpus_sent2h[i]:
                            # print(list_sumpus_sent1[i],j)
                            if self.check_sumpus(list_sumpus_sent1[i],j) == False:
                                    countwrong +=1
                        if  countwrong > 1:
                            error.append('Cant find rhyme between paragraphs '+str((list_sumpus_sent1[i],list_sumpus_sent2h[i]))+'in paragraph '+str(i+1))
                        if self.check_sumpus(list_sumpus_sent2l[i],list_sumpus_sent3[i]) == False:
                            # print(sumpus_sent2l,sumpus_sent3)
                            error.append('Cant find rhyme between paragraphs '+str((list_sumpus_sent2l[i],list_sumpus_sent3[i]))+'in paragraph '+str(i+1))
                        if i > 0:
                            if self.check_sumpus(list_sumpus_sent2l[i],list_sumpus_sent4[i-1]) == False:
                                error.append('Cant find rhyme between paragraphs '+str((list_sumpus_sent2l[i],list_sumpus_sent4[i-1]))+'in paragraph '+str(i+1))
                    if error == []:
                        return 'The poem is correct according to the principle.'
                    else:
                        return error
            except:
                return 'Something went wrong Make sure you enter it in correct form.'
            
        else:
            return 'Something went wrong Make sure you enter it in correct form.'