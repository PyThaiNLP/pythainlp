# -*- coding: utf-8 -*-
from __future__ import absolute_import,division,unicode_literals,print_function
'''
ขอขอบคุณ คุณ Korakot Chaovavanich‎ สำหรับโค้ด word_frequency จาก https://www.facebook.com/photo.php?fbid=363640477387469&set=gm.434330506948445&type=3&permPage=1
'''
import re,requests
def word_frequency(word,domain='all'):
    listdomain={'all':'','imaginative':'1','natural-pure-science':'2','applied-science':'3','social-science':'4','world-affairs-history':'5','commerce-finance':'6','arts':'7','belief-thought':'8','leisure':'9','others':'0'}
    url = "http://www.arts.chula.ac.th/~ling/TNCII/corp.php"
    data = {'genre[]':'','domain[]':listdomain[domain],'sortby':'perc','p':word}
    r = requests.post(url,data=data)
    pat = re.compile('TOTAL</font>(?s).*?#ffffff">(.*?)</font>')
    n = pat.search(r.text).group(1)
    return int('0'+n.strip())