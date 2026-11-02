"""
GenAI Phrasing Editor using Few-Shot In-Context Prompting and BharatGen / LLMs.
Includes fallback to deterministic linguistic refiner.
"""

import os
from typing import Dict, Any, Optional
from .prompts import build_refinement_prompt
from .rule_refiner import RuleRefiner
from ..config import DEFAULT_LLM_PROVIDER, OPENAI_API_KEY, GEMINI_API_KEY

class GenAIEditor:
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or DEFAULT_LLM_PROVIDER
        self.rule_refiner = RuleRefiner()
        self.openai_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
        self.gemini_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")

    def refine_text(self, text: str, devanagari_text: str = "", style: str = "Standard Formal") -> Dict[str, Any]:
        """
        Refines phrasing to improve grammar, vocabulary, and tone.
        """
        if not text or not text.strip():
            return {
                "original_input": text,
                "refined_text": "",
                "style": style,
                "provider": "none"
            }

        # 1. Attempt LLM provider if configured
        if self.provider == "openai" and self.openai_key:
            try:
                import openai
                client = openai.OpenAI(api_key=self.openai_key)
                prompt = build_refinement_prompt(text, devanagari_text, style)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                refined = response.choices[0].message.content.strip()
                return {
                    "original_input": text,
                    "refined_text": refined,
                    "style": style,
                    "provider": "OpenAI (GPT-4o-mini)"
                }
            except Exception as e:
                print(f"[Warning] OpenAI call failed: {e}. Falling back to Rule Refiner.")

        # 2. High-precision rule-based linguistic refiner (Offline/Default)
        refined = self.rule_refiner.refine(text, devanagari_text, style=style)
        return {
            "original_input": text,
            "refined_text": refined,
            "style": style,
            "provider": "Linguistic Grammar & Style Engine (BharatGen Prompt Alignment)"
        }

