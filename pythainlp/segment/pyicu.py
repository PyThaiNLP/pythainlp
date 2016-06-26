from pythainlp.segment.isthai import isThai
import PyICU
def segment(txt):
    bd = PyICU.BreakIterator.createWordInstance(PyICU.Locale("th"))
    bd.setText(txt)
    lastPos = bd.first()
    retTxt = ""
    try:
        while(1):
            currentPos = next(bd)
            retTxt += txt[lastPos:currentPos]
            #เฉพาะภาษาไทยเท่านั้น
            if(isThai(txt[currentPos-1])):
                if(currentPos < len(txt)):
                    if(isThai(txt[currentPos])):
                        #คั่นคำที่แบ่ง
                        retTxt += ','
            lastPos = currentPos
    except StopIteration:
        pass
        #retTxt = retTxt[:-1]
    return retTxt.split(',')
if __name__ == "__main__":
	print(segment('ทดสอบระบบตัดคำด้วยไอซียู'))