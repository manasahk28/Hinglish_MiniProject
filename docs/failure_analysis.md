# Quantitative Error Analysis & Linguistic Failure Modes

## 1. Executive Summary
This document provides a systematic failure analysis for the **Hinglish Smart Writing Assistant**, evaluated on a curated dataset of **45 representative test cases** across **6 distinct linguistic categories**. Hinglish (Hindi written in Roman/Latin script with extensive English code-switching) introduces distinct NLP challenges that do not exist in standard mono-script or single-language settings.

### Benchmark Evaluation Summary
- **Total Test Cases**: 45
- **Mean Character Error Rate (CER)**: `0.1890` (18.9%)
- **Mean Word Error Rate (WER)**: `0.3530` (35.3%)
- **Mean Word Accuracy**: `64.70%`
- **Mean Translation BLEU**: `1.56`
- **Mean chrF**: `5.33`

---

## 2. Category-Wise Performance Breakdown

| Linguistic Category | Sample Count | Mean CER | Mean WER | Word Accuracy (%) | Dominant Error Type |
|---|---|---|---|---|---|
| **Daily Conversational** | 8 | **0.0822** | **0.2045** | **79.55%** | Minor vowel elongation (*acchi* vs *achi*) |
| **Ambiguous Phonetics & Homographs** | 7 | **0.0887** | **0.2109** | **78.91%** | Contextual homographs (*kaha* where vs said) |
| **Slang & SMS Abbreviations** | 5 | **0.1324** | **0.2260** | **77.40%** | Unseen contractions (*wfh*, *gud*) |
| **Complex Syntax & Conditionals** | 6 | **0.1850** | **0.4048** | **59.52%** | Correlative conjunctions & compound verbs |
| **Politeness & Formal Communication** | 6 | **0.2278** | **0.4292** | **57.08%** | Sanskritized vocabulary drift (*khed*, *asuvidha*) |
| **Numbers, Dates & Technical Codes** | 5 | **0.2449** | **0.4159** | **58.41%** | Alphanumeric tokens & ordinal markers (*15th*) |
| **Workplace & Tech Code-Mixing** | 8 | **0.3581** | **0.5699** | **43.01%** | Over-transliteration of English loanwords |

---

## 3. Systematic Breakdown of Failure Categories

### Error Type A: Phonetic Homographs & Multi-Word Ambiguity
- **Description**: The Latin script lacks the phonological distinctions inherent to Devanagari (such as dental vs retroflex consonants, vowel length distinctions, and nasalized vowels).
- **Representative Failure Cases**:
  - `kaha`:
    - Context 1 (*"usne kaha ki wo kal aayega"*) -> Correct: `कहा` (said).
    - Context 2 (*"tum kal kaha ja rahe the?"*) -> Correct: `कहाँ` (where).
  - `mai` / `me`:
    - Case 19: *"mai bhi wahi soch raha tha"* -> Subject pronoun `मैं`.
    - Case 20: *"room me andhera hai"* -> Locative postposition `में`.
  - `bat`:
    - Ambiguous between `बात` (discussion/topic) and English loanword `बैट` (cricket bat).
- **Mitigation Implemented**: Contextual n-gram tagger checking punctuation (e.g. `?`) and adjacent verbs/pronouns (`bhi`, `soch`, `ja`).

### Error Type B: Over-Transliteration of English Technical Loanwords
- **Description**: When technical terms such as *schedule*, *documentation*, *presentation*, *pull request (PR)*, *invoice* are subjected to character-level phonetic transliteration, they produce awkward or non-standard Devanagari spellings (e.g., `schedule` -> `स्चेदुले` instead of `शेड्यूल`).
- **Impact**: Accounts for the highest CER (`0.3581`) in the Workplace & Tech category.
- **Mitigation Implemented**: 
  - Token-level `CodeSwitchTagger` identifying English vocabulary and acronyms.
  - User-configurable toggle: **Preserve English Loanwords** (keeps loanwords in clean Latin script) vs **Phonetic Conversion**.

### Error Type C: Extreme SMS Contractions and Vowel Deletion
- **Description**: Texting conventions drop vowels and auxiliary verb characters:
  - `h` -> `है`
  - `krna` -> `करना`
  - `plz` -> `प्लीज़`
  - `shi` -> `सही`
  - `bhot` -> `बहुत`
- **Mitigation Implemented**: High-priority Aksharantar slang lookup table executing before phonetic syllable decomposition.

### Error Type D: Grammatical Gender Discord in Code-Mixed Hindi
- **Description**: English nouns borrowed into Hinglish lack intrinsic grammatical gender. Speakers frequently mix gender agreements:
  - Input: *"mera meeting 3 baje schedule hai"*
  - Grammatical Issue: In Hindi, "meeting" (बैठक) is feminine, necessitating *"मेरी"*.
- **Mitigation Implemented**: GenAI Phrasing module with few-shot in-context learning to normalize subject-verb-gender agreement in **Standard Formal** mode.

---

## 4. Key Takeaways for Future Model Improvement
1. **Hybrid Neural-Rule Pipeline**: Relying purely on neural sequence-to-sequence transliteration without code-switch token boundary awareness leads to corrupted technical jargon. A hybrid tokenizer + lexicon lookup outperforms end-to-end models on text messages.
2. **Context Window Expansion**: Disambiguating homographs like *kaha* requires sentence-level syntactic parsing rather than isolated token transliteration.
3. **Domain-Specific Fine-Tuning**: Fine-tuning BharatGen / IndicTrans2 on conversational Hinglish chat corpora (e.g., LinCE, Hinglish-TOP) substantially reduces translation distortion.

