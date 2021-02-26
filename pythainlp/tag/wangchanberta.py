from typing import Dict, List, Tuple, Union
import re
from transformers import (
    CamembertTokenizer,
    AutoTokenizer,
    pipeline,
)

class ThaiNameTagger:
    def __init__(self,
                dataset_name: str = "thainer",
                model_name:str = "wangchanberta-base-att-spm-uncased"
                ) -> None:
        self.model_name = model_name
        self.tokenizer = CamembertTokenizer.from_pretrained(
                                    f'airesearch/{self.model_name}',
                                    revision='main')
        if self.model_name == "wangchanberta-base-att-spm-uncased":
            self.tokenizer.additional_special_tokens = ['<s>NOTUSED', '</s>NOTUSED', '<_>']
        self.classify_tokens = pipeline(
            task='ner',
            tokenizer=self.tokenizer,
            model = f'airesearch/{self.model_name}',
            revision = f'finetuned@{dataset_name}-ner',
            ignore_labels=[], 
            grouped_entities=True
        )

    def get_ner(
        self, text: str, tag: bool = False
    ) -> List[Tuple[str, str]]:
        """
        This function tags named-entitiy from text in IOB format.

        Powered by wangchanberta from VISTEC-depa AI Research Institute of Thailand
        :param str text: text in Thai to be tagged
        :param bool tag: output like html tag.
        :return: a list of tuple associated with tokenized word group, NER tag,
                 and output like html tag (if the parameter `tag` is
                 specified as `True`).
                 Otherwise, return a list of tuple associated with tokenized
                 word and NER tag
        :rtype: Union[list[tuple[str, str]]], str
        """
        text = re.sub(" ", "<_>", text)
        self.json_ner = self.classify_tokens(text)
        self.output = ""
        self.sent_ner = [(i['word'].replace("<_>", " "),i['entity_group']) for i in self.json_ner]
        if tag:
            temp = ""
            sent = ""
            for idx, (word, ner) in enumerate(self.sent_ner):
                if ner.startswith("B-") and temp != "":
                    sent += "</" + temp + ">"
                    temp = ner[2:]
                    sent += "<" + temp + ">"
                elif ner.startswith("B-"):
                    temp = ner[2:]
                    sent += "<" + temp + ">"
                elif ner == "O" and temp != "":
                    sent += "</" + temp + ">"
                    temp = ""
                sent += word

                if idx == len(self.sent_ner) - 1 and temp != "":
                    sent += "</" + temp + ">"

            return sent
        
        return self.sent_ner
