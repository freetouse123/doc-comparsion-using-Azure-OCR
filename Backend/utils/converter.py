import subprocess
import tempfile
import os


def convert_word_to_pdf_bytes(input_path):
    """
    Converts DOC/DOCX to PDF using LibreOffice.
    Returns PDF as bytes (in-memory).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Run LibreOffice conversion
        command = [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            input_path,
            "--outdir",
            tmpdir
        ]

        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # LibreOffice uses same base filename
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        pdf_path = os.path.join(tmpdir, f"{base_name}.pdf")

        # Read PDF into memory
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        return pdf_bytes
