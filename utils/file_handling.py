import os
from utils.ansi_helpers import Printer

def verify_file_path(p: Printer, file_path: str) -> str:
    """Check if the file exists and return its (corrected/normalized) path. \n
    This function uses methods from **os** module that are **cross-platform compatible**.\n"""
    
    try:
        p.info(f"Verifying file path: {file_path}")
        input_path = os.path.normpath(file_path)
        if not os.path.isfile(input_path):
            alt_path = os.path.join(os.getcwd(), input_path.lstrip(r"\/"))
            if os.path.isfile(alt_path):
                p.success(f"File found: {alt_path}\n")
                return alt_path
            else:
                p.error(f"File not found: {file_path}")
        else:
            p.success(f"File found: {file_path}\n")
            return input_path
    except Exception as e:
        p.error(f"Error locating file: {str(e)}")

def read_file(p: Printer, file_path: str) -> (str | None):
    """Read the content of the file and return as string."""
    
    try:
        p.info("Reading file...")
        ext = os.path.splitext(file_path)[1].lower() # index 1 because 0 is the file name

        # TEXT FILES
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

        # PDF FILES
        elif ext == ".pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])

        # WORD/DOCX FILES
        elif ext == ".docx":
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        # OTHER? - unsupported file types
        else:
            p.error(f"Unsupported file type: {ext}")

        # SUPPORTED BUT EMPTY FILES
        if not text.strip():
            p.error(f"File is empty or contains no readable text: {file_path}")

        p.success("File read successfully\n")
        return text
    except ImportError as e:
        p.error(f"Required library not found: {str(e)}")
    except Exception as e:
        p.error(f"Error reading file: {str(e)}")
