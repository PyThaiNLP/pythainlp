# -*- coding_utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
def tis620_to_utf8(text: str)->str:
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


def to_idna(text: str) -> str:
    """
    Encode text with IDNA, as used in Internationalized Domain Name (IDN).

    :param str text: Thai text
    :return: IDNA-encoded text
    :rtype: str

    :Example:
    ::

        from pythainlp.util import to_idna

        to_idna("คนละครึ่ง.com")
        # output: 'xn--42caj4e6bk1f5b1j.com'
    """
    return text.encode("idna").decode("utf-8")
