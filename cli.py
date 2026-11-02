"""
Command Line Interface (CLI) for Hinglish Smart Writing Assistant.
Supports:
- Interactive text processing
- File batch processing
- Benchmark evaluation execution
"""

import argparse
import json
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
from src.agent.writing_assistant import HinglishWritingAssistant
from src.evaluation.evaluator import BenchmarkEvaluator

def interactive_mode():
    assistant = HinglishWritingAssistant()
    print("=" * 60)
    print("✍️ Hinglish Smart Writing Assistant (Interactive CLI)")
    print("Type your Hinglish text and press Enter. Type 'exit' to quit.")
    print("=" * 60)

    while True:
        try:
            user_input = input("\n[Hinglish] > ").strip()
            if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting...")
                break

            result = assistant.process(user_input, style="Standard Formal")
            print("-" * 50)
            print(f"Native Script : {result['devanagari']}")
            print(f"Refined Formal: {result['phrasing']['refined_text']}")
            print(f"English Trans : {result['translation']}")
            print("-" * 50)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

def main():
    parser = argparse.ArgumentParser(description="Hinglish Smart Writing Assistant CLI")
    parser.add_argument("--text", type=str, help="Process a single sentence")
    parser.add_argument("--style", type=str, default="Standard Formal", help="Phrasing tone")
    parser.add_argument("--benchmark", action="store_true", help="Run 45 test-case benchmark evaluation")
    parser.add_argument("--interactive", action="store_true", help="Start interactive REPL mode")
    args = parser.parse_args()

    if args.benchmark:
        evaluator = BenchmarkEvaluator()
        summary = evaluator.run_benchmark(save_results=True)
        print("\nBenchmark Overall Summary:")
        print(json.dumps(summary["overall_summary"], indent=2))
        return

    if args.text:
        assistant = HinglishWritingAssistant()
        res = assistant.process(args.text, style=args.style)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    interactive_mode()

if __name__ == "__main__":
    main()
