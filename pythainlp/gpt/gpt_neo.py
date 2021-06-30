# -*- coding: utf-8 -*-
from typing import List
import torch
from torch.utils.data import Dataset, random_split
from transformers import (
    GPT2Tokenizer,
    TrainingArguments,
    Trainer,
    GPTNeoForCausalLM
)
import os

torch.manual_seed(42)
class ListDataset(Dataset):
    def __init__(
        self, txt_list: List[str], tokenizer: GPT2Tokenizer, max_length: int, bos_token, eos_token
    ):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []
        for txt in txt_list:
            encodings_dict = tokenizer(
                bos_token + txt + eos_token,
                truncation=True,
                max_length=max_length,
                padding="max_length"
            )
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(
                torch.tensor(encodings_dict['attention_mask'])
            )

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx: int):
        return self.input_ids[idx], self.attn_masks[idx]


class FewShot:
    """
    Few-Shot Learning using GPT-Neo

    Hoempage: `EleutherAI/gpt-neo <https://github.com/EleutherAI/gpt-neo>`_

    Thank you code from https://link.medium.com/4FfbALWz8gb
    """
    def __init__(
        self, model_dir: str, model_name: str = "thaigpt-next", device: str = "cuda", size: str = "125M"
    ):
        """
        :param str model_dir: path of model dir
        :param str model_name: model name (thaigpt-next or gpt-neo)
        :param str device: device
        :param str size: model size
        **Options for size**
            * *125M* (default) - GPT-Neo 125M / thaigpt-next-125M
            * *1.3B* - GPT-Neo 1.3B
            * *2.7B* - GPT-Neo 2.7B
        """
        self.device = device
        self.bos_token = '<|startoftext|>'
        self.eos_token = '<|endoftext|>'
        self.pad_token = '<|pad|>'
        self.model_dir = model_dir
        if not os.path.exists(self.model_dir):
            self.init_model(model_name, size)
        else:
            self.load_model()

    def init_model(self, model_name : str, size: str = "125M") -> None:
        """
        init GPT-Neo model

        :param str size: model size
        **Options for size**
            * *125M* (default) - GPT-Neo 125M
            * *1.3B* - GPT-Neo 1.3B
            * *2.7B* - GPT-Neo 2.7B
        """
        if model_name == "thaigpt-next" and size == "125M":
            self.pretrained = "wannaphong/thaigpt-next-125m"
        elif model_name == "gpt-neo":
            self.pretrained = "EleutherAI/gpt-neo-"+str(size)
        else:
            raise NotImplementedError()
        self.tokenizer = GPT2Tokenizer.from_pretrained(
            self.pretrained,
            bos_token=self.bos_token,
            eos_token=self.eos_token,
            pad_token=self.pad_token
        )
        self.tokenizer.save_pretrained(self.model_dir)
        self.model = GPTNeoForCausalLM.from_pretrained(
            self.pretrained
        ).to(self.device)
        self.model.resize_token_embeddings(len(self.tokenizer))

    def load_model(self):
        """
        Load model from path of model directory
        """
        self.model_dir = self.model_dir
        self.tokenizer = GPT2Tokenizer.from_pretrained(
            self.model_dir,
            bos_token=self.bos_token,
            eos_token=self.eos_token,
            pad_token=self.pad_token
        )
        self.model = GPTNeoForCausalLM.from_pretrained(
            self.model_dir
        ).to(self.device)
        self.model.resize_token_embeddings(len(self.tokenizer))

    def train(
        self,
        data: List[str],
        logging_dir: str,
        num_train_epochs: int = 10,
        train_size: float = 0.95
    ):
        """
        Train model

        :param str data: List for text
        :param str logging_dir: logging directory
        :param int num_train_epochs: Number train epochs
        :param str train_size: size of train set
        """
        self.data = data
        self.max_length = max(
            [len(self.tokenizer.encode(i)) for i in self.data]
        )
        self.dataset = ListDataset(
            self.data,
            self.tokenizer,
            max_length=self.max_length,
            bos_token=self.bos_token,
            eos_token=self.eos_token
        )
        self.train_size = int(train_size * len(self.dataset))
        self.train_dataset, self.val_dataset = random_split(
            self.dataset, [
                self.train_size, len(self.dataset) - self.train_size
                ]
        )
        self.training_args = TrainingArguments(
            output_dir=self.model_dir,
            do_train=True,
            do_eval=True,
            evaluation_strategy="epoch",
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=2,
            logging_strategy="epoch",
            save_strategy="epoch",
            per_device_eval_batch_size=2,
            logging_dir=logging_dir
        )
        self.train = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.val_dataset,
            data_collator=lambda data: {
                'input_ids': torch.stack([f[0] for f in data]),
                'attention_mask': torch.stack([f[1] for f in data]),
                'labels': torch.stack([f[0] for f in data])
            }
        )
        self.train.train()
        self.train.evaluate()
        self.train.save_model(self.model_dir)

    def remove_bos(self, txt: str) -> str:
        return txt.replace(self.bos_token, '')

    def remove_eos(self, txt: str) -> str:
        return txt.replace(self.eos_token, '')

    def remove_bos_eos(self, txt: str) -> str:
        return self.remove_eos(self.remove_bos(txt))

    def gen(
        self,
        text: str,
        top_k: int = 50,
        max_length: int = 89,
        top_p: float = 0.95,
        keep_bos: bool = False,
        keep_eos: bool = False,
        temperature: int = 1,
        num_return_sequences: int = 5,
        skip_special_tokens: bool = True
    ) -> List[str]:
        """
        :param str text: text
        :param int top_k: top k
        :param int max_length: max length of return sequences
        :param float top_p: top p
        :param bool keep_bos: keep beginning of a sentence
        :param bool keep_eos: keep end of a sentence
        :param int temperature: temperature
        :param int num_return_sequences: number of return sequences
        :param bool skip_special_tokens: skip special tokens

        :return: return sequences
        :rtype: List[str]
        """
        self.generated = self.tokenizer(
            self.bos_token + text, return_tensors="pt"
        ).input_ids.to(self.device)
        self.sample_outputs = self.model.generate(
            self.generated,
            do_sample=True,
            top_k=top_k,
            max_length=max_length,
            top_p=top_p,
            temperature=temperature,
            num_return_sequences=num_return_sequences
        )
        _temp = [
            self.tokenizer.decode(
                i, skip_special_tokens=skip_special_tokens
            ) for i in self.sample_outputs
        ]
        if not keep_bos and not keep_eos:
            return [self.remove_bos_eos(i) for i in _temp]
        elif not keep_bos:
            return [self.remove_bos(i) for i in _temp]
        elif not keep_eos:
            return [self.remove_eos(i) for i in _temp]
        else:
            return _temp
