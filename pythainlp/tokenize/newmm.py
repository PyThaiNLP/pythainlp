'''
ตัดคำภาษาไทยโดยใช้ Maximum Matching algorithm
เดติดโค้ดต้นฉบับ คุณ Korakot Chaovavanich
จาก https://www.facebook.com/groups/408004796247683/permalink/431283740586455/ 
'''
from marisa_trie import Trie
from collections import Counter, defaultdict
from pythainlp.corpus.thaiword import get_data
class LatticeString(str):
    def __new__(cls, value, multi=None): 
        ''' Return a string instance 
        ''' 
        return str.__new__(cls, value)
    
    def __init__(self, value, multi=None):
        self.unique = True
        if multi:
            self.multi = list(multi)
            if len(self.multi) > 1:
                self.unique = False
        else:
            self.multi = [value]
            
        self.in_dict = True   # บอกว่าเป็นคำมีในดิกหรือเปล่า

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
    trie = Trie(get_data())
    words_at = defaultdict(list) # main data structure
    
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
        # กรณี len(q) == 0  คือ เจอคำนอก dict
def mmcut(text):
    '''
    ตัดคำแบบ maximal matching
    '''
    res = []
    for w in tcut(text):
        if w.unique:
            res.append(w)
        else:
            mm = min(w.multi, key=lambda x: x.count('/'))
            res.extend(mm.split('/'))
    return res