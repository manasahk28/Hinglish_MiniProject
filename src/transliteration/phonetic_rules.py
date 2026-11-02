"""
Phonetic transliteration rules and Aksharantar-compatible dictionary engine.
Translates Roman-script Hinglish tokens into Devanagari Hindi using:
1. Aksharantar lexicon lookup (exact match)
2. Common Hinglish phonetic abbreviations & slang normalizations
3. Rule-based Indic phonetic parser (consonant-vowel segmentation, conjuncts, matras, nuktas)
"""

import json
from pathlib import Path
from typing import Optional, Dict

class PhoneticTransliterationEngine:
    def __init__(self, aksharantar_path: Optional[str] = None):
        self.lexicon: Dict[str, str] = {}
        if aksharantar_path and Path(aksharantar_path).exists():
            try:
                with open(aksharantar_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.lexicon = data.get("word_mappings", {})
            except Exception as e:
                print(f"[Warning] Could not load Aksharantar lexicon: {e}")

        # SMS & Hinglish texting slang expansions to standard Devanagari
        self.slang_dict: Dict[str, str] = {
            "h": "है",
            "hn": "हाँ",
            "ha": "हाँ",
            "haa": "हाँ",
            "haan": "हाँ",
            "nhi": "नहीं",
            "ni": "नहीं",
            "plz": "प्लीज़",
            "pls": "प्लीज़",
            "thx": "थैंक्स",
            "ty": "थैंक यू",
            "yr": "यार",
            "bro": "ब्रो",
            "v": "भी",
            "krna": "करना",
            "kro": "करो",
            "kr": "कर",
            "rha": "रहा",
            "rhi": "रही",
            "rhe": "रहे",
            "kuch": "कुछ",
            "bohot": "बहुत",
            "bhot": "बहुत",
            "shi": "सही",
            "gud": "गुड",
            "bt": "बात",
            "wfh": "डब्ल्यूएफएच",
            "otp": "ओटीपी",
            "pr": "पीआर",
            "url": "यूआरएल",
            "gpay": "जीपे"
        }

        # Multi-character consonant mapping ordered by length descending
        self.consonants = [
            ("chh", "छ"), ("kh", "ख"), ("gh", "घ"), ("ch", "च"),
            ("jh", "झ"), ("th", "थ"), ("dh", "ध"), ("ph", "फ"),
            ("bh", "भ"), ("sh", "श"), ("shh", "ष"), ("ng", "ङ"),
            ("ny", "ञ"), ("gy", "ज्ञ"), ("tr", "त्र"), ("ksh", "क्ष"),
            ("k", "क"), ("g", "ग"), ("j", "ज"), ("t", "त"),
            ("d", "द"), ("n", "न"), ("p", "प"), ("b", "ब"),
            ("m", "म"), ("y", "य"), ("r", "र"), ("l", "ल"),
            ("v", "व"), ("w", "व"), ("s", "स"), ("h", "ह"),
            ("z", "ज़"), ("f", "फ़"), ("q", "क़"), ("x", "क्स")
        ]

        # Initial independent vowels
        self.initial_vowels = [
            ("aa", "आ"), ("a", "अ"), ("ee", "ई"), ("ii", "ई"), ("i", "इ"),
            ("oo", "ऊ"), ("uu", "ऊ"), ("u", "उ"), ("ai", "ऐ"), ("au", "औ"),
            ("e", "ए"), ("o", "ओ")
        ]

        # Dependent vowel signs (matras)
        self.matras = [
            ("aa", "ा"), ("a", ""), ("ee", "ी"), ("ii", "ी"), ("i", "ि"),
            ("oo", "ू"), ("uu", "ू"), ("u", "ु"), ("ai", "ै"), ("au", "ौ"),
            ("e", "े"), ("o", "ो")
        ]

    def _match_prefix(self, text: str, table):
        for pattern, symbol in table:
            if text.startswith(pattern):
                return pattern, symbol
        return None, None

    def transliterate_phonetic_token(self, token: str) -> str:
        """Transliterates a single Roman token to Devanagari using phonetic segmenter."""
        t = token.lower().strip()
        if not t:
            return ""

        # 1. Exact Lexicon / Slang check
        if t in self.slang_dict:
            return self.slang_dict[t]
        if t in self.lexicon:
            return self.lexicon[t]

        # 2. Heuristic rules for common endings like 'ein' (बातें), 'on' (दिनों), 'aayega' (आएगा)
        # Check if the word starts with a vowel
        res = []
        i = 0
        n = len(t)
        prev_was_consonant = False

        while i < n:
            rem = t[i:]

            # Check nasal endings 'n' at end or followed by punctuation
            if (rem == "n" or rem == "m") and i > 0:
                res.append("ं")
                i += 1
                prev_was_consonant = False
                continue

            if not prev_was_consonant:
                # Look for independent vowel
                v_pat, v_sym = self._match_prefix(rem, self.initial_vowels)
                if v_pat:
                    res.append(v_sym)
                    i += len(v_pat)
                    prev_was_consonant = False
                    continue

                # Look for consonant
                c_pat, c_sym = self._match_prefix(rem, self.consonants)
                if c_pat:
                    res.append(c_sym)
                    i += len(c_pat)
                    prev_was_consonant = True
                    continue

                # Fallback char
                res.append(rem[0])
                i += 1
                prev_was_consonant = False
            else:
                # Previous was consonant: look for matra
                m_pat, m_sym = self._match_prefix(rem, self.matras)
                if m_pat:
                    res.append(m_sym)
                    i += len(m_pat)
                    prev_was_consonant = False
                    continue

                # Look for next consonant (creates conjunct with halant)
                c_pat, c_sym = self._match_prefix(rem, self.consonants)
                if c_pat:
                    # If end of word or double consonant (like 'tt', 'kk', 'st'), insert halant or schwa
                    # In Hindi orthography, cluster before consonant usually takes halant:
                    res.append("्")
                    res.append(c_sym)
                    i += len(c_pat)
                    prev_was_consonant = True
                    continue

                res.append(rem[0])
                i += 1
                prev_was_consonant = False

        output = "".join(res)
        # Clean up double virama or isolated signs
        output = output.replace("््", "्")
        return output

