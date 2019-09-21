# -*- coding: utf-8 -*-
"""
Code by Charin Polpanumas
https://github.com/cstorm125/thai2fit/
"""
import collections
import re

from typing import List, Collection, Callable
import emoji
import html
import numpy as np
import torch

from pythainlp.corpus import download, get_corpus, get_corpus_path
from pythainlp.tokenize import Tokenizer
from pythainlp.util import normalize as normalize_char_order

'''
# Fastai dependencies
The following codes are copied from
https://github.com/fastai/fastai/blob/master/fastai/text/transform.py
in order to avoid importing the entire fastai library
'''

UNK = 'xxunk'
TK_REP = 'xxrep'
TK_WREP = 'xxwrep'
TK_END = 'xxend'
TK_URL ='xxurl'

class BaseTokenizer():
    """Basic class for a tokenizer function. (code from `fastai`)"""
    def __init__(self, lang: str): self.lang = lang

    def tokenizer(self, t: str) -> List[str]: return t.split(' ')

    def add_special_cases(self, toks: Collection[str]): pass
    
def replace_url(x):
    """
        Replace url in `x` with TK_URL

        :param str x: text to replace url

        :return: text where urls  are replaced
        :rtype: str

        :Example:

            >>> from pythainlp.ulmfit import replace_url
            >>> replace_url("go to github.com")
            go to xxurl
    """    
    URL_PATTERN = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    return re.sub(URL_PATTERN, TK_URL, x)


def fix_html(x: str) -> str:
    """
        List of replacements from html strings in `x`. (code from `fastai`)

        :param str x: text to replace html string

        :return: text where html strings are replaced
        :rtype: str

        :Example:

            >>> from pythainlp.ulmfit import fix_html
            >>> fix_html("Anbsp;amp;nbsp;B @.@ ")
            A & B.
    """
    re1 = re.compile(r'  +')
    x = x.replace('#39;', "'").replace('amp;', '&').replace(
        '#146;', "'").replace('nbsp;', ' ').replace(
        '#36;', '$').replace('\\n', "\n").replace('quot;', "'").replace(
        '<br />', "\n").replace('\\"', '"').replace('<unk>', UNK).replace(
        ' @.@ ', '.').replace(' @-@ ', '-').replace(' @,@ ', ',').replace(
        '\\', ' \\ ')
    return re1.sub(' ', html.unescape(x))


def rm_useless_spaces(t: str) -> str:
    """Remove multiple spaces in `t`. (code from `fastai`)"""
    return re.sub(' {2,}', ' ', t)


def spec_add_spaces(t: str) -> str:
    """Add spaces around / and # in `t`. \n (code from `fastai`)"""
    return re.sub(r'([/#\n])', r' \1 ', t)

'''
End of fastai codes
'''

__all__ = [
    "ThaiTokenizer",
    "document_vector",
    "merge_wgts",
    "pre_rules_th",
    "post_rules_th",
    "pre_rules_th_sparse",
    "post_rules_th_sparse",
    "process_thai",
    "_THWIKI_LSTM",
]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_MODEL_NAME_LSTM = "wiki_lm_lstm"
_ITOS_NAME_LSTM = "wiki_itos_lstm"

_THAI2FIT_WORDS = get_corpus("words_th_thai2fit_201810.txt")
_pythainlp_tokenizer = Tokenizer(custom_dict=_THAI2FIT_WORDS, engine="newmm")


# Download pretrained models
def _get_path(fname: str) -> str:
    """
    :meth: download get path of file from pythainlp-corpus
    :param str fname: file name
    :return: path to downloaded file
    """
    path = get_corpus_path(fname)
    if not path:
        download(fname)
        path = get_corpus_path(fname)
    return path


