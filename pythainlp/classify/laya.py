# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Laya Multilingual model for zero-shot text classification and decision making.

Laya is a non-autoregressive decision model designed for System 1 thinking
that performs typed choices, scoring, and binary decisions over text
in a single forward pass without task-specific fine-tuning.
"""

from __future__ import annotations

import json
import math
import os
from typing import Any, Dict, Optional, Union

from pythainlp.corpus import get_hf_hub
from pythainlp.tools import safe_path_join

_DEFAULT_REPO_ID = "pythainlp/laya-multilingual-onnx"

_QTYPES: Dict[str, int] = {"choice": 0, "score": 1, "noul": 2}
_QTYPE_NAMES: Dict[int, str] = {0: "choice", 1: "score", 2: "noul"}

_TEMP_MIN: float = 0.5
_TEMP_MAX: float = 5.0


def _clamp_temperature(
    temperature: Any, lo: float = _TEMP_MIN, hi: float = _TEMP_MAX
) -> float:
    """
    Clamp temperature to a valid range [lo, hi].

    :param Any temperature: Temperature value to clamp.
    :param float lo: Minimum allowed temperature.
    :param float hi: Maximum allowed temperature.
    :return: Clamped temperature float.
    :rtype: float
    """
    try:
        t = float(temperature)
    except (TypeError, ValueError):
        return 1.0
    if not math.isfinite(t):
        return 1.0
    return min(hi, max(lo, t))


def _confidence_from_probs(probs: Any, num_options: int) -> float:
    """
    Calculate normalized Shannon entropy confidence: 1 - H(p) / log(k).

    :param Any probs: 1D probability array.
    :param int num_options: Number of active options.
    :return: Confidence value between 0.0 and 1.0.
    :rtype: float
    """
    import numpy as np

    if num_options < 2:
        return 1.0
    p = probs[:num_options]
    entropy = -(p * np.log(np.clip(p, 1e-12, 1.0))).sum()
    confidence = 1.0 - (entropy / math.log(num_options))
    return float(np.clip(confidence, 0.0, 1.0))


def _temp_bucket(qtype: int, num_options: int) -> str:
    """
    Return temperature bucket string for given question type and option count.

    :param int qtype: Question type integer (0: choice, 1: score, 2: noul).
    :param int num_options: Number of options.
    :return: Bucket name string, e.g. 'choice:3-5'.
    :rtype: str
    """
    if num_options <= 2:
        size = "2"
    elif num_options <= 5:
        size = "3-5"
    elif num_options <= 10:
        size = "6-10"
    else:
        size = "11+"
    return f"{_QTYPE_NAMES[qtype]}:{size}"


def _serialize_state(state: Union[str, dict[str, Any], list[Any]]) -> str:
    """
    Serialize text or structured state to string.

    :param Union[str, dict[str, Any], list[Any]] state: State to serialize.
    :return: String representation.
    :rtype: str
    """
    if isinstance(state, str):
        return state
    return json.dumps(state, ensure_ascii=False)


def _render_criterion(value: Any) -> str:
    """
    Render one criterion value as a clean string.

    :param Any value: Criterion text, dictionary, list, or number.
    :return: Rendered text representation.
    :rtype: str
    """
    if isinstance(value, str):
        return value
    return json.dumps(
        value, ensure_ascii=False, separators=(", ", ": "), default=str
    )


def _render_options(q: dict[str, Any]) -> list[str]:
    """
    Render option texts for a question definition.

    :param dict[str, Any] q: Question dictionary with keys 't' and 'crit'.
    :return: List of rendered option strings.
    :rtype: list[str]
    """
    q_type = q["t"]
    criteria = q.get("crit")
    if q_type == "choice":
        if not isinstance(criteria, dict):
            return []
        return [
            k
            if v is None or v == ""
            else f"{k}: {_render_criterion(v)}"
            for k, v in criteria.items()
        ]
    if q_type == "score":
        if not isinstance(criteria, list):
            return []
        return [
            f"level {i}: {_render_criterion(c)}"
            for i, c in enumerate(criteria)
        ]
    # noul (yes/no)
    crit_dict = criteria if isinstance(criteria, dict) else {}
    false_crit = crit_dict.get("false")
    true_crit = crit_dict.get("true")
    false_desc = (
        _render_criterion(false_crit)
        if false_crit not in (None, "")
        else "no, the statement does not hold"
    )
    true_desc = (
        _render_criterion(true_crit)
        if true_crit not in (None, "")
        else "yes, the statement holds"
    )
    return [f"false: {false_desc}", f"true: {true_desc}"]


class _TokenizerWrapper:
    """Lightweight wrapper around FastTokenizer (tokenizers or transformers)."""

    cls_token: str
    cls_token_id: int
    sep_token: str
    sep_token_id: int
    pad_token: str
    pad_token_id: int
    mask_token: str
    mask_token_id: int

    def __init__(self, tok_json_path: str, tok_config_path: str) -> None:
        try:
            from tokenizers import Tokenizer as FastTokenizer

            self._backend: Any = FastTokenizer.from_file(tok_json_path)
            self._backend.no_padding()
            self._backend.no_truncation()
            self._is_hf_tokenizer = False
        except ModuleNotFoundError:
            try:
                from transformers import AutoTokenizer

                tok_dir = os.path.dirname(tok_json_path)
                self._backend = AutoTokenizer.from_pretrained(tok_dir)
                self._is_hf_tokenizer = True
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    "Please install tokenizers or transformers via "
                    "'pip install tokenizers' or 'pip install transformers'."
                ) from exc

        with open(tok_config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        for name in ("cls_token", "sep_token", "pad_token", "mask_token"):
            value = config.get(name)
            if isinstance(value, dict):
                value = value.get("content")
            if not isinstance(value, str):
                raise ValueError(f"Tokenizer configuration is missing {name}")
            if self._is_hf_tokenizer:
                token_id = self._backend.convert_tokens_to_ids(value)
            else:
                token_id = self._backend.token_to_id(value)
            if token_id is None:
                raise ValueError(f"Tokenizer cannot map token {value!r}")
            setattr(self, name, value)
            setattr(self, f"{name}_id", int(token_id))

    def __call__(
        self, text: str, add_special_tokens: bool = False
    ) -> dict[str, list[int]]:
        if self._is_hf_tokenizer:
            tokens = self._backend(
                text, add_special_tokens=add_special_tokens
            )["input_ids"]
        else:
            tokens = self._backend.encode(
                text, add_special_tokens=add_special_tokens
            ).ids
        return {"input_ids": tokens}


def _build_prefix(
    tok: _TokenizerWrapper,
    q: dict[str, Any],
    head_max_len: int = 256,
) -> tuple[list[int], list[int]]:
    """
    Build question prefix tokens and marker positions.

    :param _TokenizerWrapper tok: Tokenizer wrapper.
    :param dict[str, Any] q: Internal question definition.
    :param int head_max_len: Maximum length for question header.
    :return: Tuple of (input_ids, marker_positions).
    :rtype: tuple[list[int], list[int]]
    """
    opts = _render_options(q)
    ins = str(q["ins"]).replace(tok.mask_token, " ")
    head_ids = tok(f"{q['t']} question: {ins}", add_special_tokens=False)[
        "input_ids"
    ]
    opt_ids: list[list[int]] = []
    for opt_text in opts:
        encoded_opt = tok(
            " " + opt_text.replace(tok.mask_token, " "),
            add_special_tokens=False,
        )["input_ids"][:48]
        opt_ids.append([tok.mask_token_id] + encoded_opt)

    opt_budget = head_max_len - sum(len(o) for o in opt_ids)
    if opt_budget < 16:
        per = max(4, (head_max_len - 16) // max(1, len(opt_ids)))
        opt_ids = [o[:per] for o in opt_ids]
        opt_budget = head_max_len - sum(len(o) for o in opt_ids)

    head_ids = head_ids[: max(8, opt_budget)]
    ids = [tok.cls_token_id] + head_ids + [tok.sep_token_id]
    markers: list[int] = []
    for opt in opt_ids:
        markers.append(len(ids))
        ids.extend(opt)
    ids.append(tok.sep_token_id)
    return ids, markers


def _build_sequence(
    tok: _TokenizerWrapper,
    state: Union[str, dict[str, Any], list[Any]],
    q: dict[str, Any],
    max_len: int = 1024,
    head_max_len: int = 256,
    truncate_left: bool = False,
) -> tuple[list[int], list[int]]:
    ""
    "Build token sequence: [CLS] <type> ins [SEP] [MASK] opt0 ... [SEP] state [SEP].

    :param _TokenizerWrapper tok: Tokenizer instance.
    :param Union[str, dict[str, Any], list[Any]] state: Input state/text.
    :param dict[str, Any] q: Question definition.
    :param int max_len: Maximum total sequence length.
    :param int head_max_len: Maximum prefix/header length.
    :param bool truncate_left: Whether to truncate state from left instead of right.
    :return: Tuple of (input_ids, marker_positions).
    :rtype: tuple[list[int], list[int]]
    """
    ids, markers = _build_prefix(tok, q, head_max_len)
    room = max(0, max_len - len(ids) - 1)
    state_str = _serialize_state(state).replace(tok.mask_token, " ")
    st = tok(state_str, add_special_tokens=False)["input_ids"]
    st = st[-room:] if truncate_left else st[:room]
    ids = ids + st + [tok.sep_token_id]
    return ids[:max_len], [m for m in markers if m < max_len]


