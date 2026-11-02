"""
Master Writing Assistant Agent.
Orchestrates:
1. Code-switch token classification
2. Transliteration (Roman Hinglish -> Devanagari Hindi)
3. Phrasing Refinement (Standard Formal, Casual, Polite, Concise)
4. English Translation (IndicTrans2)
5. Quality Critic (Character Error Rate & Confidence scoring)
"""

from typing import Dict, Any, Optional
from ..transliteration.pipeline import HinglishTransliterationPipeline
from ..translation.pipeline import HinglishTranslationPipeline
from ..phrasing.genai_editor import GenAIEditor
from ..evaluation.metrics import compute_cer, compute_wer, compute_word_accuracy

class HinglishWritingAssistant:
    def __init__(self, llm_provider: Optional[str] = None):
        self.transliteration_pipeline = HinglishTransliterationPipeline()
        self.translation_pipeline = HinglishTranslationPipeline()
        self.genai_editor = GenAIEditor(provider=llm_provider)

    def process(
        self,
        text: str,
        style: str = "Standard Formal",
        preserve_english_loanwords: bool = False,
        translate_to_english: bool = True
    ) -> Dict[str, Any]:
        """
        Executes end-to-end writing assistant pipeline.
        """
        if not text or not text.strip():
            return {
                "input": text,
                "devanagari": "",
                "phrasing": {},
                "translation": "",
                "code_switch_summary": {},
                "tokens": []
            }

        # Step 1: Transliteration
        xlit_result = self.transliteration_pipeline.transliterate(
            text,
            preserve_english_loanwords=preserve_english_loanwords
        )
        devanagari_text = xlit_result["devanagari"]

        # Step 2: Phrasing refinement in requested style
        phrasing_result = self.genai_editor.refine_text(
            text=text,
            devanagari_text=devanagari_text,
            style=style
        )

        # Step 3: English Translation
        translation_text = ""
        if translate_to_english:
            trans_res = self.translation_pipeline.translate(
                devanagari_text if devanagari_text else text,
                source_lang="hi"
            )
            translation_text = trans_res.get("translation", "")

        # Step 4: Quality & Verification Critique
        # CER / Word distance between raw transliteration and refined Devanagari
        internal_cer = compute_cer(devanagari_text, phrasing_result["refined_text"])
        internal_wer = compute_wer(devanagari_text, phrasing_result["refined_text"])

        return {
            "input": text,
            "devanagari": devanagari_text,
            "tokens": xlit_result["tokens"],
            "code_switch_summary": xlit_result["code_switch_summary"],
            "phrasing": phrasing_result,
            "translation": translation_text,
            "refinement_cer": internal_cer,
            "refinement_wer": internal_wer
        }

    def process_all_styles(self, text: str) -> Dict[str, Any]:
        """Generates all 4 stylistic variants simultaneously."""
        styles = ["Standard Formal", "Natural Casual", "Polite / Respectful", "Concise / Professional"]
        results = {}
        for s in styles:
            results[s] = self.process(text, style=s)
        return results
