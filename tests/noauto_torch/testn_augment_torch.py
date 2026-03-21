# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for augmentation functions that require transformers
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (torch, transformers)
# - Python 3.13+ compatibility issues

import unittest


class AugmentTestCaseN(unittest.TestCase):
    """Tests for augmentation functions (requires transformers)"""

    def test_augment_wangchanberta_returns_list(self):
        from pythainlp.augment.lm import Thai2transformersAug

        augmenter = Thai2transformersAug()
        result = augmenter.augment("แมวกิน<mask>")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_augment_wangchanberta_items_are_strings(self):
        from pythainlp.augment.lm import Thai2transformersAug

        augmenter = Thai2transformersAug()
        result = augmenter.augment("แมวกิน<mask>")
        for item in result:
            self.assertIsInstance(item, str)

    def test_augment_wangchanberta_generate_returns_list(self):
        from pythainlp.augment.lm import Thai2transformersAug

        augmenter = Thai2transformersAug()
        result = augmenter.generate("แมวกิน<mask>", num_replace_tokens=1)
        self.assertIsInstance(result, list)

    def test_augment_phayathaibert_returns_list(self):
        from pythainlp.augment.lm import ThaiTextAugmenter

        augmenter = ThaiTextAugmenter()
        result = augmenter.augment("แมวกิน<mask>")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_augment_phayathaibert_items_are_strings(self):
        from pythainlp.augment.lm import ThaiTextAugmenter

        augmenter = ThaiTextAugmenter()
        result = augmenter.augment("แมวกิน<mask>")
        for item in result:
            self.assertIsInstance(item, str)

    def test_augment_phayathaibert_num_augs_respected(self):
        from pythainlp.augment.lm import ThaiTextAugmenter

        augmenter = ThaiTextAugmenter()
        result = augmenter.augment("แมวกิน<mask>", num_augs=2)
        self.assertEqual(len(result), 2)

    def test_augment_phayathaibert_exceeds_limit_raises(self):
        from pythainlp.augment.lm import ThaiTextAugmenter

        augmenter = ThaiTextAugmenter()
        with self.assertRaises(ValueError):
            augmenter.augment("แมวกิน<mask>", num_augs=10)

    def test_augment_phayathaibert_adds_mask_if_missing(self):
        from pythainlp.augment.lm import ThaiTextAugmenter

        augmenter = ThaiTextAugmenter()
        result = augmenter.augment("แมวกิน", num_augs=1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
