from tltk.nlp import spell_candidates
from typing import List

def spell(text: str) -> List[str]:
    return spell_candidates(text)
