import os
import json
from utils.ansi_helpers import Printer

# Load supported file extensions config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "configs", "supported_files.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    SUPPORTED_FILES_MAP: dict[str, str] = json.load(f)

def is_supported_file_extension(p: Printer, path: str) -> tuple[bool, str]:
    """
    Verify extension is compatible with the projects requirements. \n
    ***
    Returns:
        tuple:
            - bool: True if supported, False if not
            - str: the extension of the file.
    """
    
    ext: str = os.path.splitext(path)[1].lower() 
    
    if ext not in SUPPORTED_FILES_MAP:
        p.warning(f"Supported file types are: {', '.join(SUPPORTED_FILES_MAP)}")
        p.error(f"Input File type not supported: '{ext}'")
        # no return needed since error calls sys.exit(1)
    
    return True, ext

def verify_file_path(p: Printer, file_path: str) -> str:
    """
    Check if the file exists and return its (corrected/normalized) path. \n
    This function uses methods from **os** module that are **cross-platform compatible**.\n
    ***
    Returns:
        str: 
            - The input path if the file at that directory exists.
    """
    
    try:
        p.info(f"Verifying input file path: {file_path}")
        
        input_path = os.path.normpath(file_path)
        
        # If normalizing alone does not work, try the absolute path
        if not os.path.isfile(input_path):
            alt_path = os.path.join(os.getcwd(), input_path.lstrip(r"\/"))
            if os.path.isfile(alt_path):
                p.success(f"File found: {alt_path}\n")
                if is_supported_file_extension(p, alt_path):
                    return alt_path
            else:
                p.error(f"File not found: {file_path}")
        
        # Here the normalized path worked, meaning file exists
        else:
            p.success(f"File found: {file_path}\n")
            if is_supported_file_extension(p, input_path):
                return input_path
    except Exception as e:
        p.error(f"Error locating file: {str(e)}")

def verify_output_path(p: Printer, file_path: str) -> str:
    """
    Check if the output directory exists and return its (corrected/normalized) path. \n
    This function uses methods from **os** module that are **cross-platform compatible**.\n
    ***
    Returns:
        str: 
            - The output path if it's a valid directory.
    """
    
    try:
        p.info(f"Verifying output path: {file_path}")
        
        output_path = os.path.normpath(file_path)
        output_directory = os.path.dirname(output_path)
        
        # If normalizing alone does not work, try the absolute path
        if not os.path.isdir(output_directory):
            alt_path = os.path.join(os.getcwd(), output_path.lstrip(r"\/"))
            alt_directory = os.path.dirname(alt_path)
            if os.path.isdir(alt_directory):
                p.success(f"Output directory found: {os.path.dirname(alt_path)}\n")
                supported, ext = is_supported_file_extension(p, alt_path)
                if supported:
                    return alt_path
            else:
                p.error(f"Output directory not found: {output_directory} | {alt_directory}")
        
        # Here the normalized path worked, meaning directory exists
        else:
            p.success(f"Output directory verified: {output_directory}\n")
            if is_supported_file_extension(p, output_path):
                return output_path

    except Exception as e:
        p.error(f"Error verifying output path: {str(e)}")

def read_file(p: Printer, file_path: str) -> str:
    """
    Read the content of the file and return as string. \n
    ***
    Returns:
        str: 
            - The content of the file as a string.
    """
    
    try:
        p.info("Reading file...")
        
        # GET FILE EXTENSION (we already verified it is supported earlier -> verify_file_path -> is_supported_file_extension)
        ext: str = os.path.splitext(file_path)[1].lower() 

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

        # DEFENSIVE FALLBACK (maybe someone manually bypass the path verification check)
        else:
            p.error(f"Unsupported file type: '{ext}'")
        
        # EMPTY FILES
        if not text.strip():
            p.error(f"File is empty or contains no readable text: {file_path}")

        p.success("File read successfully\n")
        return text
    except ImportError as e:
        p.error(f"Required library not found: {str(e)}")
    except Exception as e:
        p.error(f"Error reading file: {str(e)}")

def write_file(p: Printer, file_path: str, content: str) -> None:
    """
    Write the content of the file and return as string. \n
    ***
    Returns:
        None: 
    """
    
    try:
        p.info("Writing file...")
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        
        p.success(f"SummarAIzation complete. Output saved to {file_path}\n")
    except Exception as e:
        p.error(f"Error writing file: {str(e)}")