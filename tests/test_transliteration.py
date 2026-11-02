"""
Unit tests for Transliteration Pipeline and Code-Switch Tagger using standard unittest.
"""

import unittest
from src.transliteration.pipeline import HinglishTransliterationPipeline
from src.transliteration.code_switch_tagger import CodeSwitchTagger

class TestTransliteration(unittest.TestCase):
    def setUp(self):
        self.pipeline = HinglishTransliterationPipeline()
        self.tagger = CodeSwitchTagger()

    def test_code_switch_tagging(self):
        sentence = "mera meeting 3 baje schedule hai"
        tags = self.tagger.analyze_sentence(sentence)
        types = [t["type"] for t in tags if t["type"] != "WHITESPACE"]
        self.assertIn("HINDI_ROMAN", types)
        self.assertIn("ENGLISH_LOAN", types)
        self.assertIn("NUMERIC", types)

    def test_basic_transliteration(self):
        res = self.pipeline.transliterate("namaste")
        self.assertEqual(res["devanagari"], "नमस्ते")

    def test_sms_slang_normalization(self):
        res = self.pipeline.transliterate("bhai kaisa h tu")
        self.assertIn("भाई", res["devanagari"])
        self.assertIn("है", res["devanagari"])

    def test_preserve_english_loanwords(self):
        res = self.pipeline.transliterate("mera meeting schedule hai", preserve_english_loanwords=True)
        self.assertIn("meeting", res["devanagari"])

if __name__ == "__main__":
    unittest.main()
