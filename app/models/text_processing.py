import re
import pymorphy3
import os
from striprtf.striprtf import rtf_to_text


morph = pymorphy3.MorphAnalyzer()


def clean_text(text):
    """Clean and lemmatize text"""
    # Remove everything except letters and spaces
    text = re.sub(r'[^а-яА-ЯёЁ\s]', '', text)

    # Convert to lowercase
    text = text.lower()

    # Split into words and lemmatize
    words = text.split()
    lemmas = [morph.parse(word)[0].normal_form for word in words]

    return ' '.join(lemmas)


def read_rtf_files(folder_path):
    """Read all RTF files in a directory"""
    rtf_files_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".rtf"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                rtf_content = f.read()
                text = rtf_to_text(rtf_content)
                rtf_files_data.append({"name": filename, "content": text})
    return rtf_files_data
