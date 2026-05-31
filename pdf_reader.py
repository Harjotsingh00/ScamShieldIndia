from pypdf import PdfReader


def extract_pdf_text(pdf_file):
    """
    Extract text from uploaded PDF.
    Returns a string.
    """

    try:

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    except Exception as e:

        return f"PDF Extraction Error: {str(e)}"