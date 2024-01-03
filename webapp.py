import streamlit as st
from gtts import gTTS
from io import BytesIO
from fpdf import FPDF
from PIL import Image
import numpy as np
import pytesseract
from docx2pdf import convert

def text_to_speech(text, lang='en', slow_speed=False):
    tts = gTTS(text, lang=lang, slow=slow_speed)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

def text_to_pdf(text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=text_content)
    return pdf

def image_to_text(uploaded_image):
    # Open the uploaded image with PIL
    image = Image.open(uploaded_image)

    # Use Tesseract to perform OCR on the image
    text = pytesseract.image_to_string(image)
    return text
def main():
    st.title("Text Tools App")

    # Set tabs
    tabs = ["Home", "Text to Speech", "Text to PDF", "Word to PDF", "Image to Text", "About"]
    selected_tab = st.sidebar.radio("Navigation", tabs)

    # Centered title inside a container
    with st.container():
        st.markdown("<h1 style='text-align: center;'>Text Tools App</h1>", unsafe_allow_html=True)

    if selected_tab == "Home":
        st.write("Welcome to the Text Tools App!")
        st.header("Quick Access")
        selected_tool = st.selectbox("Choose a Tool", ["Text to Speech", "Text to PDF", "Word to PDF", "Image to Text"])
        if selected_tool == "Text to Speech":
            st.write("Convert text to speech in various languages.")
        elif selected_tool == "Text to PDF":
            st.write("Convert text to a PDF file.")
        elif selected_tool == "Word to PDF":
            st.write("Convert Word documents to PDF.")
        elif selected_tool == "Image to Text":
            st.write("Extract text from an image using OCR.")

    elif selected_tab == "Text to Speech":
        st.title("Text-to-Speech Conversion")

        text_input_tts = st.text_area("Enter text to convert to speech")
        languages_tts = {'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de'}
        selected_lang_tts = st.selectbox('Select Language', list(languages_tts.keys()))
        slow_speed_tts = st.checkbox('Slow Speed')

        if st.button("Convert to Speech"):
            if text_input_tts:
                lang_code_tts = languages_tts[selected_lang_tts]
                audio = text_to_speech(text_input_tts, lang=lang_code_tts, slow_speed=slow_speed_tts)
                st.audio(audio.read(), format='audio/mp3')
            else:
                st.warning("Please enter some text.")

    elif selected_tab == "Text to PDF":
        st.title("Text-to-PDF Conversion")

        text_input_pdf = st.text_area("Enter text to convert to PDF")

        if st.button("Convert to PDF"):
            if text_input_pdf:
                pdf = text_to_pdf(text_input_pdf)
                st.download_button("Download PDF", pdf.output(dest="S").encode("latin-1"), file_name="converted_text.pdf", mime="application/pdf")
            else:
                st.warning("Please enter some text.")

    elif selected_tab == "Word to PDF":
        st.title("Word-to-PDF Conversion")

        uploaded_file = st.file_uploader("Upload a Word document", type=["docx"])

        if uploaded_file is not None:
            convert(uploaded_file)

            st.success("Conversion successful! Please download the converted PDF.")

            converted_pdf_path = uploaded_file.name.replace(".docx", ".pdf")
            with open(converted_pdf_path, "rb") as file:
                pdf_bytes = file.read()
                st.download_button("Download PDF", pdf_bytes, file_name=converted_pdf_path)

    elif selected_tab == "Image to Text":
        st.title("Image-to-Text Extraction")

        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            extracted_text = image_to_text(uploaded_image)
            st.subheader("Extracted Text:")
            st.write(extracted_text)

    elif selected_tab == "About":
        st.title("About Text Tools App")
        st.header("Operations Overview")

        st.subheader("Text to Speech")
        st.write("""
            The 'Text to Speech' tab allows you to convert entered text into speech.
            Choose a language and adjust the speed to convert text into audio files.
            """)

        st.subheader("Text to PDF")
        st.write("""
            In the 'Text to PDF' tab, you can convert entered text into a downloadable PDF file.
            """)

        st.subheader("Word to PDF")
        st.write("""
            The 'Word to PDF' tab enables you to upload a Word document and convert it to a PDF file.
            """)

if __name__ == "__main__":
    main()
