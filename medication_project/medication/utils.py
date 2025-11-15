import base64
import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def ocr_extract_prescription(text_content=None, base64_image=None):
    """
    Supports:
    - PDF text (text_content)
    - Image OCR (base64_image)
    """

    url = "https://api.groq.com/openai/v1/chat/completions"

    # --------------------------
    # CASE 1: PDF text (NO image)
    # --------------------------
    if base64_image is None:
        user_content = text_content  # must be a simple string
        print("USER CONTENT WITH TEXT:", user_content)

    # --------------------------
    # CASE 2: Image input (Vision)
    # --------------------------
    else:
        user_content = [
            {
                "type": "input_text",
                "text": """
Extract structured prescription data and return ONLY JSON.
                """
            },
            {
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            }
        ]
        #print("USER CONTENT WITH IMAGE:", user_content)

    # --------------------------
    # Build payload properly
    # --------------------------
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You extract prescriptions into clean JSON."
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("OCR RAW RESPONSE:", response.text)

    response.raise_for_status()
    data = response.json()

    # Validate structure
    if "choices" not in data or not data["choices"]:
        raise ValueError(f"OCR API Error: {data}")

    # Return the AI-generated JSON
    print("OCR EXTRACTED JSON1111:", data["choices"][0]["message"]["content"])
    return data["choices"][0]["message"]["content"]
