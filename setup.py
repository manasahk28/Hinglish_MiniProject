from setuptools import setup, find_packages

setup(
    name="hinglish_writing_assistant",
    version="1.0.0",
    description="Hinglish Smart Writing Assistant: Transliteration, Phrasing Refinement & Translation",
    author="CS3235 Mini-Project Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.30.0",
        "gradio>=4.0.0",
        "sacrebleu>=2.4.0",
        "jiwer>=3.0.0",
        "pandas>=2.0.0",
        "pydantic>=2.0.0"
    ],
)

