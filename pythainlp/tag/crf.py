# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Pure-Python Linear-Chain Conditional Random Field (CRF) tagger.

This module provides a lightweight, pure-Python inference engine
for First-Order Markov Chain (FOMC) CRF models using Viterbi decoding.
It loads model weights exported in JSON or gzipped JSON format,
allowing CRF models to run with zero C/C++ extension dependencies.
"""

from __future__ import annotations

import gzip
import json
import os
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

if TYPE_CHECKING:
    import types


def _extract_item_features(
    item: Union[Sequence[str], Dict[str, Any]],
) -> List[Tuple[str, float]]:
    """Extract (feature_name, feature_value) pairs from an observation.

    :param item: Observation features, either as a sequence of feature names
        or as a dictionary mapping feature names to values.
    :type item: Union[Sequence[str], Dict[str, Any]]
    :return: List of (feature_name, float_weight) tuples.
    :rtype: List[Tuple[str, float]]
    """
    if not isinstance(item, dict):
        return [(str(feat), 1.0) for feat in item]

    features: List[Tuple[str, float]] = []
    for key, val in item.items():
        if isinstance(val, str):
            features.append((f"{key}:{val}", 1.0))
        elif isinstance(val, bool):
            if val:
                features.append((key, 1.0))
        elif isinstance(val, (int, float)):
            if val != 0:
                features.append((key, float(val)))
    return features


class CRFTagger:
    """Linear-Chain Conditional Random Field (CRF) tagger.

    Uses pure-Python Viterbi decoding to predict optimal label sequences
    from pre-trained CRF weights without requiring external C libraries.

    :param Optional[str] model_path: Path to the CRF model weights file
        (`.json` or `.json.gz`).
    """

    labels: List[str]
    _num_labels: int
    _label_to_idx: Dict[str, int]
    _trans_mat: List[List[float]]
    _state_features: Dict[str, List[Tuple[int, float]]]

    def __init__(self, model_path: Optional[str] = None) -> None:
        """Initialize the CRF tagger.

        :param Optional[str] model_path: Path to model weights file.
        """
        self.labels = []
        self._num_labels = 0
        self._label_to_idx = {}
        self._trans_mat = []
        self._state_features = {}
        if model_path is not None:
            self.open(model_path)

    def open(self, model_path: str) -> None:
        """Load model weights from a JSON or gzipped JSON file.

        :param str model_path: Path to the model weights file.
        :raises FileNotFoundError: If the model file cannot be found.
        """
        resolved_path = self._resolve_model_path(model_path)
        data = self._read_weights_file(resolved_path)
        self._load_data(data)

    @staticmethod
    def _resolve_model_path(model_path: str) -> str:
        """Resolve legacy .crfsuite / .model paths to .json.gz if available.

        :param str model_path: Original path to model.
        :return: Resolved path to weight file.
        :rtype: str
        """
        if os.path.exists(model_path):
            return model_path
        if not (model_path.endswith(".gz") or model_path.endswith(".json")):
            gz_candidate = model_path.rsplit(".", 1)[0] + ".json.gz"
            if os.path.exists(gz_candidate):
                return gz_candidate
            json_candidate = model_path.rsplit(".", 1)[0] + ".json"
            if os.path.exists(json_candidate):
                return json_candidate
        return model_path

    @staticmethod
    def _read_weights_file(file_path: str) -> Dict[str, Any]:
        """Read weights dictionary from JSON or gzip-compressed JSON.

        :param str file_path: Path to weights file.
        :return: Parsed weights dictionary.
        :rtype: Dict[str, Any]
        """
        with open(file_path, "rb") as file_obj:
            magic = file_obj.read(4)

        if magic.startswith(b"\x1f\x8b"):
            with gzip.open(file_path, "rt", encoding="utf-8") as file_handle:
                return cast(Dict[str, Any], json.load(file_handle))

        if magic == b"lCRF":
            candidates = [
                file_path.rsplit(".", 1)[0] + ".json.gz",
                file_path + ".json.gz",
            ]
            for cand in candidates:
                if os.path.exists(cand):
                    with gzip.open(cand, "rt", encoding="utf-8") as file_handle:
                        return cast(Dict[str, Any], json.load(file_handle))

            from pythainlp.corpus import corpus_path
            from pythainlp.tools.path import safe_path_join

            if "thainer" in file_path or "thai-ner" in file_path:
                bundled_thainer = safe_path_join(
                    corpus_path(), "thainer_crf_1_5_1.json.gz"
                )
                if os.path.exists(bundled_thainer):
                    with gzip.open(
                        bundled_thainer, "rt", encoding="utf-8"
                    ) as file_handle:
                        return cast(Dict[str, Any], json.load(file_handle))

            raise ValueError(
                f"Model file '{file_path}' is in binary CRFsuite format. "
                "Please use converted .json.gz weights instead."
            )

        with open(file_path, "r", encoding="utf-8") as file_handle:
            return cast(Dict[str, Any], json.load(file_handle))

    def _load_data(self, data: Dict[str, Any]) -> None:
        """Initialize internal structures from weights data.

        :param Dict[str, Any] data: Parsed model dictionary.
        """
        self.labels = list(data.get("labels", []))
        self._num_labels = len(self.labels)
        self._label_to_idx = {lbl: i for i, lbl in enumerate(self.labels)}

        transitions = data.get("transitions", {})
        self._trans_mat = [
            [
                transitions.get(f"{self.labels[i]}->{self.labels[j]}", 0.0)
                for j in range(self._num_labels)
            ]
            for i in range(self._num_labels)
        ]

        raw_state_feats = data.get("state_features", {})
        self._state_features = {
            attr: [
                (self._label_to_idx[lbl], weight)
                for lbl, weight in lbl_map.items()
                if lbl in self._label_to_idx
            ]
            for attr, lbl_map in raw_state_feats.items()
        }

    def _compute_state_scores(
        self, item: Union[Sequence[str], Dict[str, Any]]
    ) -> List[float]:
        """Compute state scores for all labels at a single sequence position.

        :param item: Observation features at current position.
        :type item: Union[Sequence[str], Dict[str, Any]]
        :return: State score per label index.
        :rtype: List[float]
        """
        scores = [0.0] * self._num_labels
        for attr, val in _extract_item_features(item):
            active = self._state_features.get(attr)
            if active is not None:
                for lbl_idx, weight in active:
                    scores[lbl_idx] += weight * val
        return scores

    def tag(
        self, xseq: Sequence[Union[Sequence[str], Dict[str, Any]]]
    ) -> List[str]:
        """Predict the optimal label sequence for an item sequence.

        :param xseq: Sequence of item features, where each item is either
            a sequence of string feature names or a dictionary of features.
        :type xseq: Sequence[Union[Sequence[str], Dict[str, Any]]]
        :return: Predicted sequence of labels.
        :rtype: List[str]
        """
        seq_len = len(xseq)
        if seq_len == 0 or self._num_labels == 0:
            return []

        dp_scores = self._compute_state_scores(xseq[0])
        backpointers: List[List[int]] = []

        for step in range(1, seq_len):
            state_scores = self._compute_state_scores(xseq[step])
            new_dp = [0.0] * self._num_labels
            backpointer = [0] * self._num_labels

            for curr_idx in range(self._num_labels):
                best_score = float("-inf")
                best_prev = 0
                for prev_idx in range(self._num_labels):
                    score = (
                        dp_scores[prev_idx]
                        + self._trans_mat[prev_idx][curr_idx]
                    )
                    if score > best_score:
                        best_score = score
                        best_prev = prev_idx
                new_dp[curr_idx] = best_score + state_scores[curr_idx]
                backpointer[curr_idx] = best_prev

            dp_scores = new_dp
            backpointers.append(backpointer)

        best_last = max(range(self._num_labels), key=lambda i: dp_scores[i])
        best_path = [best_last]
        for backpointer in reversed(backpointers):
            best_path.append(backpointer[best_path[-1]])
        best_path.reverse()

        return [self.labels[idx] for idx in best_path]

    def close(self) -> None:
        """Close the tagger and release internal model structures."""
        self.labels.clear()
        self._num_labels = 0
        self._label_to_idx.clear()
        self._trans_mat.clear()
        self._state_features.clear()

    def __enter__(self) -> CRFTagger:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None:
        """Context manager exit."""
        self.close()
