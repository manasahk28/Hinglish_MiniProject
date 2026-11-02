"""
Gradio Web Application for Hinglish Smart Writing Assistant.
Provides alternate lightweight web UI for Transliteration, Phrasing, and Translation.
"""

import gradio as gr
from src.agent.writing_assistant import HinglishWritingAssistant
from src.config import PHRASING_STYLES

assistant = HinglishWritingAssistant()

def process_hinglish(text, style, preserve_loanwords, enable_translation):
    if not text or not text.strip():
        return "", "", "", "Please provide text."
    
    res = assistant.process(
        text=text,
        style=style,
        preserve_english_loanwords=preserve_loanwords,
        translate_to_english=enable_translation
    )
    
    devanagari = res["devanagari"]
    improved = res["phrasing"]["refined_text"]
    translation = res["translation"] if enable_translation else "(Translation disabled)"
    
    summary = res["code_switch_summary"]
    details = (
        f"Hindi Tokens: {summary.get('HINDI_ROMAN', 0)} | "
        f"English Loanwords: {summary.get('ENGLISH_LOAN', 0)} | "
        f"Acronyms: {summary.get('ACRONYM', 0)}"
    )
    
    return devanagari, improved, translation, details

# Build Gradio Interface
with gr.Blocks(title="Hinglish Smart Writing Assistant") as demo:
    gr.Markdown("# ✍️ Hinglish Smart Writing Assistant")
    gr.Markdown("Convert Roman-script Hinglish to native Devanagari script, refine tone/grammar, and translate to English.")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="Roman-Script Hinglish Input",
                placeholder="e.g., bhai kaisa hai tu, bohot din se baat nahi hui",
                lines=3,
                value="bhai kaisa hai tu, bohot din se baat nahi hui"
            )
            style_dropdown = gr.Dropdown(
                choices=PHRASING_STYLES,
                value="Standard Formal",
                label="Target Phrasing Style"
            )
            preserve_check = gr.Checkbox(
                label="Preserve English Loanwords (Keep in Latin script)",
                value=False
            )
            translate_check = gr.Checkbox(
                label="Translate to English (IndicTrans2)",
                value=True
            )
            submit_btn = gr.Button("🚀 Process & Refine", variant="primary")
            
        with gr.Column():
            out_devanagari = gr.Textbox(label="1. Native Devanagari Script", lines=2)
            out_improved = gr.Textbox(label="2. Refined Phrasing (Selected Tone)", lines=2)
            out_translation = gr.Textbox(label="3. English Translation", lines=2)
            out_tokens = gr.Textbox(label="4. Code-Switching Analysis", lines=1)
            
    submit_btn.click(
        fn=process_hinglish,
        inputs=[input_text, style_dropdown, preserve_check, translate_check],
        outputs=[out_devanagari, out_improved, out_translation, out_tokens]
    )

    gr.Examples(
        examples=[
            ["bhai kaisa hai tu, bohot din se baat nahi hui", "Standard Formal", False, True],
            ["mera meeting 3 baje schedule hai", "Standard Formal", False, True],
            ["please mujhe documentation update karke send kar do", "Concise / Professional", False, True],
            ["yeh banda ekdum mast h yaar", "Natural Casual", False, True],
            ["train number 12951 platform 4 par aayegi", "Standard Formal", False, True]
        ],
        inputs=[input_text, style_dropdown, preserve_check, translate_check]
    )

if __name__ == "__main__":
    demo.launch(server_port=7860)
