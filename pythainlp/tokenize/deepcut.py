# -*- coding: utf-8 -*-
"""
deepcut wrapper
"""
import sys

try:
    import deepcut
except ImportError:
    """ในกรณีที่ยังไม่ติดตั้ง deepcut ในระบบ"""
    from pythainlp.tools import install_package

    install_package("deepcut")
    try:
        import deepcut
    except ImportError:
        sys.exit("Error: Try 'pip install deepcut'")


def segment(text):
    return deepcut.tokenize(text)
