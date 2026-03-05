import streamlit as st
import google.generativeai as genai
from pdf2image import convert_from_bytes
import PIL.Image
import io

# App Layout
st.set_page_config(page_title="P&ID Analyzer", page_icon="🏗️")
st.title("🏗️ P&ID Process Description Generator")

# API Key Input (Sidebar)
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)

# File Uploader
uploaded_file = st.file_uploader("Upload a P&ID (PDF)", type="pdf")

if uploaded_file and api_key:
    if st.button("Generate Description"):
        with st.spinner("Analyzing diagram..."):
            # 1. Convert PDF to Image
            images = convert_from_bytes(uploaded_file.read(), dpi=300)
            img = images[0] # Analyze the first page
            
            # 2. Setup Gemini
            model = genai.GenerativeModel(model_name='models/gemini-1.5-pro')
            prompt = "Identify all major equipment tags and write a sequential process description for this P&ID."
            
            # 3. Get Response
            response = model.generate_content([prompt, img])
            
            st.subheader("Process Description")
            st.write(response.text)
elif not api_key:
    st.info("Please enter your API Key in the sidebar to begin.")
