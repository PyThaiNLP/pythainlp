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


class ListDataset(Dataset):
    def __init__(self, txt_list, tokenizer, max_length):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []
        for txt in txt_list:
            encodings_dict = tokenizer(
                '<|startoftext|>' + txt + '<|endoftext|>',
                truncation=True,
                max_length=max_length,
                padding="max_length"
            )
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attn_masks[idx]


class FewShot:
    def __init__(self, model_dir: str, device: str = 'cuda', size: str = "125M") -> None:
        self.device = device
        self.model_dir = model_dir
        if os.path.exists(self.model_dir):
            self.init_model(size)
        else:
            self.load_model()

    def init_model(self, size: str = "125M") -> None:
        self.pretraine = "EleutherAI/gpt-neo-%f{size}"
        self.tokenizer = GPT2Tokenizer.from_pretrained(
            self.pretraine,
            bos_token='<|startoftext|>',
            eos_token='<|endoftext|>',
            pad_token='<|pad|>'
        )
        self.model = GPTNeoForCausalLM.from_pretrained(self.pretraine).to(self.device)
        self.model.resize_token_embeddings(len(self.tokenizer))

    def load_model(self):
        self.pretraine = self.model_dir
        self.tokenizer = GPT2Tokenizer.from_pretrained(
            self.pretraine,
            bos_token='<|startoftext|>',
            eos_token='<|endoftext|>',
            pad_token='<|pad|>'
        )
        self.model = GPTNeoForCausalLM.from_pretrained(
            self.pretraine
        ).to(self.device)
        self.model.resize_token_embeddings(len(self.tokenizer))

    def train(
        self,
        data: List[str],
        logging_dir: str,
        num_train_epochs = 10,
        test_on: bool = True,
        train_size: float = 0.95
    ):
        self.data = data
        self.max_length = max(
            [len(self.tokenizer.encode(i)) for i in self.data]
        )
        self.dataset = ListDataset(
            self.data,
            self.tokenizer,
            max_length=self.max_length
        )
        self.train_size = int(train_size * len(self.dataset))
        self.train_dataset, self.val_dataset = random_split(
            self.dataset, [
                self.train_size, len(self.dataset) - self.train_size
                ]
        )
        self.training_args = TrainingArguments(
            output_dir=self.model_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=2,
            per_device_eval_batch_size=2,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir=logging_dir
        )
        Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.val_dataset,
            data_collator=lambda data: {
                'input_ids': torch.stack([f[0] for f in data]),
                'attention_mask': torch.stack([f[1] for f in data]),
                'labels': torch.stack([f[0] for f in data])
            }
        ).train()

    def gen(
        self,
        text: str,
        top_k: int = 50,
        max_length: int = 89,
        top_p: float = 0.95,
        temperature: int = 1,
        num_return_sequences: int = 5
    ):
        self.generated = self.tokenizer(
            '<|startoftext|>' + text, return_tensors="pt"
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
