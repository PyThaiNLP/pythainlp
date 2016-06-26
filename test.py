from pythainlp.segment import segment
a = 'ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'
b = segment(a)
print(b)
print(type(b))
from pythainlp.rank import rank
aa = rank(a)
print(aa)
from pythainlp.romanization import romanization
b=romanization("ต้นกก")
print(b)