# Custom fastai tokenizer
class ThaiTokenizer(BaseTokenizer):
    """
    Wrapper around a frozen newmm tokenizer to make it a
    :class:`fastai.BaseTokenizer`.
    (see: https://docs.fast.ai/text.transform#BaseTokenizer)
    """

    def __init__(self, lang: str = "th"):
        self.lang = lang

    @staticmethod
    def tokenizer(text: str) -> List[str]:
        """
        This function tokenizes text with *newmm* engine and the dictionary
        specifically for `ulmfit` related functions
        (see: `Dictonary file (.txt) \
        <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/words_th_thai2fit_201810.txt>`_).
        :meth: tokenize text with a frozen newmm engine
        :param str text: text to tokenize
        :return: tokenized text
        :rtype: list[str]

        :Example:

            Using :func:`pythainlp.ulmfit.ThaiTokenizer.tokenizer` is
            similar to :func:`pythainlp.tokenize.word_tokenize`
            with *ulmfit* engine.

            >>> from  pythainlp.ulmfit import ThaiTokenizer
            >>> from  pythainlp.tokenize import word_tokenize
            >>>
            >>> text = "อาภรณ์, จินตมยปัญญา ภาวนามยปัญญา"
            >>> ThaiTokenizer.tokenizer(text)
             ['อาภรณ์', ',', ' ', 'จิน', 'ตม', 'ย', 'ปัญญา',
             ' ', 'ภาวนามยปัญญา']
            >>>
            >>> word_tokenize(text, engine='ulmfit')
            ['อาภรณ์', ',', ' ', 'จิน', 'ตม', 'ย', 'ปัญญา',
             ' ', 'ภาวนามยปัญญา']

        """
        return _pythainlp_tokenizer.word_tokenize(text)

    def add_special_cases(self, toks):
        pass


def replace_rep_after(text: str) -> str:
    """
    Replace repetitions at the character level in `text` after the repetition.
    This is done to prevent such case as 'น้อยยยยยยยย' becoming 'น้อ xxrep 8 ย'
    ;instead it will retain the word as 'น้อย xxrep 8'

    :param str text: input text to replace character repetition

    :return: text with repetitive token **xxrep** and the counter
             after character repetition

    :rtype: str
    :Example:

        >>> from pythainlp.ulmfit import replace_rep_after
        >>>
        >>> text = "กาาาาาาา"
        >>> replace_rep_after(text)
        'กาxxrep7 '
    """

    def _replace_rep(m):
        c, cc = m.groups()
        return f"{c}{TK_REP}{len(cc)+1} "

    re_rep = re.compile(r"(\S)(\1{3,})")

    return re_rep.sub(_replace_rep, text)


def replace_wrep_post(toks: Collection):
    """
    Replace reptitive words post tokenization;
    fastai `replace_wrep` does not work well with Thai.

    :param list[str] toks: list of tokens

    :return: list of tokens where **xxwrep** token and the counter
             is added in front of repetitive words.
    :rtype: list[str]

    :Example:

        >>> from pythainlp.ulmfit import replace_wrep_post_nonum
        >>>
        >>> toks = ["กา", "น้ำ", "น้ำ", "น้ำ", "น้ำ"]
        >>> replace_wrep_post(toks)
        ['กา', 'xxwrep', '3', 'น้ำ']

    """
    previous_word = None
    rep_count = 0
    res = []
    for current_word in toks+[TK_END]:
        if current_word == previous_word:
            rep_count += 1
        elif (current_word != previous_word) & (rep_count > 0):
            res += [TK_WREP, str(rep_count), previous_word]
            rep_count = 0
        else:
            res.append(previous_word)
        previous_word = current_word
    return res[1:]


def rm_useless_newlines(text: str) -> str:
    "Remove multiple newlines in `text`."

    return re.sub(r"[\n]{2,}", " ", text)


def rm_brackets(text: str) -> str:
    "Remove all empty brackets from `t`."
    new_line = re.sub(r"\(\)", "", text)
    new_line = re.sub(r"\{\}", "", new_line)
    new_line = re.sub(r"\[\]", "", new_line)

    return new_line


def ungroup_emoji(toks: Collection):
    "Ungroup emojis"
    res = []
    for tok in toks:
        if emoji.emoji_count(tok) == len(tok):
            for char in tok:
                res.append(char)
        else:
            res.append(tok)
    return res


def lowercase_all(toks: Collection):
    """Lowercase all English words;
    English words in Thai texts don't usually have nuances of capitalization.
    """
    return [tok.lower() for tok in toks]


def replace_rep_nonum(text: str) -> str:
    """
    Replace repetitions at the character level in `text` after the repetition.
    This is done to prevent such case as 'น้อยยยยยยยย' becoming 'น้อ xxrep ย';
    instead it will retain the word as 'น้อย xxrep '

    :param str text: input text to replace character repetition

    :return: text with repetitive token **xxrep** after
             character repetition
    :rtype: str

    :Example:

        >>> from pythainlp.ulmfit import replace_rep_nonum
        >>>
        >>> text = "กาาาาาาา"
        >>> replace_rep_nonum(text)
        'กา xxrep '

    """
    def _replace_rep(m):
        c, cc = m.groups()
        return f"{c} {TK_REP} "
    re_rep = re.compile(r"(\S)(\1{3,})")
    return re_rep.sub(_replace_rep, text)


