from .oxidized_thainlp import segment as rust_segment
import codecs



def segment(text:str, safe = False, parallel = False) -> List[List[int]]:
    """
    This method is an implementation of newmm segmentaion.
    
    Currently uses only default dict (pythainlp/corpus/words_th.txt).
    
    Support multithread mode - set by parallel flag
    
    
    
    """
    result = rust_segment(text,safe,parallel)
    for (index,utf8bytes) in enumerate(result):
        result[index] = codecs.decode(bytearray(utf8bytes),encoding="utf-8")
    return result