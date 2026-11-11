import os
import io
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pdfplumber
import docx

# Explicitly set the path to the Tesseract executable
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def parse_image(file_bytes: bytes) -> str:
    """Extracts text from an image file using enhanced Tesseract OCR."""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        
        # 1. Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Try raw OCR first
        text = pytesseract.image_to_string(image)
        if text and len(text.strip()) > 10:
            return text.strip()
            
        # 2. If sparse, try grayscale + contrast enhancement
        gray = image.convert('L')
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(1.8)
        text_enhanced = pytesseract.image_to_string(enhanced)
        if text_enhanced and len(text_enhanced.strip()) > len(text.strip()):
            return text_enhanced.strip()
            
        return text.strip()
    except Exception as e:
        print(f"Error parsing image with Tesseract: {e}")
        return ""

def parse_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages_to_read = min(15, len(pdf.pages))
            for i in range(pages_to_read):
                page_text = pdf.pages[i].extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

def parse_docx(file_bytes: bytes) -> str:
    """Extracts text from a Word Document."""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except Exception as e:
        print(f"Error parsing Word Document: {e}")
        return ""

def parse_document(file_bytes: bytes, filename: str) -> str:
    """Routes the file to the correct parser based on extension."""
    ext = filename.lower().split('.')[-1]
    
    if ext in ['png', 'jpg', 'jpeg', 'bmp', 'webp', 'tiff']:
        return parse_image(file_bytes)
    elif ext == 'pdf':
        return parse_pdf(file_bytes)
    elif ext in ['doc', 'docx']:
        return parse_docx(file_bytes)
    else:
        # Fallback for plain text / markdown / code
        try:
            return file_bytes.decode('utf-8', errors='ignore').strip()
        except Exception:
            return ""
