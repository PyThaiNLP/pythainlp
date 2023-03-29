# -*- coding: utf-8 -*-
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
"""
Thai soundex

Has three systems to choose from: Udom83 (default), LK82, and MetaSound
"""

__all__ = [
    "soundex",
    "lk82",
    "metasound",
    "udom83",
    "prayut_and_somchaip",
]

from pythainlp.soundex.lk82 import lk82
from pythainlp.soundex.metasound import metasound
from pythainlp.soundex.udom83 import udom83
from pythainlp.soundex.prayut_and_somchaip import prayut_and_somchaip

DEFAULT_SOUNDEX_ENGINE = "udom83"

from pythainlp.soundex.core import soundex
