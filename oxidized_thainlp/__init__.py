from .oxidized_thainlp import segment as rust_segment
def segment(text:str, safe = False, parallel = False):
    result = segment(text,True,True)
    for (index,utf8bytes) in enumerate(result):
        result[index] = codecs.decode(bytearray(utf8bytes),encoding="utf-8")
    return result