def replace_wrep_post_nonum(toks: Collection):
    """
    Replace reptitive words post tokenization;
    fastai `replace_wrep` does not work well with Thai.

    :param list[str] toks: list of tokens

    :return: list of tokens where **xxwrep** token is added in front of
             repetitive words.
    :rtype: list[str]

    :Example:

        >>> from pythainlp.ulmfit import replace_wrep_post_nonum
        >>>
        >>> toks = ["กา", "น้ำ", "น้ำ", "น้ำ", "น้ำ"]
        >>> replace_wrep_post_nonum(toks)
        ['กา', 'xxwrep', 'น้ำ']

    """
    previous_word = None
    rep_count = 0
    res = []
    for current_word in toks+[TK_END]:
        if current_word == previous_word:
            rep_count += 1
        elif (current_word != previous_word) & (rep_count > 0):
            res += [TK_WREP, previous_word]
            rep_count = 0
        else:
            res.append(previous_word)
        previous_word = current_word
    return res[1:]


def remove_space(toks: Collection):
    """
    Do not include space for bag-of-word models.

    :param list[str] toks: list of tokens

    :return: list of tokens where space tokens (" ") are filtered out
    :rtype: list[str]
    """
    res = []
    for t in toks:
        if t != ' ':
            res.append(t)
    return res

# Pretrained paths
# TODO: Let the user decide if they like to download (at setup?)
_THWIKI_LSTM = dict(
    wgts_fname=_get_path(_MODEL_NAME_LSTM),
    itos_fname=_get_path(_ITOS_NAME_LSTM)
)

# Preprocessing rules for Thai text
# dense features
pre_rules_th = [
    replace_rep_after,
    fix_html,
    normalize_char_order,
    spec_add_spaces,
    rm_useless_spaces,
    rm_useless_newlines,
    rm_brackets,
    replace_url,
]

post_rules_th = [replace_wrep_post, ungroup_emoji, lowercase_all,]
# sparse features
pre_rules_th_sparse = pre_rules_th[1:] + [replace_rep_nonum]
post_rules_th_sparse = post_rules_th[1:] + [replace_wrep_post_nonum,
                                            remove_space]


def process_thai(text: str, pre_rules: Collection = pre_rules_th_sparse,
                 tok_func: Callable = _pythainlp_tokenizer.word_tokenize,
                 post_rules: Collection = post_rules_th_sparse) -> Collection[str]:
    """
    Process Thai texts for models (with sparse features as default)

    :param str text: text to be cleaned
    :param list[func] pre_rules: rules to apply before tokenization.
    :param func tok_func: tokenization function (by default, **tok_func** is
                          :func:`pythainlp.tokenize.word_tokenize`)

    :param list[func]  post_rules: rules to apply after tokenizations

    :return: a list of cleaned tokenized texts
    :rtype: list[str]


    :Note:
      - The default **pre-rules** consists of :func:`fix_html`,
        :func:`pythainlp.util.normalize`,
        :func:`spec_add_spaces`,
        :func:`rm_useless_spaces`,
        :func:`rm_useless_newlines`,
        :func:`rm_brackets`
        and :func:`replace_rep_nonum`.

      - The default **post-rules** consists of :func:`ungroup_emoji`,
        :func:`lowercase_all`,  :func:`replace_wrep_post_nonum`,
        and :func:`remove_space`.

    :Example:

        1. Use default pre-rules and post-rules:

        >>> from pythainlp.ulmfit import process_thai
        >>> text = "บ้านนนนน () อยู่นานนานนาน 😂🤣😃😄😅 PyThaiNLP amp;     "
        >>> process_thai(text)
        [บ้าน', 'xxrep', '   ', 'อยู่', 'xxwrep', 'นาน', '😂', '🤣',
        '😃', '😄', '😅', 'pythainlp', '&']

        2. Modify pre_rules and post_rules arugments with
           rules provided in :mod:`pythainlp.ulmfit`:

        >>> from pythainlp.ulmfit import (
            process_thai,
            replace_rep_after,
            fix_html,
            ungroup_emoji,
            replace_wrep_post,
            remove_space)
        >>>
        >>> text = "บ้านนนนน () อยู่นานนานนาน 😂🤣😃😄😅 PyThaiNLP amp;     "
        >>> process_thai(text,
                         pre_rules=[replace_rep_after, fix_html],
                         post_rules=[ungroup_emoji,
                                     replace_wrep_post,
                                     remove_space]
                        )
        ['บ้าน', 'xxrep', '5', '()', 'อยู่', 'xxwrep', '2', 'นาน', '😂', '🤣',
         '😃', '😄', '😅', 'PyThaiNLP', '&']


    """
    res = text
    for pre in pre_rules:
        res = pre(res)
    res = tok_func(res)
    for post in post_rules:
        res = post(res)
    return res

