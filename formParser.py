import google.generativeai as genai
import streamlit as st
import openai
import json
import os
import tempfile
import pdfplumber
from PIL import Image
import pytesseract
from datetime import datetime
import re


genai.configure(api_key="")

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n\n"
    return text if text.strip() else None  # Return None if no text found

# Function to extract text from an image (for scanned PDFs)
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

# Function to extract key-value pairs using GPT-4
def extract_all_key_value_pairs(text):
    """Uses Gemini to extract key-value pairs from text."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""Extract the key-value pairs from the following document text. 
    Output only the pairs in this format: Key: Value. Avoid additional commentary.

    Text:
    {text}
    """

    response = model.generate_content(prompt)

    # Convert response text to a dictionary
    key_value_dict = {}
    if response.text:
        for line in response.text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key_value_dict[key.strip()] = value.strip()

    return key_value_dict
  # Return as dictionary

# Function to calculate age if Date of Birth is present
def calculate_age(dob_string):
    """Auto-calculates age from Date of Birth (if present in extracted key-value pairs)."""
    try:
        # Match common date formats (DD-MM-YYYY, MM/DD/YYYY, YYYY-MM-DD)
        match = re.search(r"(\d{1,2}[-/]\w{3,9}[-/]\d{4}|\d{4}[-/]\d{2}[-/]\d{2})", dob_string)
        if match:
            dob = match.group(0)
            dob_date = datetime.strptime(dob, "%d-%b-%Y")  # Example format: 01-Jan-1980
            today = datetime.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
            return age
    except Exception:
        return None
    return None

# Streamlit UI
st.title("📄 AI-Powered Form Parser")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF, Text, or Image File", type=["pdf", "txt", "png", "jpg"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        file_path = temp_file.name

    # Extract text from uploaded file
    extracted_text = None
    if uploaded_file.type == "application/pdf":
        extracted_text = extract_text_from_pdf(file_path)
        if not extracted_text:  # If no text, process as scanned image
            extracted_text = extract_text_from_image(file_path)
    elif uploaded_file.type == "text/plain":
        extracted_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type in ["image/png", "image/jpeg"]:
        extracted_text = extract_text_from_image(file_path)

    if extracted_text:
        # Extract key-value pairs
        extracted_data = extract_all_key_value_pairs(extracted_text)

        # Auto-calculate age if "Date of Birth" is found
        for key, value in extracted_data.items():
            if "Date of Birth" in key or "DOB" in key:
                age = calculate_age(value)
                if age:
                    extracted_data["Calculated Age"] = age

        # Layout: Two columns
        col1, col2 = st.columns(2)

        with col1:
            st.write("### Uploaded File Contents")
            st.text_area("Full Document Text", extracted_text, height=400)

        with col2:
            st.write("### Extracted Key-Value Pairs")

            # Display as key-value pairs
            for key, value in extracted_data.items():
                st.write(f"**{key}**: {value}")

            # Display JSON format
            st.write("### Extracted Data in JSON Format")
            st.json(extracted_data)
    else:
        st.error("Could not extract text from the document. Please upload a valid file.")
