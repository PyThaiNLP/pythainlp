# -*- coding: utf-8 -*-
import platform
import sys
import struct
import pip
def windows_is():
    return platform.system()=='Windows'
try:
    import icu
    print("OK")
except ImportError:
    if windows_is()==True:
        python_version='{0[0]}.{0[1]}'.format(sys.version_info)
        bit=struct.calcsize("P") * 8
        if python_version=="3.6":
            if bit=="64":
                pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp36-cp36m-win_amd64.whl'])
            else:
                pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp36-cp36m-win32.whl'])
        elif python_version=="3.5":
            if bit=="64":
                pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp35-cp35m-win_amd64.whl'])
            else:
                pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp35-cp35m-win32.whl'])
        elif python_version=="3.4":
            if bit=="64":
                pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp34-cp34m-win_amd64.whl'])
            else:
                pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp34-cp34m-win32.whl'])
        elif python_version=="2.7":
            if bit=="64":
                pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp27-cp27m-win_amd64.whl'])
            else:
                pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp27-cp27m-win32.whl'])
        else:
            pip.main(['install','pyicu'])
    else:
        pip.main(['install','pyicu'])