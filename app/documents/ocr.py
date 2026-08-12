import os

import pytesseract
from pdf2image import convert_from_path
from PIL import Image


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    text = ""

    if ext in [".png", ".jpg", ".jpeg"]:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    elif ext == ".pdf":
        pages = convert_from_path(file_path)

        for page in pages:
            text += pytesseract.image_to_string(page)

    return text.strip()