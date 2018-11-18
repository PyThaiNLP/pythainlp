# -*- coding: utf-8 -*-

import datetime
from pythainlp.util import thai_strftime

fmt = "%Aที่ %-d %B พ.ศ. %Y เวลา %H:%Mน. (%a %d-%b-%y)"
date = datetime.datetime(1976, 10, 6, 1, 40)

# วันพุธที่ 6 ตุลาคม พ.ศ. 2519 เวลา 01:40น. (พ 06-ต.ค.-19)
print(thai_strftime(date, fmt))
