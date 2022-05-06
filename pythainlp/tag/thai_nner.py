from thai_nner import NNER
from pythainlp.corpus import get_path_folder_corpus, get_corpus_path

class Thai_NNER:
    def __init__(self, path_model = get_corpus_path('thai_nner','1.0')) -> None:
        self.model = NNER(path_model=path_model)

    def tag(self, text):
        return self.model.get_tag(text)