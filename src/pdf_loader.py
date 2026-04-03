import fitz
from typing import List, Dict

def load_pdf(file) -> List[Dict]:
    doc = fitz.open(stream=file.read(), filetype="pdf")

    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        if len(text.strip()) < 50:
            continue

        pages.append({
            "page": page_num + 1,
            "text": text.strip()
        })

    doc.close()
    print(f"Loaded {len(pages)} pages of text from PDF")
    return pages