def _collate_items(
    items: list[dict[str, Any]], pad_id: int
) -> dict[str, Any]:
    """
    Collate sequence items into numpy batch feed dict for ONNX Runtime.

    :param list[dict[str, Any]] items: List of prepared items.
    :param int pad_id: Padding token ID.
    :return: Batch feed dictionary.
    :rtype: dict[str, Any]
    """
    import numpy as np

    if not items:
        raise ValueError("Cannot collate an empty batch.")
    n = len(items)
    length = max(len(item["ids"]) for item in items)
    count = max(2, max(len(item["markers"]) for item in items))

    batch = {
        "input_ids": np.full((n, length), pad_id, dtype=np.int64),
        "attention_mask": np.zeros((n, length), dtype=np.int64),
        "marker_pos": np.zeros((n, count), dtype=np.int64),
        "marker_mask": np.zeros((n, count), dtype=bool),
        "qtype": np.array([item["qtype"] for item in items], dtype=np.int64),
    }
    for i, item in enumerate(items):
        item_len = len(item["ids"])
        item_cnt = len(item["markers"])
        batch["input_ids"][i, :item_len] = item["ids"]
        batch["attention_mask"][i, :item_len] = 1
        batch["marker_pos"][i, :item_cnt] = item["markers"]
        batch["marker_mask"][i, :item_cnt] = True
    return batch


