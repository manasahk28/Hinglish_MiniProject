"""
Evaluation metrics for Transliteration and Translation.
Computes:
- Character Error Rate (CER)
- Word Error Rate (WER)
- Word Accuracy (1 - WER, bounded [0, 1])
- Translation Quality (BLEU & chrF)
"""

from typing import List, Dict, Any, Union, Sequence
import re

def _levenshtein_distance(s1: Sequence, s2: Sequence) -> int:
    """Computes basic Levenshtein distance over any sequence of elements."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def compute_cer(reference: str, hypothesis: str) -> float:
    """
    Computes Character Error Rate (CER).
    CER = Levenshtein_Chars(ref, hyp) / len(ref)
    """
    ref = reference.strip()
    hyp = hypothesis.strip()
    if not ref:
        return 0.0 if not hyp else 1.0

    try:
        import jiwer
        return float(jiwer.cer(ref, hyp))
    except Exception:
        dist = _levenshtein_distance(list(ref), list(hyp))
        return dist / max(1, len(ref))

def compute_wer(reference: str, hypothesis: str) -> float:
    """
    Computes Word Error Rate (WER).
    WER = Levenshtein_Words(ref, hyp) / len(ref_words)
    """
    ref = reference.strip()
    hyp = hypothesis.strip()
    if not ref:
        return 0.0 if not hyp else 1.0

    try:
        import jiwer
        return float(jiwer.wer(ref, hyp))
    except Exception:
        ref_words = ref.split()
        hyp_words = hyp.split()
        dist = _levenshtein_distance(ref_words, hyp_words)
        return dist / max(1, len(ref_words))

def compute_word_accuracy(reference: str, hypothesis: str) -> float:
    """
    Computes Word Accuracy percentage (1 - WER bounded in [0, 1]).
    """
    wer = compute_wer(reference, hypothesis)
    return max(0.0, 1.0 - wer)

def compute_bleu(reference: Union[str, List[str]], hypothesis: str) -> float:
    """
    Computes BLEU score for machine translation using sacrebleu.
    """
    if isinstance(reference, str):
        references = [reference]
    else:
        references = reference

    if not hypothesis.strip():
        return 0.0

    try:
        import sacrebleu
        score = sacrebleu.sentence_bleu(hypothesis, references).score
        return round(float(score), 2)
    except Exception:
        # Simple n-gram precision fallback
        hyp_tokens = hypothesis.lower().split()
        ref_tokens = references[0].lower().split()
        if not hyp_tokens:
            return 0.0
        matches = sum(1 for w in hyp_tokens if w in ref_tokens)
        return round((matches / max(1, len(hyp_tokens))) * 100.0, 2)

def compute_chrf(reference: Union[str, List[str]], hypothesis: str) -> float:
    """
    Computes chrF score (character n-gram F-score) for translation quality.
    """
    if isinstance(reference, str):
        references = [reference]
    else:
        references = reference

    if not hypothesis.strip():
        return 0.0

    try:
        import sacrebleu
        score = sacrebleu.sentence_chrf(hypothesis, references).score
        return round(float(score), 2)
    except Exception:
        return 0.0

def evaluate_prediction(
    ref_devanagari: str,
    hyp_devanagari: str,
    ref_translation: str,
    hyp_translation: str
) -> Dict[str, float]:
    """Computes all primary evaluation metrics in one call."""
    cer = compute_cer(ref_devanagari, hyp_devanagari)
    wer = compute_wer(ref_devanagari, hyp_devanagari)
    word_acc = compute_word_accuracy(ref_devanagari, hyp_devanagari)
    bleu = compute_bleu(ref_translation, hyp_translation)
    chrf = compute_chrf(ref_translation, hyp_translation)

    return {
        "CER": round(cer, 4),
        "WER": round(wer, 4),
        "Word_Accuracy": round(word_acc * 100.0, 2),
        "BLEU": bleu,
        "chrF": chrf
    }

