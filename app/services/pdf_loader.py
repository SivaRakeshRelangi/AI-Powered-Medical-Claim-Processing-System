from pdf2image import convert_from_bytes
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def load_pdf_pages(file):
    images = convert_from_bytes(file.read())

    pages = []

    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)

        pages.append({
            "page_num": i + 1,
            "text": text
        })

    print(pages[:2])  # debug
    return pages