"""
Unit tests for evaluation metrics using standard unittest.
"""

import unittest
from src.evaluation.metrics import (
    compute_cer,
    compute_wer,
    compute_word_accuracy,
    evaluate_prediction
)

class TestMetrics(unittest.TestCase):
    def test_identical_cer_wer(self):
        ref = "नमस्ते भारत"
        hyp = "नमस्ते भारत"
        self.assertEqual(compute_cer(ref, hyp), 0.0)
        self.assertEqual(compute_wer(ref, hyp), 0.0)
        self.assertEqual(compute_word_accuracy(ref, hyp), 1.0)

    def test_different_cer(self):
        ref = "नमस्ते"
        hyp = "नमसते"
        cer = compute_cer(ref, hyp)
        self.assertGreater(cer, 0.0)

    def test_evaluate_prediction_keys(self):
        res = evaluate_prediction(
            ref_devanagari="कल मिलते हैं",
            hyp_devanagari="कल मिलते हैं",
            ref_translation="See you tomorrow",
            hyp_translation="See you tomorrow"
        )
        self.assertIn("CER", res)
        self.assertIn("WER", res)
        self.assertIn("Word_Accuracy", res)
        self.assertIn("BLEU", res)
        self.assertEqual(res["CER"], 0.0)

if __name__ == "__main__":
    unittest.main()
