"""
Comprehensive Evaluation Suite for Hinglish Smart Writing Assistant.
Evaluates 30-50 representative test cases against ground truth:
- Character Error Rate (CER)
- Word Error Rate (WER)
- Word Accuracy (1 - WER)
- Translation BLEU & chrF
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from ..agent.writing_assistant import HinglishWritingAssistant
from .metrics import evaluate_prediction
from ..config import TEST_CASES_PATH, TEST_EVAL_PATH

class BenchmarkEvaluator:
    def __init__(self, test_cases_path: Path = TEST_CASES_PATH):
        self.test_cases_path = test_cases_path
        self.assistant = HinglishWritingAssistant()

    def run_benchmark(self, save_results: bool = True) -> Dict[str, Any]:
        """Runs evaluation over all test cases and generates summary statistics."""
        with open(self.test_cases_path, "r", encoding="utf-8") as f:
            test_cases = json.load(f)

        evaluated_records = []
        category_metrics: Dict[str, List[Dict[str, float]]] = {}

        total_cer = 0.0
        total_wer = 0.0
        total_acc = 0.0
        total_bleu = 0.0
        total_chrf = 0.0

        for case in test_cases:
            cid = case["id"]
            cat = case["category"]
            inp = case["hinglish_input"]
            ref_dev = case["reference_devanagari"]
            ref_trans = case["reference_english_translation"]

            # Process through assistant pipeline
            pred = self.assistant.process(inp, style="Standard Formal")
            hyp_dev = pred["devanagari"]
            hyp_trans = pred["translation"]

            # Compute quantitative metrics
            scores = evaluate_prediction(
                ref_devanagari=ref_dev,
                hyp_devanagari=hyp_dev,
                ref_translation=ref_trans,
                hyp_translation=hyp_trans
            )

            record = {
                "id": cid,
                "category": cat,
                "input": inp,
                "ref_devanagari": ref_dev,
                "hyp_devanagari": hyp_dev,
                "hyp_improved_formal": pred["phrasing"]["refined_text"],
                "ref_translation": ref_trans,
                "hyp_translation": hyp_trans,
                "metrics": scores,
                "notes": case.get("notes", "")
            }
            evaluated_records.append(record)

            if cat not in category_metrics:
                category_metrics[cat] = []
            category_metrics[cat].append(scores)

            total_cer += scores["CER"]
            total_wer += scores["WER"]
            total_acc += scores["Word_Accuracy"]
            total_bleu += scores["BLEU"]
            total_chrf += scores["chrF"]

        n = len(test_cases)
        overall_summary = {
            "total_test_cases": n,
            "mean_CER": round(total_cer / n, 4),
            "mean_WER": round(total_wer / n, 4),
            "mean_Word_Accuracy": round(total_acc / n, 2),
            "mean_BLEU": round(total_bleu / n, 2),
            "mean_chrF": round(total_chrf / n, 2)
        }

        # Category-wise breakdown
        category_summary = {}
        for cat, items in category_metrics.items():
            k = len(items)
            category_summary[cat] = {
                "count": k,
                "mean_CER": round(sum(x["CER"] for x in items) / k, 4),
                "mean_WER": round(sum(x["WER"] for x in items) / k, 4),
                "mean_Word_Accuracy": round(sum(x["Word_Accuracy"] for x in items) / k, 2),
                "mean_BLEU": round(sum(x["BLEU"] for x in items) / k, 2),
                "mean_chrF": round(sum(x["chrF"] for x in items) / k, 2)
            }

        benchmark_result = {
            "overall_summary": overall_summary,
            "category_summary": category_summary,
            "test_cases": evaluated_records
        }

        if save_results:
            with open(TEST_EVAL_PATH, "w", encoding="utf-8") as f:
                json.dump(benchmark_result, f, ensure_ascii=False, indent=2)
            print(f"[Success] Saved evaluated benchmark to {TEST_EVAL_PATH}")

        return benchmark_result

if __name__ == "__main__":
    evaluator = BenchmarkEvaluator()
    summary = evaluator.run_benchmark(save_results=True)
    print("\n================ BENCHMARK SUMMARY ================")
    print(json.dumps(summary["overall_summary"], indent=2))
    print("\n================ CATEGORY BREAKDOWN ================")
    print(json.dumps(summary["category_summary"], indent=2))
