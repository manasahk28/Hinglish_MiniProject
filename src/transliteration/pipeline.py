"""
Unified Hinglish Transliteration Pipeline.
Integrates Code-Switching Tagger, Homograph Disambiguation,
Aksharantar Lexicon, and IndicXlit Engine.
"""

from typing import Dict, Any, List
from .code_switch_tagger import CodeSwitchTagger
from .indicxlit_engine import IndicXlitEngine
from ..config import AKSHARANTAR_SAMPLE_PATH

# Context-dependent homograph and loanword phonetic rules
CONTEXT_HOMOGRAPHS = {
    "kaha": {
        "interrogative": "कहाँ",
        "declarative": "कहा"
    },
    "kahan": {
        "default": "कहाँ"
    },
    "bat": {
        "speech": "बात",
        "object": "बैट"
    },
    "mai": {
        "pronoun": "मैं",
        "postposition": "में"
    },
    "me": {
        "postposition": "में"
    }
}

class HinglishTransliterationPipeline:
    def __init__(self, mode: str = "hybrid"):
        self.tagger = CodeSwitchTagger()
        self.engine = IndicXlitEngine(aksharantar_path=str(AKSHARANTAR_SAMPLE_PATH))
        self.mode = mode

    def _disambiguate_homograph(self, token_lower: str, prev_token: str, next_token: str, is_question: bool) -> str:
        """Disambiguates contextual ambiguities like 'kaha' (where vs said) or 'mai' vs 'me'."""
        if token_lower == "kaha":
            if is_question or next_token in ["ja", "gaye", "ho", "hai", "the", "tha"]:
                return "कहाँ"
            return "कहा"
        
        if token_lower == "mai":
            if next_token in ["bhi", "kal", "ek", "to", "toh", "apne", "ghar"] or prev_token in ["ki", "agar"]:
                return "मैं"
            return "मैं"

        if token_lower == "me":
            return "में"

        if token_lower == "bat":
            if next_token in ["sahi", "karo", "karna", "ye", "yeh", "kya"] or prev_token in ["yeh", "ye", "ek", "koi"]:
                return "बात"

        return ""

    def transliterate(self, text: str, preserve_english_loanwords: bool = False) -> Dict[str, Any]:
        """
        Transliterates a Hinglish string into Devanagari Hindi.
        
        Args:
            text: Input Hinglish string in Roman script.
            preserve_english_loanwords: If True, leaves recognized English technical terms in Roman script.
                                        If False, transliterates them phonetically into Devanagari.
        
        Returns:
            Dict containing output text, token-by-token alignment, and metrics.
        """
        if not text or not text.strip():
            return {
                "input": text,
                "devanagari": "",
                "tokens": [],
                "code_switch_summary": {}
            }

        is_question = "?" in text
        tagged_tokens = self.tagger.analyze_sentence(text)
        
        output_parts = []
        token_details = []
        counts = {"HINDI_ROMAN": 0, "ENGLISH_LOAN": 0, "ACRONYM": 0, "NUMERIC": 0, "PUNCTUATION": 0}

        for idx, item in enumerate(tagged_tokens):
            raw = item["token"]
            t_type = item["type"]
            counts[t_type] = counts.get(t_type, 0) + 1

            if t_type == "WHITESPACE":
                output_parts.append(raw)
                continue

            if t_type in ["NUMERIC", "PUNCTUATION"]:
                output_parts.append(raw)
                token_details.append({
                    "original": raw,
                    "transliterated": raw,
                    "type": t_type
                })
                continue

            lower_t = raw.lower()
            prev_t = tagged_tokens[idx - 2]["token"].lower() if idx >= 2 and tagged_tokens[idx - 1]["type"] == "WHITESPACE" else ""
            next_t = tagged_tokens[idx + 2]["token"].lower() if idx + 2 < len(tagged_tokens) and tagged_tokens[idx + 1]["type"] == "WHITESPACE" else ""

            # Check contextual homograph first
            homograph_match = self._disambiguate_homograph(lower_t, prev_t, next_t, is_question)
            if homograph_match:
                transliterated = homograph_match
            elif t_type in ["ENGLISH_LOAN", "ACRONYM"] and preserve_english_loanwords:
                transliterated = raw
            else:
                # Transliterate through IndicXlit / Aksharantar phonetic engine
                transliterated = self.engine.transliterate_word(lower_t)[0]

            output_parts.append(transliterated)
            token_details.append({
                "original": raw,
                "transliterated": transliterated,
                "type": t_type
            })

        final_devanagari = "".join(output_parts).strip()

        return {
            "input": text,
            "devanagari": final_devanagari,
            "tokens": token_details,
            "code_switch_summary": counts
        }

