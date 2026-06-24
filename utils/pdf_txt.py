import fitz
from fastapi import UploadFile

async def extract_resume_text(file: UploadFile) -> str:
    pdf_bytes = await file.read()

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text