# -*- coding: utf-8 -*-
import platform
import sys
import struct
def windows_is():
    return platform.system()=='Windows'
def icu_install():
    if windows_is()==True:
        try:
            import icu
            i=True
        except ImportError:
            i=False
        python_version='{0[0]}.{0[1]}'.format(sys.version_info)
        bit=struct.calcsize("P") * 8
        if python_version=="3.6" and i!=True:
            if bit=="64":
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp36-cp36m-win_amd64.whl'
            else:
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp36-cp36m-win32.whl'
        elif python_version=="3.5" and i!=True:
            if bit=="64":
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp35-cp35m-win_amd64.whl'
            else:
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp35-cp35m-win32.whl'
        elif python_version=="3.4" and i!=True:
            if bit=="64":
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp34-cp34m-win_amd64.whl'
            else:
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp34-cp34m-win32.whl'
        elif python_version=="2.7" and i!=True:
            if bit=="64":
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp27-cp27m-win_amd64.whl'
            else:
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp27-cp27m-win32.whl'
        else:
            icu='pyicu'
    else:
        icu='pyicu'
    return icu