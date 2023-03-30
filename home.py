import streamlit as st
import cv2
import pytesseract
import matplotlib.pyplot as plt
import pandas as pd

st.write("Hello world")

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

def draw_boxes(image, boxes, color, thickness):
    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    return image

uploaded_file = st.file_uploader(label="Upload an image", accept_multiple_files=False,
                type=["jpg", "jpeg", "png"], key=None)

submit_button = st.button("Run OCR")

if submit_button:

    if uploaded_file is not None:

        st.image(uploaded_file, caption="Uploaded image", use_column_width=True)
        image = cv2.imread(uploaded_file)
        lang = 'eng'
        extracted_text = pytesseract.image_to_string(uploaded_file, lang=lang)
        print(extracted_text)


    else:
        # Display an error message if no file was uploaded
        st.error("Please upload an image file.")