_tokenizer = ThaiTokenizer()


def document_vector(text: str, learn, data, agg: str = "mean"):
    """
    This function vectorize Thai input text into a 400 dimension vector using
    :class:`fastai` language model and data bunch.

    :meth: `document_vector` get document vector using fastai language model
           and data bunch
    :param str text: text to be vectorized with :class:`fastai` language model.
    :param learn: :class:`fastai` language model learner
    :param data: :class:`fastai` data bunch
    :param str agg: name of aggregation methods for word embeddings
                    The avialable methods are "mean" and "sum"

    :return: :class:`numpy.array` of document vector sized 400 based on
             the encoder of the model
    :rtype: :class:`numpy.ndarray((1, 400))`

    :Example:

        >>> from pythainlp.ulmfit import document_vectorr
        >>> from fastai import *
        >>> from fastai.text import *
        >>>
        >>> # Load Data Bunch
        >>> data = load_data(MODEL_PATH, 'thwiki_lm_data.pkl')
        >>>
        >>> # Initialize language_model_learner
        >>> config = dict(emb_sz=400, n_hid=1550, n_layers=4, pad_token=1,
             qrnn=False, tie_weights=True, out_bias=True, output_p=0.25,
             hidden_p=0.1, input_p=0.2, embed_p=0.02, weight_p=0.15)
        >>> trn_args = dict(drop_mult=0.9, clip=0.12, alpha=2, beta=1)
        >>> learn = language_model_learner(data, AWD_LSTM, config=config,
                                           pretrained=False, **trn_args)
        >>> document_vector('วันนี้วันดีปีใหม่', learn, data)

    :See Also:
        * A notebook showing how to train `ulmfit` language model and its
          usage, `Jupyter Notebook \
          <https://github.com/cstorm125/thai2fit/blob/master/thwiki_lm/word2vec_examples.ipynb>`_

    """

    s = _tokenizer.tokenizer(text)
    t = torch.tensor(data.vocab.numericalize(s),
                     requires_grad=False).to(device)
    m = learn.model[0].encoder.to(device)
    res = m(t).cpu().detach().numpy()
    if agg == "mean":
        res = res.mean(0)
    elif agg == "sum":
        res = res.sum(0)
    else:
        raise ValueError("Aggregate by mean or sum")

    return res


def merge_wgts(em_sz, wgts, itos_pre, itos_new):
    """
    This function is to insert new vocab into an existing model named `wgts`
    and update the model's weights for new vocab with the average embedding.

    :meth: `merge_wgts` insert pretrained weights and vocab into a new set
           of weights and vocab; use average if vocab not in pretrained vocab
    :param int em_sz: embedding size
    :param wgts: torch model weights
    :param list itos_pre: pretrained list of vocab
    :param list itos_new: list of new vocab

    :return: merged torch model weights
    """
    vocab_size = len(itos_new)
    enc_wgts = wgts["0.encoder.weight"].numpy()

    # Average weight of encoding
    row_m = enc_wgts.mean(0)
    stoi_pre = collections.defaultdict(
        lambda: -1, {v: k for k, v in enumerate(itos_pre)}
    )

    # New embedding based on classification dataset
    new_w = np.zeros((vocab_size, em_sz), dtype=np.float32)

    for i, w in enumerate(itos_new):
        r = stoi_pre[w]
        # Use pretrianed embedding if present; else use the average
        new_w[i] = enc_wgts[r] if r >= 0 else row_m

    wgts["0.encoder.weight"] = torch.tensor(new_w)
    wgts["0.encoder_dp.emb.weight"] = torch.tensor(np.copy(new_w))
    wgts["1.decoder.weight"] = torch.tensor(np.copy(new_w))

    return wgts
