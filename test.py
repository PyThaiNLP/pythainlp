from pythainlp.segment import segment
a = 'ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'
b = segment(a)
print(b)
from pythainlp.segment.dict import segment
print(segment(a))
print(type(b))
from pythainlp.rank import rank
aa = rank(a)
print(aa)
from pythainlp.romanization import romanization
b=romanization("ต้นกก")
print(b)
from pythainlp.change import *
a="l;ylfu8iy["
a=texttothai(a)
b="นามรสนอำันี"
b=texttoeng(b)
print(a)
print(b)
from pythainlp.segment.dict import segment
print(segment('ปีคริสต์ศักราช'))
from pythainlp.number import numtowords
print("5611116.50")
print(numtowords(5611116.50))

from pythainlp.postaggers.text import pts
print(pts('รัก'))