class LayaModel:
    """
    Laya Multilingual model for zero-shot text classification and decision making.

    Laya is a non-autoregressive decision model designed for fast, calibrated,
    and reliable decision making. It supports over 100 languages including Thai,
    allowing zero-shot classification using an instruction prompt and candidate
    choices without any task-specific fine-tuning.

    :param Optional[str] model_path: Hugging Face model repository ID or
        local directory path containing the ONNX model files.
        Default is ``"pythainlp/laya-multilingual-onnx"``.
    :param Optional[list[str]] providers: List of ONNX Runtime execution
        providers (e.g. ``["CPUExecutionProvider"]``,
        ``["CUDAExecutionProvider"]``). Default is ``["CPUExecutionProvider"]``.
    :param Optional[str] revision: Git revision (branch, tag, or commit hash)
        on Hugging Face Hub (optional).
    :param int batch_size: Batch size for batched inference (default: 16).
    :param Optional[int] max_length: Maximum sequence length in tokens
        (default from configuration, typically 1024).
    :param Optional[int] head_max_length: Maximum token length for the question
        header and candidate options (default from configuration, typically 256).

    :Example:
        >>> from pythainlp.classify import LayaModel  # doctest: +SKIP
        >>> model = LayaModel()  # doctest: +SKIP
        >>> model.classify(  # doctest: +SKIP
        ...     "อาหารอร่อยมาก บรรยากาศดี พนักงานบริการยอดเยี่ยม",
        ...     choices=["Positive", "Negative", "Neutral"],
        ...     prompt="What is the sentiment of the text?",
        ... )
        'Positive'
    """

    model_path: str
    providers: list[str]
    batch_size: int

    def __init__(
        self,
        model_path: Optional[str] = None,
        providers: Optional[list[str]] = None,
        revision: Optional[str] = None,
        batch_size: int = 16,
        max_length: Optional[int] = None,
        head_max_length: Optional[int] = None,
    ) -> None:
        try:
            import numpy as np  # noqa: F401
            import onnxruntime as ort
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "Please install the required packages via "
                "'pip install numpy onnxruntime huggingface-hub tokenizers'."
            ) from exc

        if not isinstance(batch_size, int) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer.")

        self.batch_size = batch_size
        self.providers = (
            providers if providers is not None else ["CPUExecutionProvider"]
        )

        model_file, rl_cfg_file, tok_file, tok_cfg_file = self._resolve_files(
            model_path, revision
        )
        self.model_path = model_file

        self._session = ort.InferenceSession(
            model_file, providers=self.providers
        )
        self._tokenizer = _TokenizerWrapper(tok_file, tok_cfg_file)

        cfg: dict[str, Any] = {}
        if rl_cfg_file and os.path.isfile(rl_cfg_file):
            try:
                with open(rl_cfg_file, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            except Exception:
                cfg = {}

        self._max_len: int = (
            max_length if max_length is not None else int(cfg.get("max_len", 1024))
        )
        self._head_max_len: int = (
            head_max_length
            if head_max_length is not None
            else int(cfg.get("head_max_len", 256))
        )

        raw_temps = cfg.get("temperature", [1.0, 1.0, 1.0])
        self._temperature: list[float] = [
            _clamp_temperature(t) for t in raw_temps
        ]
        raw_opt_temps = cfg.get("temperature_by_options", {})
        self._temperature_by_options: dict[str, float] = {
            k: _clamp_temperature(v) for k, v in raw_opt_temps.items()
        }

    @staticmethod
    def _resolve_files(
        model_path: Optional[str], revision: Optional[str]
    ) -> tuple[str, Optional[str], str, str]:
        """Resolve file paths for model, configs, and tokenizer."""
        if model_path is not None and os.path.isdir(model_path):
            model_file = safe_path_join(model_path, "model.onnx")
            rl_cfg_file: Optional[str] = safe_path_join(
                model_path, "rl_agent_config.json"
            )
            if not os.path.isfile(rl_cfg_file):
                rl_cfg_file = None

            tok_dir = safe_path_join(model_path, "tokenizer")
            if os.path.isdir(tok_dir):
                tok_file = safe_path_join(tok_dir, "tokenizer.json")
                tok_cfg_file = safe_path_join(tok_dir, "tokenizer_config.json")
            else:
                tok_file = safe_path_join(model_path, "tokenizer.json")
                tok_cfg_file = safe_path_join(
                    model_path, "tokenizer_config.json"
                )
            return model_file, rl_cfg_file, tok_file, tok_cfg_file

        repo_id = (
            model_path if model_path is not None else _DEFAULT_REPO_ID
        )
        model_file = get_hf_hub(repo_id, "model.onnx", revision=revision)
        try:
            rl_cfg_file = get_hf_hub(
                repo_id, "rl_agent_config.json", revision=revision
            )
        except Exception:
            rl_cfg_file = None

        tok_file = get_hf_hub(
            repo_id, "tokenizer/tokenizer.json", revision=revision
        )
        tok_cfg_file = get_hf_hub(
            repo_id, "tokenizer/tokenizer_config.json", revision=revision
        )
        return model_file, rl_cfg_file, tok_file, tok_cfg_file

    @staticmethod
    def _to_internal(qdef: dict[str, Any]) -> dict[str, Any]:
        """Validate and convert user question definition to internal format."""
        if not isinstance(qdef, dict):
            raise ValueError("Each question definition must be a dictionary.")
        qtype = qdef.get("type")
        if qtype not in _QTYPES:
            raise ValueError(
                f"Unknown question type {qtype!r}; expected 'choice', 'score', or 'noul'."
            )
        if "instructions" not in qdef:
            raise ValueError("Question definition is missing 'instructions'.")

        criteria = qdef.get("criteria")
        if qtype == "choice":
            if isinstance(criteria, list):
                if not criteria:
                    raise ValueError("Choice criteria list must not be empty.")
                if not all(isinstance(c, str) for c in criteria):
                    raise ValueError("Choice labels must be strings.")
                if len(set(criteria)) != len(criteria):
                    raise ValueError("Choice labels must be unique.")
                criteria = dict.fromkeys(criteria)
            if not isinstance(criteria, dict) or not criteria:
                raise ValueError(
                    "Choice criteria must be a non-empty dictionary or list."
                )
            if not all(isinstance(k, str) for k in criteria):
                raise ValueError("Choice labels must be strings.")
        elif qtype == "score":
            if not isinstance(criteria, list) or not criteria:
                raise ValueError("Score criteria must be a non-empty list.")
        elif criteria is not None and not isinstance(criteria, dict):
            raise ValueError(
                "Noul criteria must be a dictionary with false/true descriptions."
            )

        instructions = qdef["instructions"]
        if not isinstance(instructions, str):
            instructions = json.dumps(instructions, ensure_ascii=False)

        return {"t": qtype, "ins": instructions, "crit": criteria}

    def system_one(
        self,
        state: Union[str, dict[str, Any], list[Any]],
        questions: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute typed-decision questions over state (upstream Laya System 1 interface).

        Supports question types:
        - ``choice``: Select best option among criteria.
        - ``score``: Ordinal evaluation across score criteria.
        - ``noul``: Binary yes/no statement evaluation.

        :param Union[str, dict[str, Any], list[Any]] state: Context or document to evaluate.
        :param dict[str, Any] questions: Dictionary of question definitions keyed by question ID.
        :return: Dictionary containing ``"model"``, ``"answers"``, and token ``"usage"``.
        :rtype: dict[str, Any]
        """
        import numpy as np

        if not isinstance(questions, dict) or not questions:
            raise ValueError("questions must be a non-empty dictionary.")

        items: list[dict[str, Any]] = []
        internal: list[dict[str, Any]] = []
        qids = list(questions.keys())

        for qid in qids:
            q = self._to_internal(questions[qid])
            ids, markers = _build_sequence(
                self._tokenizer,
                state,
                q,
                max_len=self._max_len,
                head_max_len=self._head_max_len,
            )
            if len(markers) != len(_render_options(q)):
                raise ValueError(
                    f"Question {qid!r} has too many options for token budget."
                )
            items.append(
                {"ids": ids, "markers": markers, "qtype": _QTYPES[q["t"]]}
            )
            internal.append(q)

        answers: dict[str, Any] = {}
        for start in range(0, len(items), self.batch_size):
            chunk = items[start : start + self.batch_size]
            batch = _collate_items(chunk, self._tokenizer.pad_token_id)
            logits_out, act_out = self._session.run(None, batch)
            logits = np.asarray(logits_out, dtype=np.float32)
            act = np.asarray(act_out, dtype=np.float32)

            exp_act = np.exp(act - np.max(act, axis=-1, keepdims=True))
            act_probs = exp_act / np.sum(exp_act, axis=-1, keepdims=True)

            for row, item in enumerate(chunk):
                qid = qids[start + row]
                q = internal[start + row]
                k = len(item["markers"])
                qt = item["qtype"]
                bucket = _temp_bucket(qt, k)
                scale = self._temperature_by_options.get(
                    bucket, self._temperature[qt]
                )
                z = logits[row, :k] / scale
                exp_z = np.exp(z - np.max(z))
                p = exp_z / np.sum(exp_z)

                answer: dict[str, Any] = {
                    "type": q["t"],
                    "confidence": round(_confidence_from_probs(p, k), 4),
                    "action": {
                        "act_probability": round(float(act_probs[row, 0]), 4)
                    },
                }

                if q["t"] == "choice":
                    labels = list(q["crit"])
                    answer.update(
                        choice=labels[int(p.argmax())],
                        probabilities={
                            label: round(float(v), 4)
                            for label, v in zip(labels, p)
                        },
                    )
                elif q["t"] == "score":
                    answer.update(
                        score=round(float((np.arange(k) * p).sum()), 4),
                        legend={
                            str(i): value for i, value in enumerate(q["crit"])
                        },
                        probabilities={
                            str(i): round(float(v), 4)
                            for i, v in enumerate(p)
                        },
                    )
                else:
                    true_prob = float(p[1])
                    answer.update(
                        noul=round(true_prob, 4),
                        confidence=round(max(true_prob, 1.0 - true_prob), 4),
                    )
                answers[qid] = answer

        return {
            "model": "laya-multilingual-onnx",
            "answers": answers,
            "usage": {
                "input_tokens": sum(len(it["ids"]) for it in items),
                "output_tokens": 0,
            },
        }

    def classify(
        self,
        text: Union[str, dict[str, Any], list[Any]],
        choices: Union[list[str], dict[str, Any]],
        prompt: str = "Select the best choice for the given text.",
        return_details: bool = False,
    ) -> Union[str, dict[str, Any]]:
        """
        Classify text into one of candidate choices using prompt guidance.

        :param Union[str, dict[str, Any], list[Any]] text: Input text or structured state.
        :param Union[list[str], dict[str, Any]] choices: List of candidate choice labels
            or dictionary mapping each choice label to its description.
        :param str prompt: Instruction prompt guiding the classification task.
            Default is ``"Select the best choice for the given text."``.
        :param bool return_details: If True, returns full details dictionary including
            choice, confidence, probabilities, and action probability.
            If False (default), returns the selected choice label string.
        :return: Selected choice string or detailed answer dictionary.
        :rtype: Union[str, dict[str, Any]]
        """
        questions = {
            "classification": {
                "type": "choice",
                "instructions": prompt,
                "criteria": choices,
            }
        }
        res = self.system_one(text, questions)
        ans = res["answers"]["classification"]
        if return_details:
            return ans
        return str(ans["choice"])

    def classify_batch(
        self,
        texts: list[Union[str, dict[str, Any], list[Any]]],
        choices: Union[list[str], dict[str, Any]],
        prompt: str = "Select the best choice for the given text.",
        return_details: bool = False,
    ) -> list[Union[str, dict[str, Any]]]:
        """
        Classify multiple texts in batches.

        :param list[Union[str, dict[str, Any], list[Any]]] texts: List of texts or states.
        :param Union[list[str], dict[str, Any]] choices: Candidate choices.
        :param str prompt: Instruction prompt.
        :param bool return_details: Whether to return full details.
        :return: List of predicted choices or detailed dictionaries.
        :rtype: list[Union[str, dict[str, Any]]]
        """
        if not texts:
            return []

        results: list[Union[str, dict[str, Any]]] = []
        for text in texts:
            res = self.classify(
                text,
                choices=choices,
                prompt=prompt,
                return_details=return_details,
            )
            results.append(res)
        return results

    def predict(
        self,
        text: Union[str, dict[str, Any], list[Any]],
        choices: Optional[Union[list[str], dict[str, Any]]] = None,
        prompt: str = "Select the best choice for the given text.",
        questions: Optional[dict[str, Any]] = None,
        return_details: bool = False,
    ) -> Any:
        """
        Predict classification choice or structured decisions.

        If ``choices`` is provided, executes choice classification.
        If ``questions`` is provided, executes structured decision tasks.

        :param Union[str, dict[str, Any], list[Any]] text: Input text or state.
        :param Optional[Union[list[str], dict[str, Any]]] choices: Candidate choices.
        :param str prompt: Instruction prompt when using choices.
        :param Optional[dict[str, Any]] questions: Question dictionary.
        :param bool return_details: Whether to return detailed output.
        :return: Predicted choice or questions output.
        :rtype: Any
        """
        if questions is not None:
            return self.system_one(text, questions)
        if choices is not None:
            return self.classify(
                text,
                choices=choices,
                prompt=prompt,
                return_details=return_details,
            )
        raise ValueError(
            "Either 'choices' or 'questions' must be specified."
        )


Laya = LayaModel
