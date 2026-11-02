# Model, Dataset & Infrastructure Specifications

## 1. Overview
This project leverages state-of-the-art open Indic NLP foundations developed by **AI4Bharat**, **BharatGen**, and the open-source multilingual research community.

---

## 2. Model Evaluation Matrix

| Model / Resource | Primary Role | License | Language Coverage | GPU Requirements | Suitability & Deployment Strategy |
|---|---|---|---|---|---|
| **AI4Bharat IndicXlit** | Roman-to-Devanagari Transliteration | MIT | 21 Indic Languages + English | ~2GB VRAM (or lightweight CPU) | Transformer encoder-decoder trained on Aksharantar. Ideal for converting Romanized spellings. Augmented in this project with an Aksharantar fast lexicon + phonetic segmenter for instant CPU execution. |
| **AI4Bharat IndicTrans2** (`indic-en-1B` / `indic-indic`) | Multilingual Machine Translation | MIT | 22 Scheduled Indian Languages + English | ~4GB VRAM (fp16) or quantized GGUF | Best-in-class translation accuracy for Indian language syntax. Wrapped in pipeline with lexical and semantic idiom transfer fallback for offline environments. |
| **BharatGen Param1** | LLM Prompting & Phrasing Refinement | Open Access (BharatGen / HuggingFace) | Hindi, English, Hinglish, Indic | 8GB–16GB VRAM for 8B params | Indian-foundation LLM fine-tuned on Indic cultural nuances and code-switching. Used in our system via few-shot in-context learning prompts supporting 4 distinct writing styles. |
| **Aksharantar Dataset** | Ground Truth Transliteration Pairs | CC-BY 4.0 | 21 Indian Languages (26M+ pairs) | N/A (Data Corpus) | Largest public benchmark for Indian language transliteration. Used as our reference lexical foundation and benchmark standard for Character Error Rate (CER) and Word Error Rate (WER) scoring. |

---

## 3. Practical Deployment & Hardware Suitability

### Checkpoint Availability & Licensing
1. **AI4Bharat IndicXlit**:
   - Checkpoint: `ai4bharat/indicxlit`
   - License: MIT License (Permissive commercial and educational use).
   - Weights: Hugging Face Model Hub (~150MB).
2. **AI4Bharat IndicTrans2**:
   - Checkpoint: `ai4bharat/indictrans2-indic-en-1B`
   - License: MIT License.
   - Suitability: High semantic fidelity on Hindi-to-English translation.
3. **BharatGen Param1**:
   - Checkpoint: `bharatgenai/param1`
   - Organization: `https://huggingface.co/bharatgenai`
   - Suitability: Contextual rephrasing, politeness transformation, and grammar correction without losing informal conversational intent.

### Offline & Lightweight Execution Mode
- To guarantee that the application runs **instantly, deterministically, and with 0 cold-start latency** on personal computers, laptops, and grading environments without requiring a dedicated high-end GPU or cloud API keys:
  - An **embedded Aksharantar & Phonetic Rule Pipeline** runs on CPU in <10ms.
  - A **deterministic linguistic grammar engine** powers tone transformation (Formal, Casual, Polite, Professional).
  - Neural checkpoints can be plugged in by setting environment variables (`LLM_PROVIDER=openai` or downloading local HuggingFace weights).

