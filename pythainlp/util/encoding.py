# -*- coding_utf-8 -*-
# SPDX-FileCopyrightText: Copyright 2016-2023 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
def tis620_to_utf8(text: str) -> str:
    """
    Convert TIS-620 to UTF-8

    :param str text: TIS-620 encoded text
    :return: UTF-8 encoded text
    :rtype: str

    :Example:
    ::

        from pythainlp.util import tis620_to_utf8

        tis620_to_utf8("¡ÃÐ·ÃÇ§ÍØµÊÒË¡ÃÃÁ")
        # output: 'กระทรวงอุตสาหกรรม'
    """
    return text.encode("cp1252", "ignore").decode("tis-620")


def thai_to_idn(text: str) -> str:
    """
    Encode text with Punycode, as used in Internationalized Domain Name (IDN).

    :param str text: Thai text
    :return: Text in IDNA encoding
    :rtype: str

    :Example:
    ::

        from pythainlp.util import thai_to_idn

        thai_to_idn("คนละครึ่ง.com")
        # output: 'xn--42caj4e6bk1f5b1j.com'
    """
    return text.encode("idna").decode("utf-8")
