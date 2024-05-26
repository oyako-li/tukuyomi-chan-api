# import pandas as pd
# import numpy as np
# from sklearn.manifold import TSNE
import torch
import json
import base64
from transformers import BertJapaneseTokenizer, BertModel
import sudachipy

# BERTの日本語モデル
MODEL_NAME = "cl-tohoku/bert-base-japanese-whole-word-masking"

# トークナイザとモデルのロード
tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME).to("mps")
# 各データの形式を整える
max_length = 256
dictionary = sudachipy.Dictionary()
morphy = dictionary.create(mode=sudachipy.SplitMode.C)


def morphogenesis(text: str):
    morphemes = morphy.tokenize(text)
    return [m.surface() for m in morphemes]


def tokenize(text: str):
    encoding = tokenizer(
        text,
        max_length=max_length,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    encoding = {k: v.to("mps") for k, v in encoding.items()}
    return encoding


def vectorise(encoding: dict):
    # 文章ベクトルを計算
    attention_mask = encoding["attention_mask"]
    with torch.no_grad():
        output = model(**encoding)
        last_hidden_state = output.last_hidden_state
        averaged_hidden_state = (last_hidden_state * attention_mask.unsqueeze(-1)).sum(
            1
        ) / attention_mask.sum(1, keepdim=True)

    sentence_vector = averaged_hidden_state[0].cpu().numpy()
    return sentence_vector
