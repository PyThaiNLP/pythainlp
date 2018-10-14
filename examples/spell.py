# -*- coding: utf-8 -*-

from pythainlp.spell import spell

a = spell("สี่เหลียม")
print(a)  # ['สี่เหลี่ยม']

# a = spell("สี่เหลียม", engine="hunspell")  # available in some Linux systems
