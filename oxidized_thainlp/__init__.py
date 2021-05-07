from .oxidized_thainlp import segment as rust_segment
import codecs
def segment(text:str, safe = False, parallel = False):
    result = rust_segment(text,True,True)
    for (index,utf8bytes) in enumerate(result):
        result[index] = codecs.decode(bytearray(utf8bytes),encoding="utf-8")
    return result