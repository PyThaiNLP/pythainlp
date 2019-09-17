# -*- coding: utf-8 -*-
"""
Visualization of text data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Collection, Callable, Tuple

__all__ = ['top_feats_label', 'top_feats_all', 'plot_top_feats']

def top_feats_label(X: np.ndarray, features: Collection[str], label_idx: Collection[bool] = None,
                    min_val: float = 0.1, agg_func: Callable = np.mean)->pd.DataFrame:
    '''
    original code (Thomas Buhrman)[from https://buhrmann.github.io/tfidf-analysis.html]
    rank features of each label by their encoded values (CountVectorizer, TfidfVectorizer, etc.)
    aggregated with `agg_func`
    :param X np.ndarray: document-value matrix
    :param features Collection[str]: feature names
    :param label_idx Collection[int]: position of rows with specified label
    :param min_val float: minimum value to take into account for each feature
    :param agg_func Callable: how to aggregate features such as `np.mean` or `np.sum`
    :return: a dataframe with `feature`, `score` and `ngram`
    '''
    res = X[label_idx] if label_idx is not None else X
    res[res < min_val] = 0
    res_agg = agg_func(res, axis=0)
    df = pd.DataFrame([(features[i], res_agg[i]) for i in np.argsort(res_agg)[::-1]])
    df.columns = ['feature','score']
    df['ngram'] = df.feature.map(lambda x: len(set(x.split(' '))))
    return df

def top_feats_all(X: np.ndarray, y: np.ndarray, features: Collection[str], min_val: float = 0.1, 
                  agg_func: Callable = np.mean)->Collection[pd.DataFrame]:
    '''
    original code (Thomas Buhrman)[from https://buhrmann.github.io/tfidf-analysis.html]
    for all labels, rank features of each label by their encoded values (CountVectorizer, TfidfVectorizer, etc.)
    aggregated with `agg_func`
    :param X np.ndarray: document-value matrix
    :param y np.ndarray: labels
    :param features Collection[str]: feature names
    :param min_val float: minimum value to take into account for each feature
    :param agg_func Callable: how to aggregate features such as `np.mean` or `np.sum`
    :return: a list of dataframes with `rank` (rank within label), `feature`, `score`, `ngram` and `label`
    '''
    labels = np.unique(y)
    dfs = []
    for l in labels:
        label_idx = (y==l)
        df = top_feats_label(X,features,label_idx,min_val,agg_func).reset_index()
        df['label'] = l
        df.columns = ['rank','feature','score','ngram','label']
        dfs.append(df)
    return dfs

def plot_top_feats(dfs: Collection[pd.DataFrame], top_n: int = 25, ngram_range: Tuple[int,int]=(1,2),)-> None:
    '''
    original code (Thomas Buhrman)[from https://buhrmann.github.io/tfidf-analysis.html]
    plot top features from a collection of `top_feats_all` dataframes
    :param dfs Collection[pd.DataFrame]: `top_feats_all` dataframes
    :param top_n int: number of top features to show
    :param ngram_range Tuple[int,int]: range of ngrams for features to show
    :return: nothing
    '''
    fig = plt.figure(figsize=(12, 9), facecolor="w")
    x = np.arange(top_n)
    for i, df in enumerate(dfs):
        df = df[(df.ngram>=ngram_range[0])&(df.ngram<=ngram_range[1])][:top_n]
        ax = fig.add_subplot(1, len(dfs), i+1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_frame_on(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel("score", labelpad=16, fontsize=14)
        ax.set_title(f"label = {str(df.label[0])}", fontsize=16)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
        ax.barh(x, df.score, align='center', color='#3F5D7D')
        ax.set_yticks(x)
        ax.set_ylim([-1, x[-1]+1])
        ax.invert_yaxis()
        yticks = ax.set_yticklabels(df.feature)
        plt.subplots_adjust(bottom=0.09, right=0.97, left=0.15, top=0.95, wspace=0.52)
    plt.show()
