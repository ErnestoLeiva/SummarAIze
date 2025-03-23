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
        p.info(f"Reading file")
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            if not text.strip():
                p.error(f"File is empty: {file_path}")
            p.success(f"File read successfully\n")
            return text
    except Exception as e:
        p.error(f"Error reading file: {str(e)}")
