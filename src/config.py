"""
Configuration for Hinglish Smart Writing Assistant.
Defines model identifiers, caching, paths, and default hyperparameters.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"

TEST_CASES_PATH = DATA_DIR / "test_cases.json"
TEST_EVAL_PATH = DATA_DIR / "test_cases_evaluated.json"
AKSHARANTAR_SAMPLE_PATH = DATA_DIR / "aksharantar_sample.json"

# Models Specification (AI4Bharat, BharatGen, Open Source HuggingFace)
INDICXLIT_MODEL_ID = "ai4bharat/indicxlit"
INDICTRANS2_HIN_ENG_ID = "ai4bharat/indictrans2-indic-en-1B"
MARIAN_MT_HIN_ENG_ID = "Helsinki-NLP/opus-mt-hi-en"
BHARATGEN_PARAM1_ID = "bharatgenai/param1"

# LLM Providers Configuration (Gemini / OpenAI / Fallback)
DEFAULT_LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock_genai")  # 'openai', 'gemini', 'mock_genai'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Transliteration Configuration
TRANSLITERATION_DEFAULT_ENGINE = "hybrid"  # 'hybrid', 'indicxlit', 'phonetic_rule'
LANGUAGE_CODE = "hi"
SCRIPT_NAME = "Devanagari"

# Generation & Phrasing Styles
PHRASING_STYLES = [
    "Standard Formal",
    "Natural Casual",
    "Polite / Respectful",
    "Concise / Professional"
]

