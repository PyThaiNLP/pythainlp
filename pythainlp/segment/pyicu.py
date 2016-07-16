from __future__ import absolute_import
from __future__ import print_function
from .isthai import isThai
import PyICU
def segment(txt):
    """คืนค่าออกมาเป็น list ที่ได้มาจากการตัดคำโดย ICU"""
	bd = PyICU.BreakIterator.createWordInstance(PyICU.Locale("th"))
    bd.setText(txt)
    lastPos = bd.first()
    retTxt = ""
    try:
        while(1):
            currentPos = next(bd)
            retTxt += txt[lastPos:currentPos]
            if(isThai(txt[currentPos-1])):
                if(currentPos < len(txt)):
                    if(isThai(txt[currentPos])):
                        retTxt += ','
            lastPos = currentPos
    except StopIteration:
        pass
    return retTxt.split(',')
if __name__ == "__main__":
	print(segment('ทดสอบระบบตัดคำด้วยไอซียู'))