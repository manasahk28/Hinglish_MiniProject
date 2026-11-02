"""
Streamlit Web Application: Hinglish Smart Writing Assistant.
Interactive frontend for Transliteration, Phrasing Refinement, and Translation.
"""

import json
import streamlit as st
import pandas as pd
from pathlib import Path

from src.agent.writing_assistant import HinglishWritingAssistant
from src.evaluation.metrics import evaluate_prediction
from src.config import TEST_CASES_PATH, TEST_EVAL_PATH, PHRASING_STYLES

# Page Configuration
st.set_page_config(
    page_title="Hinglish Smart Writing Assistant",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .token-badge {
        display: inline-block;
        padding: 2px 8px;
        margin: 2px;
        border-radius: 4px;
        font-size: 0.85rem;
    }
    .badge-hindi { background-color: #DBEAFE; color: #1E40AF; }
    .badge-loan { background-color: #FEF3C7; color: #92400E; }
    .badge-acronym { background-color: #FCE7F3; color: #9D174D; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_assistant():
    return HinglishWritingAssistant()

@st.cache_data
def load_test_data():
    cases = []
    if Path(TEST_CASES_PATH).exists():
        with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
            cases = json.load(f)
    
    eval_data = {}
    if Path(TEST_EVAL_PATH).exists():
        with open(TEST_EVAL_PATH, "r", encoding="utf-8") as f:
            eval_data = json.load(f)
            
    return cases, eval_data

assistant = load_assistant()
test_cases, eval_results = load_test_data()

# Sidebar Navigation & Settings
st.sidebar.title("🛠️ Assistant Settings")

app_mode = st.sidebar.radio(
    "Choose Mode:",
    ["Interactive Editor", "Benchmark Dashboard (45 Test Cases)", "Failure Analysis Guide"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Pipeline Configuration")
target_style = st.sidebar.selectbox("Phrasing Tone:", PHRASING_STYLES, index=0)
preserve_loanwords = st.sidebar.checkbox("Preserve English Loanwords (Keep in Latin)", value=False)
enable_translation = st.sidebar.checkbox("Enable English Translation", value=True)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Core Engines:**\n"
    "- Transliteration: AI4Bharat IndicXlit / Aksharantar\n"
    "- Phrasing: BharatGen Param1 Few-Shot / Grammar Refiner\n"
    "- Translation: AI4Bharat IndicTrans2\n"
    "- Evaluation: CER, WER, SacreBLEU, chrF"
)

# MODE 1: Interactive Editor
if app_mode == "Interactive Editor":
    st.markdown('<div class="main-title">✍️ Hinglish Smart Writing Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Convert Roman Hinglish to native Devanagari script, refine tone/grammar, and optionally translate to English.</div>', unsafe_allow_html=True)

    # Preset selector for quick demo
    preset_options = ["Custom Input"] + [f"Case #{c['id']}: {c['hinglish_input'][:40]}..." for c in test_cases[:10]]
    selected_preset = st.selectbox("Quick Sample Presets:", preset_options)

    default_text = "bhai kaisa hai tu, bohot din se baat nahi hui"
    if selected_preset != "Custom Input":
        idx = int(selected_preset.split(":")[0].replace("Case #", "")) - 1
        default_text = test_cases[idx]["hinglish_input"]

    user_input = st.text_area("Enter Roman-script Hinglish text:", value=default_text, height=100)

    if st.button("🚀 Process & Refine", type="primary"):
        if not user_input.strip():
            st.warning("Please enter some Hinglish text to process.")
        else:
            with st.spinner("Processing through Transliteration, GenAI Phrasing & Translation..."):
                res = assistant.process(
                    user_input,
                    style=target_style,
                    preserve_english_loanwords=preserve_loanwords,
                    translate_to_english=enable_translation
                )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("1. Devanagari Script (Transliteration)")
                st.info(res["devanagari"])

                st.subheader("2. Refined Phrasing (" + target_style + ")")
                st.success(res["phrasing"]["refined_text"])

            with col2:
                st.subheader("3. English Translation (IndicTrans2)")
                if res["translation"]:
                    st.info(res["translation"])
                else:
                    st.write("*(Translation disabled)*")

                st.subheader("4. Code-Switching Token Analysis")
                summary = res["code_switch_summary"]
                st.write(
                    f"**Tokens:** Hindi Roman: `{summary.get('HINDI_ROMAN', 0)}` | "
                    f"English Loanwords: `{summary.get('ENGLISH_LOAN', 0)}` | "
                    f"Acronyms: `{summary.get('ACRONYM', 0)}`"
                )

            # Detailed Token Classification
            with st.expander("🔍 Inspect Token-by-Token Alignments & Code-Mixing"):
                df_tokens = pd.DataFrame(res["tokens"])
                if not df_tokens.empty:
                    st.dataframe(df_tokens, use_container_width=True)

            # Multi-style Comparison
            with st.expander("🎭 Compare All Phrasing Styles"):
                all_styles = assistant.process_all_styles(user_input)
                comparison_data = []
                for style_name, s_res in all_styles.items():
                    comparison_data.append({
                        "Tone / Style": style_name,
                        "Refined Hindi Output": s_res["phrasing"]["refined_text"]
                    })
                st.table(pd.DataFrame(comparison_data))

# MODE 2: Benchmark Dashboard
elif app_mode == "Benchmark Dashboard (45 Test Cases)":
    st.markdown('<div class="main-title">📊 Quantitative Evaluation Benchmark</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Evaluation on 45 representative test cases across 6 distinct linguistic categories.</div>', unsafe_allow_html=True)

    if eval_results:
        summary = eval_results.get("overall_summary", {})
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Cases", summary.get("total_test_cases", 0))
        col1.markdown("<small>Representative dataset</small>", unsafe_allow_html=True)
        col2.metric("Mean CER", f"{summary.get('mean_CER', 0.0):.3f}")
        col2.markdown("<small>Character Error Rate (lower is better)</small>", unsafe_allow_html=True)
        col3.metric("Word Accuracy", f"{summary.get('mean_Word_Accuracy', 0.0)}%")
        col3.markdown("<small>Exact word match ratio</small>", unsafe_allow_html=True)
        col4.metric("Mean BLEU", f"{summary.get('mean_BLEU', 0.0):.2f}")
        col4.markdown("<small>Translation n-gram precision</small>", unsafe_allow_html=True)
        col5.metric("Mean chrF", f"{summary.get('mean_chrF', 0.0):.2f}")
        col5.markdown("<small>Character n-gram F-score</small>", unsafe_allow_html=True)

        st.markdown("### 📂 Category Performance Breakdown")
        cat_summary = eval_results.get("category_summary", {})
        cat_df = pd.DataFrame.from_dict(cat_summary, orient="index")
        cat_df.index.name = "Category"
        cat_df.reset_index(inplace=True)
        st.dataframe(cat_df, use_container_width=True)

        st.markdown("### 📋 Test Case Inspector")
        category_filter = st.selectbox(
            "Filter by Linguistic Category:",
            ["All"] + list(cat_summary.keys())
        )

        test_records = eval_results.get("test_cases", [])
        if category_filter != "All":
            test_records = [r for r in test_records if r["category"] == category_filter]

        table_rows = []
        for r in test_records:
            table_rows.append({
                "ID": r["id"],
                "Category": r["category"],
                "Hinglish Input": r["input"],
                "Hypothesis Devanagari": r["hyp_devanagari"],
                "Reference Devanagari": r["ref_devanagari"],
                "CER": r["metrics"]["CER"],
                "Word Acc (%)": r["metrics"]["Word_Accuracy"],
                "Translation": r["hyp_translation"],
                "Notes": r["notes"]
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True)
    else:
        st.warning("No evaluated benchmark results found. Run `python -m src.evaluation.evaluator` to generate them.")

# MODE 3: Failure Analysis Guide
else:
    st.markdown('<div class="main-title">🔬 Error Analysis & Failure Modes</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Systematic linguistic breakdown of error categories in Hinglish Processing.</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 1. Phonetic Homograph Ambiguity
    - **Problem**: In Latin script, words with different meanings share the same romanization (e.g. *kaha* = "कहा" (said) vs "कहाँ" (where); *me* = "में" (in) vs "मे" (May)).
    - **Mitigation**: Disambiguation using contextual syntactic n-grams (presence of question marks, verbs like *ja rahe*).

    ### 2. Code-Switching & English Loanwords
    - **Problem**: Words like *meeting*, *presentation*, *server* when transliterated character-by-character into Devanagari can produce variations (e.g. "मीटिंग" vs "मीटिग") causing higher CER against pure Sanskritized benchmarks.
    - **Mitigation**: Dual-mode transliteration allowing users to either preserve Latin loanwords or phonetically render them.

    ### 3. SMS & Social Media Slang Contractions
    - **Problem**: Users write heavily truncated forms (e.g. *h* -> है, *nhi* -> नहीं, *plz* -> प्लीज, *krna* -> करना, *v* -> भी).
    - **Mitigation**: Integrated Aksharantar slang normalizer mapping common SMS shortforms before phonetic decomposition.

    ### 4. Subject-Verb Gender Agreement in Code-Mixed Contexts
    - **Problem**: Code-mixed Hindi assigns grammatical genders inconsistently to English nouns (e.g. *"मेरा मीटिंग"* vs *"मेरी बैठक"*).
    - **Mitigation**: GenAI phrasing module trained with few-shot in-context examples to enforce gender-agreement consistency in Formal mode.
    """)
