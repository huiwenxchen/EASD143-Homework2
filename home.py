import streamlit as st
import pytesseract
import pandas as pd
import cv2
from PIL import Image
import tempfile
import os
import numpy as np



def process_image(image, languages):
    # Read the image using OpenCV
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Perform OCR using tesseract
    extracted_text = pytesseract.image_to_string(img, lang=languages)

    return extracted_text

st.title("OCR Workflow X Streamlit")

uploaded_files = st.file_uploader("Upload one or multiple image files for OCR", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

language_options = {
    "English": "eng",
    "Chinese": "chi_sim",
    "French": "fra",
    "Japanese": "jpn",
    "Korean": "kor"
}
languages = st.multiselect("Select the language(s) for OCR", list(language_options.keys()), default=["English"])
button = st.button("Process Images")

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

if button:
    if uploaded_files and languages:
        ocr_output = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file.flush()
                img = Image.open(temp_file.name)
                extracted_text = process_image(img, "+".join([language_options[lang] for lang in languages]))
                ocr_output.append({"File Name": uploaded_file.name, "Extracted Text": extracted_text})

        ocr_output_df = pd.DataFrame(ocr_output)
        st.write(ocr_output_df)
        csv = convert_df(ocr_output_df)
        save_button = st.download_button(
            "Press to save as CSV",
            csv,
            "ocr_putput.csv",
            "text/csv",
            key='download-csv'
        )
        if save_button:
            st.write("File saved successfully!")

    else:
        st.warning("Please upload image file(s) and/or select language(s) before processing OCR.")

