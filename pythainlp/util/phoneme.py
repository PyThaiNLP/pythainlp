# -*- coding: utf-8 -*-
"""
Phonemes util
"""

consonants_ipa_nectec = [
    ("k","k","k^"),
    ("kʰ","kh"),
    ("ŋ","ng","ng^"),
    ("tɕ","c"),
    ("tɕʰ","ch"),
    ("s","s"),
    ("j","j","j^"),
    ("d","d"),
    ("t","y","t^"),
    ("tʰ","th"),
    ("n","n","n^"),
    ("b","b"),
    ("p","p","p^"),
    ("pʰ","ph"),
    ("f","f"),
    ("m","m","m^"),
    ("r","r"),
    ("l","l"),
    ("w","w","w^"),
    ("h","h"),
    ("?","z","z^")
]
# ipa, initial, final

monophthong_ipa_nectec = [
    ("i","i"),
    ("e","e"),
    ("ɛ","x"),
    ("ɤ","q"),
    ("a","a"),
    ("am","am^"),
    ("aj","aj^"),
    ("aw","aw^"),
    ("u","u"),
    ("o","o"),
    ("ɔ","@"),
    ("ii","ii"),
    ("ee","ee"),
    ("ɛɛ","xx"),
    ("ɯɯ","vv"),
    ("ɤɤ","qq"),
    ("aa","aa"),
    ("uu","uu"),
    ("oo","oo"),
    ("","@@"), #-อ long
]

diphthong_ipa_nectec = [
    ("ia","ia"),
    ("ɯa","va"),
    ("ua","ua"),
    ("iia","iia"),
    ("ɯɯa","vva"),
    ("uua","uua"),
]

tones_ipa_nectec = [
    ("˧","0"),
    ("˨˩","1"),
    ("˥˩","2"),
    ("˦˥","3"),
    ("˩˩˦","4"),
]

dict_nectec_to_ipa = {i[1]:i[0] for i in consonants_ipa_nectec+monophthong_ipa_nectec+diphthong_ipa_nectec+tones_ipa_nectec}
dict_nectec_to_ipa.update({i[2]:i[0] for i in consonants_ipa_nectec if len(i)>2})

def nectec_to_ipa(pronunciation: str) -> str:
    """
    Converter NECTEC system to IPA system

    :Example:
    ::
        from pythainlp.util import nectec_to_ipa
 
        print(nectec_to_ipa("kl-uua-j^-2"))
        # output : 'kl uua j ˥˩'


    References
    ----------

    Pornpimon Palingoon, Sumonmas Thatphithakkul. Chapter 4 Speech processing and Speech corpus. In: Handbook of Thai Electronic Corpus. 1st ed. p. 122–56.
    """
    pronunciation = pronunciation.split("-")
    _temp = []
    for i in pronunciation:
        if i in dict_nectec_to_ipa.keys():
            _temp.append(dict_nectec_to_ipa[i])
        else:
            _temp.append(i)
    return ' '.join(_temp)
