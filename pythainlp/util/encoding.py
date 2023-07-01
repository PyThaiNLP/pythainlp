# -*- coding_utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
def tis620_to_utf8(text: str)->str:
    """
    Convert TIS-620 to UTF-8

    :param str text: Text that use TIS-620 encoding
    :return: Text that use UTF-8 encoding
    :rtype: str

    :Example:
    ::

        from pythainlp.util import tis620_to_utf8

        tis620_to_utf8("¡ÃÐ·ÃÇ§ÍØµÊÒË¡ÃÃÁ")
        # output: 'กระทรวงอุตสาหกรรม'
    """
    return text.encode("cp1252", "ignore").decode("tis-620")
