"""
Few-shot prompting templates for Hinglish & Hindi Phrasing Improvement.
Designed for BharatGen Param1, Gemini, and open LLMs.
"""

SYSTEM_PROMPT = """You are an expert bilingual Hinglish & Hindi Writing Assistant.
Your goal is to refine and improve user inputs written in Roman Hinglish or Devanagari Hindi into high-quality, grammatically sound, contextually appropriate phrasing while preserving the core meaning.
You must adhere strictly to the requested tone:
- Standard Formal: Pure, polite, grammatically perfect Hindi suitable for documentation and official communication.
- Natural Casual: Conversational, friendly Hindi suitable for texting and informal chats.
- Polite / Respectful: Courteous tone emphasizing respect ('आप', 'कृपया', 'कीजिए').
- Concise / Professional: Direct, crisp corporate/technical communication.
"""

FEW_SHOT_EXAMPLES = [
    {
        "input": "bhai kaisa hai tu, bohot din se baat nahi hui",
        "formal": "भाई, आप कैसे हैं? काफी दिनों से आपसे बात नहीं हुई।",
        "casual": "भाई कैसा है तू? बहुत दिनों से बात नहीं हुई यार।",
        "polite": "भाई साहब, आप कैसे हैं? आशा है सब कुशल मंगल होगा, बहुत दिनों से संपर्क नहीं हुआ।",
        "professional": "नमस्कार, आशा है आप सकुशल हैं। काफी समय से आपसे चर्चा नहीं हो पाई।"
    },
    {
        "input": "mera meeting 3 baje schedule hai",
        "formal": "मेरी बैठक 3:00 बजे निर्धारित है।",
        "casual": "मेरी मीटिंग 3 बजे शेड्यूल्ड है।",
        "polite": "कृपया ध्यान दें कि मेरी बैठक 3 बजे निर्धारित की गई है।",
        "professional": "मेरी निर्धारित बैठक दोपहर 3:00 बजे है।"
    },
    {
        "input": "please mujhe documentation update karke send kar do",
        "formal": "कृपया मुझे दस्तावेज़ अद्यतन करके प्रेषित कर दीजिए।",
        "casual": "प्लीज डॉक्यूमेंटेशन अपडेट करके मुझे भेज दो।",
        "polite": "आपसे विनम्र निवेदन है कि दस्तावेज़ को अपडेट करके मुझे प्रेषित करने का कष्ट करें।",
        "professional": "कृपया अद्यतित दस्तावेज़ मुझे प्रेषित करें।"
    },
    {
        "input": "server down hai isliye bug fix nahi ho pa raha",
        "formal": "सर्वर डाउन होने के कारण तकनीकी त्रुटि का निवारण नहीं हो पा रहा है।",
        "casual": "सर्वर डाउन है, इसलिए बग ठीक नहीं हो पा रहा।",
        "polite": "सर्वर डाउन होने के कारण बग ठीक करने में असमर्थ हूँ, कृपया थोड़ा समय दें।",
        "professional": "सर्वर अनुपलब्धता के कारण त्रुटि निवारण कार्य लंबित है।"
    }
]

def build_refinement_prompt(text: str, devanagari_text: str, target_style: str) -> str:
    """Builds the prompt for LLM rewriting."""
    examples_str = ""
    for ex in FEW_SHOT_EXAMPLES:
        examples_str += f"""
Input: {ex['input']}
Target ({target_style}): {ex.get(target_style.lower().split()[0], ex['formal'])}
"""

    prompt = f"""{SYSTEM_PROMPT}

Examples of phrasing refinement:
{examples_str}

Now refine the following sentence:
Original Input: {text}
Transliterated Devanagari: {devanagari_text}
Requested Style: {target_style}

Output only the refined Hindi sentence without any preamble or explanation.
Refined Sentence:"""
    return prompt

