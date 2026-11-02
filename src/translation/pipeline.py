"""
Hinglish to English Translation Pipeline.
"""

from typing import Dict, Any
from .indictrans_engine import IndicTransEngine

class HinglishTranslationPipeline:
    def __init__(self, model_id: str = "ai4bharat/indictrans2-indic-en-1B"):
        self.engine = IndicTransEngine(model_id=model_id)

    def translate(self, text: str, source_lang: str = "hinglish") -> Dict[str, Any]:
        """Translates Hinglish or Devanagari Hindi text into English."""
        if not text or not text.strip():
            return {"input": text, "translation": "", "engine": "IndicTrans2"}

        translated_text = self.engine.translate(text)
        return {
            "input": text,
            "source_lang": source_lang,
            "target_lang": "en",
            "translation": translated_text,
            "engine": "AI4Bharat IndicTrans2"
        }

