# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Two-stage Thai Misspelling Correction based on Pre-trained Language Models

:See Also:
    * Paper: \
        https://ieeexplore.ieee.org/abstract/document/10202006
    * GitHub: \
        https://github.com/bookpanda/Two-stage-Thai-Misspelling-Correction-Based-on-Pre-trained-Language-Models
"""
from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer, BertForTokenClassification
import torch

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
tokenizer = AutoTokenizer.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")

class BertModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = BertForTokenClassification.from_pretrained('bookpanda/wangchanberta-base-att-spm-uncased-tagging')

    def forward(self, input_id, mask, label):
        output = self.bert(input_ids=input_id, attention_mask=mask, labels=label, return_dict=False)
        return output

tagging_model = BertModel()
if use_cuda:
    tagging_model = tagging_model.to(device=device)
ids_to_labels = {0: 'f', 1: 'i'}

def align_word_ids(texts):
    tokenized_inputs = tokenizer(texts, padding='max_length', max_length=512, truncation=True)
    word_ids = tokenized_inputs.word_ids()
    label_ids = []
    for word_idx in word_ids:

        if word_idx is None:
            label_ids.append(-100)
        else:
            try:
                label_ids.append(2)
            except:
                label_ids.append(-100)

    return label_ids

def evaluate_one_text(model, sentence):
    text = tokenizer(sentence, padding='max_length', max_length = 512, truncation=True, return_tensors="pt")
    mask = text['attention_mask'][0].unsqueeze(0).to(device)
    input_id = text['input_ids'][0].unsqueeze(0).to(device)
    label_ids = torch.Tensor(align_word_ids(sentence)).unsqueeze(0).to(device)

    logits = tagging_model(input_id, mask, None)
    logits_clean = logits[0][label_ids != -100]

    predictions = logits_clean.argmax(dim=1).tolist()
    prediction_label = [ids_to_labels[i] for i in predictions]
    return prediction_label


mlm_model = AutoModelForMaskedLM.from_pretrained("bookpanda/wangchanberta-base-att-spm-uncased-masking")
if use_cuda:
    mlm_model = mlm_model.to(device=device)

def correct(text):
    ans = []
    i_f = evaluate_one_text(tagging_model, text)
    a = tokenizer(text)
    i_f_len = len(i_f)
    for j in range(i_f_len):
        if i_f[j] == 'i':
            ph = a['input_ids'][j+1]
            a['input_ids'][j+1] = 25004
            b = {'input_ids': torch.Tensor([a['input_ids']]).type(torch.int64).to(device), 'attention_mask': torch.Tensor([a['attention_mask']]).type(torch.int64).to(device)}
            token_logits = mlm_model(**b).logits
            mask_token_index = torch.where(b["input_ids"] == tokenizer.mask_token_id)[1]
            mask_token_logits = token_logits[0, mask_token_index, :]
            top_5_tokens = torch.topk(mask_token_logits, 5, dim=1).indices[0].tolist()
            ans.append((j, top_5_tokens[0]))
            text = ''.join(tokenizer.convert_ids_to_tokens(a['input_ids']))
            a['input_ids'][j+1] = ph
    for x,y in ans:
        a['input_ids'][x+1] = y
    final_output = tokenizer.convert_ids_to_tokens(a['input_ids'])
    if "<s>" in final_output:
        final_output.remove("<s>")
    if "</s>" in final_output:
        final_output.remove("</s>")
    if "" in final_output:
        final_output.remove("")
    if final_output[0] == '▁':
        final_output.pop(0)
    final_output = ''.join(final_output)
    final_output = final_output.replace("▁", " ")
    final_output = final_output.replace("", "")
    return final_output
