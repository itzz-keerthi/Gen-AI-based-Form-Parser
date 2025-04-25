# Gen-AI-based-Form-Parser

## Overview

An intelligent document parser built using **Streamlit** and **Google's Gemini API** that extracts structured key-value pairs from **PDFs**, **images**, and **text files**. This application automatically calculates **age from Date of Birth** fields using NLP and date parsing.

---

![Image](https://github.com/user-attachments/assets/b724a8ed-7be1-45d3-9e04-aa752db8dc59)
![Image](https://github.com/user-attachments/assets/c0e39983-d7b6-420b-b056-ddcc9a6124c3)

## ✨ Features

- ✅ Upload support for `.pdf`, `.txt`, `.png`, `.jpg` files
- 🤖 AI-powered key-value extraction using **Gemini (Gemini-Pro model)**
- 📅 Auto-age calculation from fields like **"DOB"** or **"Date of Birth"**
- 🔍 OCR support for scanned PDFs and images using **Tesseract**
- 🧠 Intelligent fallback: if no text is found in PDFs, processes them as images
- 🧪 Clean JSON format output for integration with APIs or databases
- 🎨 Streamlit UI for instant demo and testing

---

## 🚀 Tech Stack

| Component       | Description                             |
|----------------|-----------------------------------------|
| Streamlit       | Web interface for uploading & display   |
| Google Gemini   | Used for AI-based key-value extraction  |
| pdfplumber      | Text extraction from PDFs               |
| Tesseract OCR   | Text extraction from images             |
| Pillow (PIL)    | Image handling                          |
| Regex & datetime| Age calculation from DOB                |

---

## 📂 Project Structure

```
📁 form-parser-gemini/
│
├── app.py                # Main Streamlit app
├── README.md             # Documentation
├── requirements.txt      # All required dependencies
└── .env                  # (Optional) for storing Gemini API key securely
```

---

## 📥 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/itzz-keerthi/Gen-AI-based-Form-Parser.git
cd form-parser-gemini
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Tesseract-OCR**

- **Windows**: Download from [here](https://github.com/tesseract-ocr/tesseract)
- **Ubuntu**:  
```bash
sudo apt install tesseract-ocr
```

4. **Set Gemini API Key**

- You can **hardcode** it:
```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

- Or use a `.env` file for security:
```env
GEMINI_API_KEY=your_api_key_here
```

Then in `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

5. **Run the Streamlit app**
```bash
streamlit run app.py
```

---

## 📸 Sample Usage

1. Upload a document (`.pdf`, `.txt`, `.jpg`, `.png`)
2. The app extracts all **key-value pairs** intelligently
3. If a **Date of Birth** is found, the **calculated age** is appended
4. JSON view is available for integration or export

---

## 🧠 Example Input and Output

**Uploaded Document Content:**

```
Name: John Doe
Date of Birth: 12-Feb-1990
Gender: Male
Occupation: Engineer
```

**Extracted JSON Output:**
```json
{
  "Name": "John Doe",
  "Date of Birth": "12-Feb-1990",
  "Gender": "Male",
  "Occupation": "Engineer",
  "Calculated Age": 35
}
```

---

## 📦 Dependencies

```txt
streamlit
pdfplumber
pytesseract
Pillow
google-generativeai
python-dotenv
```

---

## 🛡️ Security Notes

- Never hardcode sensitive API keys in production.
- Use `.env` files or secrets management services.

---

## 📈 Future Improvements

- 🔍 Multilingual document parsing
- 🧾 Dynamic field mapping using rules
- 🧠 Advanced layout understanding with LLM Vision
- 📤 Export as Excel/CSV or upload to databases

---
