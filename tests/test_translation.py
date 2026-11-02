"""
Unit tests for Hinglish Translation Pipeline using standard unittest.
"""

import unittest
from src.translation.pipeline import HinglishTranslationPipeline

class TestTranslation(unittest.TestCase):
    def setUp(self):
        self.pipeline = HinglishTranslationPipeline()

    def test_translation_basic(self):
        res = self.pipeline.translate("bhai kaisa hai tu")
        self.assertIn("translation", res)
        self.assertIn("Brother, how are you", res["translation"])

    def test_empty_translation(self):
        res = self.pipeline.translate("")
        self.assertEqual(res["translation"], "")

if __name__ == "__main__":
    unittest.main()
