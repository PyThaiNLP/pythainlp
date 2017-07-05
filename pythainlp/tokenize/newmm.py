'''
ตัดคำภาษาไทยโดยใช้ Maximum Matching algorithm
เดติดโค้ดต้นฉบับ คุณ Korakot Chaovavanich
จาก https://www.facebook.com/groups/408004796247683/permalink/431283740586455/ 
'''
from marisa_trie import Trie
from collections import Counter, defaultdict
from pythainlp.corpus.thaiword import get_data
class LatticeString(str):
    def __new__(cls, value, multi=None, in_dict=True): 
        ''' Return a string instance 
        ''' 
        return str.__new__(cls, value)
    
    def __init__(self, value, multi=None, in_dict=True):
        self.unique = True
        if multi:
            self.multi = list(multi)
            if len(self.multi) > 1:
                self.unique = False
        else:
            self.multi = [value]
            
        self.in_dict = in_dict   # บอกว่าเป็นคำมีในดิกหรือเปล่า

    def suggest(self):
        return []
def serialize(p, p2):
    for w in words_at[p]:
        p_ = p + len(w)
        if p_== p2:
            yield w
        elif p_ < p2:
            for path in serialize(p_, p2):
                yield w+'/'+path
# มี jigsaw พร้อมแล้ว  ต่อไปก็ลองเขียน tcut ใหม่
def tcut(text):
    #global last_p, i, q, ww   # for debug
    trie = Trie(get_data())
    words_at = defaultdict(list)  # main data structure
    
    def serialize(p, p2):    # helper function
        for w in words_at[p]:
            p_ = p + len(w)
            if p_== p2:
                yield w
            elif p_ < p2:
                for path in serialize(p_, p2):
                    yield w+'/'+path
                    
    q = {0}
    last_p = 0   # last position for yield
    while min(q) < len(text):
        p = min(q)
        q -= {p}  # q.pop, but for set
        
        for w in trie.prefixes(text[p:]):
            words_at[p].append(w)
            q.add(p+len(w))   
            
        if len(q)==1:
            q0 = min(q)
            yield LatticeString(text[last_p:q0], serialize(last_p, q0))
            last_p = q0
            
        # กรณี len(q) == 0  คือ ไม่มีใน dict
        if len(q)==0:
            # skip น้อยที่สุด ที่เป็นไปได้
            for i in range(p, len(text)):
                ww = trie.prefixes(text[i:])
                if ww:
                    break
            else:
                i = len(text)
            w = text[p:i]
            w = w.replace(' ','') # ลบค่าที่ว่าง
            words_at[p].append(w)
            yield LatticeString(w, in_dict=False)
            last_p = i
            q.add(i)
def mmcut(text):
    '''
	ใช้ Maximum Matching algorithm ในการตัดคำภาษาไทย
    '''
    res = []
    for w in tcut(text):
        if w.unique:
            res.append(w)
        else:
            mm = min(w.multi, key=lambda x: x.count('/'))
            res.extend(mm.split('/'))
    return res
def combine(ww):
    if ww == []:
        yield ""
    else:
        w = ww[0]
        for tail in combine(ww[1:]):
            if w.unique:
                yield w+"|"+tail
            else:
                for m in w.multi:
                    yield m.replace("/","|")+"|"+tail
                    
def listcut(text):
    '''
	ใช้ในการหา list ที่สามารถตัดคำได้ทั้งหมด
	'''
    ww = list(tcut(text))
    return list(combine(ww))
if __name__ == "__main__":
	text='ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด'
	print(mmcut(text))
	print(listcut(text))