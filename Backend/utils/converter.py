import subprocess
import tempfile
import os
import shutil
import platform


def _find_soffice() -> str:
    """
    Locate LibreOffice soffice executable on Windows or Linux.
    """
    # First try PATH (works on Linux & Windows if configured)
    soffice = shutil.which("soffice")
    if soffice:
        return soffice

    # Windows default fallback
    if platform.system() == "Windows":
        win_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
        for path in win_paths:
            if os.path.isfile(path):
                return path

    raise FileNotFoundError(
        "LibreOffice (soffice) not found. Ensure LibreOffice is installed "
        "and 'soffice' is available in PATH."
    )


def convert_word_to_pdf_bytes(input_path: str) -> bytes:
    """
    Converts DOC/DOCX to PDF using LibreOffice.
    Returns PDF as bytes (in-memory).
    Works on Windows and Linux.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    soffice_path = _find_soffice()

    with tempfile.TemporaryDirectory() as tmpdir:
        command = [
            soffice_path,
            "--headless",
            "--nologo",
            "--nolockcheck",
            "--nodefault",
            "--convert-to",
            "pdf",
            input_path,
            "--outdir",
            tmpdir,
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"LibreOffice conversion failed:\n{result.stderr}"
            )

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        pdf_path = os.path.join(tmpdir, f"{base_name}.pdf")

        if not os.path.isfile(pdf_path):
            raise RuntimeError("PDF conversion failed; output file not found.")

        with open(pdf_path, "rb") as f:
            return f.read()
