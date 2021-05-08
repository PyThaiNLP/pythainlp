from .oxidized_thainlp import load_dict as load_dict_to_oxidized, segment as rust_segment
import codecs
from typing import List


def load_dict(file_path:str,dict_name:str):
    """
    file_path should be an absolute path.
    dict_name can be any valid utf-8 string, except "default" which is reserved.
    """
    load_result = load_dict_to_oxidized(file_path,dict_name)
    print(load_result)

def segment(text:str,dict_name = "default", safe = False, parallel = False) -> List[List[int]]:
    """
    This method is an implementation of newmm segmentaion.
    
    Currently uses only default dict (pythainlp/corpus/words_th.txt).
    
    Support multithread mode - set by parallel flag
    
    
    
    """
    result = rust_segment(text,dict_name,safe,parallel)
    for (index,utf8bytes) in enumerate(result):
        result[index] = codecs.decode(bytearray(utf8bytes),encoding="utf-8")
    return result