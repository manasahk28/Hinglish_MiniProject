"""
Deterministic Rule-based Hindi/Hinglish Phrasing Refiner.
Serves as high-precision offline baseline and fallback for GenAI editor.
"""

import re
from typing import Dict, Any

class RuleRefiner:
    def __init__(self):
        # Lexical replacements for Formal Hindi
        self.formal_replacements = [
            (r"\bmera meeting\b", "मेरी बैठक"),
            (r"\bमेरा मीटिंग\b", "मेरी बैठक"),
            (r"\bpe\b", "पर"),
            (r"\bपे\b", "पर"),
            (r"\bme\b", "में"),
            (r"\bmovie\b", "चलचित्र"),
            (r"\bमूवी\b", "चलचित्र"),
            (r"\bbarish\b", "वर्षा"),
            (r"\bबारिश\b", "वर्षा"),
            (r"\bbanda\b", "व्यक्ति"),
            (r"\bबंदा\b", "व्यक्ति"),
            (r"\bmast\b", "अत्यंत उत्तम"),
            (r"\bmast h\b", "अत्यंत उत्तम है"),
            (r"\bमस्त है\b", "अत्यंत उत्तम है"),
            (r"\bkripya\b", "कृपया"),
            (r"\bjhol\b", "अनियमितता"),
            (r"\bझोल\b", "अनियमितता"),
            (r"\bscene\b", "योजना"),
            (r"\bसीन\b", "योजना"),
            (r"\bkaise ho\b", "आप कैसे हैं?"),
            (r"\bkaise hai\b", "आप कैसे हैं?"),
            (r"\bkaisa hai tu\b", "आप कैसे हैं?"),
            (r"\bकैसा है तू\b", "आप कैसे हैं?"),
            (r"\bbohot din se\b", "काफी समय से"),
            (r"\bबहुत दिन से\b", "काफी समय से"),
            (r"\btum\b", "आप"),
            (r"\bतुम\b", "आप"),
            (r"\btu\b", "आप"),
            (r"\bतू\b", "आप"),
            (r"\btime\b", "समय"),
            (r"\bटाइम\b", "समय"),
            (r"\bdocumentation\b", "दस्तावेज़"),
            (r"\bडॉक्यूमेंटेशन\b", "दस्तावेज़"),
            (r"\bdeliver ho gaya\b", "प्रस्तुत कर दिया गया"),
            (r"\bडिलीवर हो गया\b", "प्रस्तुत कर दिया गया"),
            (r"\bsend kar do\b", "प्रेषित कर दीजिए"),
            (r"\bसेंड कर दो\b", "प्रेषित कर दीजिए"),
            (r"\bplz\b", "कृपया"),
            (r"\bप्लीज़\b", "कृपया"),
            (r"\bthanks\b", "धन्यवाद"),
            (r"\bथैंक्स\b", "धन्यवाद")
        ]

        # Lexical adjustments for Casual mode
        self.casual_replacements = [
            (r"\bmera meeting\b", "मेरी मीटिंग"),
            (r"\bमेरा मीटिंग\b", "मेरी मीटिंग"),
            (r"\bpe\b", "पर"),
            (r"\bपे\b", "पर"),
            (r"\bmovie\b", "फिल्म"),
            (r"\bमूवी\b", "फिल्म"),
            (r"\bshi\b", "सही"),
            (r"\bbhot\b", "बहुत"),
            (r"\bbohot\b", "बहुत")
        ]

    def refine(self, text: str, devanagari_text: str, style: str = "Standard Formal") -> str:
        """Applies grammatical and stylistic transformations based on target style."""
        target = devanagari_text if devanagari_text else text
        
        # Strip trailing loose punctuations and clean spaces
        res = target.strip()

        if style in ["Standard Formal", "Concise / Professional", "Polite / Respectful"]:
            for pattern, replacement in self.formal_replacements:
                res = re.sub(pattern, replacement, res, flags=re.IGNORECASE)
            
            # Ensure polite verb ending if starting with 'आप'
            if "आप" in res and res.endswith("हो"):
                res = res[:-2] + "हैं।"
            elif not res.endswith((".", "।", "?", "!")):
                res += "।"
        else: # Natural Casual
            for pattern, replacement in self.casual_replacements:
                res = re.sub(pattern, replacement, res, flags=re.IGNORECASE)
            if not res.endswith((".", "।", "?", "!")):
                res += "।"

        return res

