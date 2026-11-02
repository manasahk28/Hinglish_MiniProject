"""
Code-switching detector and tokenizer for Hinglish text.
Classifies tokens into:
- HINDI_ROMAN: Hindi words written in Roman script (e.g. 'kaisa', 'ghar', 'bhai')
- ENGLISH_LOAN: Pure English borrowed/technical words (e.g. 'meeting', 'server', 'presentation')
- NUMERIC_PUNCT: Numbers, punctuation, emojis, URLs
"""

import re
from typing import List, Dict, Any

# Common English technical words, abbreviations, and loanwords frequently used in Hinglish
ENGLISH_LOANWORDS = {
    "meeting", "server", "documentation", "update", "send", "client", "presentation",
    "deliver", "bug", "fix", "pr", "pull", "request", "merge", "invoice", "payment",
    "release", "sprint", "feature", "launch", "network", "issue", "wfh", "office",
    "identity", "proof", "attach", "application", "approve", "time", "treat", "party",
    "deadline", "otp", "train", "number", "platform", "gpay", "error", "code", "url",
    "link", "email", "mail", "laptop", "mobile", "phone", "call", "project", "code",
    "branch", "git", "github", "check", "point", "nature", "scene", "room", "market",
    "movie", "late", "status", "report", "review", "upload", "download", "post", "like",
    "ok", "okay", "sorry", "thanks", "plz", "please", "bro", "sir", "mam", "result"
}

ACRONYMS = {"pr", "otp", "wfh", "url", "api", "ui", "ux", "id", "sms", "ai", "ml", "llm", "hr"}

class CodeSwitchTagger:
    def __init__(self):
        self.english_vocab = ENGLISH_LOANWORDS
        self.acronyms = ACRONYMS

    def tokenize(self, text: str) -> List[str]:
        """Splits text preserving words and punctuation."""
        return re.findall(r"\w+|[^\w\s]|\s+", text, re.UNICODE)

    def tag_token(self, token: str) -> Dict[str, Any]:
        """Classify a single token."""
        if token.isspace():
            return {"token": token, "type": "WHITESPACE"}
        
        if re.match(r"^[\d\.,\-\/:]+$", token):
            return {"token": token, "type": "NUMERIC"}
            
        if re.match(r"^[^\w\s]+$", token):
            return {"token": token, "type": "PUNCTUATION"}

        lower_t = token.lower()
        if lower_t in self.acronyms:
            return {"token": token, "type": "ACRONYM", "normalized": lower_t}

        if lower_t in self.english_vocab:
            return {"token": token, "type": "ENGLISH_LOAN", "normalized": lower_t}

        return {"token": token, "type": "HINDI_ROMAN", "normalized": lower_t}

    def analyze_sentence(self, text: str) -> List[Dict[str, Any]]:
        """Tag all tokens in a sentence."""
        raw_tokens = self.tokenize(text)
        return [self.tag_token(t) for t in raw_tokens]

