import PyICU
def isThai(chr):
    cVal = ord(chr)
    if(cVal >= 3584 and cVal <= 3711):
        return True
    return False


def icu(txt):
	bd = PyICU.BreakIterator.createWordInstance(PyICU.Locale("th"))
	bd.setText(txt)
	lastPos = bd.first()
	retTxt = ""
	try:
		while(1):
			currentPos = next(bd)
			retTxt += txt[lastPos:currentPos]
			# เฉพาะภาษาไทยเท่านั้น
			if(isThai(txt[currentPos - 1])):
				if(currentPos < len(txt)):
					if(isThai(txt[currentPos])):
                        # คั่นคำที่แบ่ง
						retTxt += ','
			lastPos = currentPos
	except StopIteration:
		pass
	return txt  # (','.join(str(x) for x in txt))  # แยกออกมาเป็น list
