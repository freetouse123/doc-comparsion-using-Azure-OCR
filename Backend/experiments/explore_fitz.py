sop_file_path = r"C:\Users\SumeetMaheshwari\Downloads\Output 1.pdf"

with open(sop_file_path, "rb") as f:
    pdf_bytes = f.read()

import fitz  # PyMuPDF

def extract_html_from_pdf_bytes(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    html_pages = []
    for page in doc:
        html = page.get_text("html")
        html_pages.append(html)

    doc.close()
    return "\n".join(html_pages)


def extract_blocks_from_pdf_bytes(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    all_pages = []
    for page in doc:
        blocks = page.get_text("blocks")
        all_pages.append(blocks)

    doc.close()
    return all_pages


def extract_json_layout(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages = []
    for page in doc:
        pages.append(page.get_text("json"))

    doc.close()
    return pages


if __name__=="__main__":
    data = extract_json_layout(pdf_bytes= pdf_bytes)
    print(data[0])

