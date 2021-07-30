# -*- coding: utf-8 -*-
"""
Named-entity recognizer
"""
from typing import List, Tuple, Union

class NER:
    def __init__(self, engine: str) -> None:
        self.load_engine(engine=engine)

    def load_engine(self, engine: str) -> None:
        self.engine = None
        if engine == "thainer":
            from pythainlp.tag.thainer import ThaiNameTagger
            self.engine = ThaiNameTagger()
        else:
            raise ValueError(
                "ner class not support {0} engine.".format(engine)
            )

    def tag(
        self,
        text
    ) -> Union[List[Tuple[str, str]], List[Tuple[str, str, str]], str]:
        return self.engine.get_ner(text)
