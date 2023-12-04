# -*- coding_utf-8 -*-
# SPDX-FileCopyrightText: Copyright 2016-2023 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
def tis620_to_utf8(text: str)->str:
    """
    Convert TIS-620 to UTF-8

    :param str text: Text that uses TIS-620 encoding
    :return: Text that uses UTF-8 encoding
    :rtype: str

    :Example:
    ::

        from pythainlp.util import tis620_to_utf8

        tis620_to_utf8("¡ÃÐ·ÃÇ§ÍØµÊÒË¡ÃÃÁ")
        # output: 'กระทรวงอุตสาหกรรม'
    """
    return text.encode("cp1252", "ignore").decode("tis-620")
