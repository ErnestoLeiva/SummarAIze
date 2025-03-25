import argparse
import json
import os
from utils.version_helper import get_version
from utils.ascii_art import ASCII_art as ascii

# Load model_registry.json at runtime to dynamically get valid choices (from model_registry.json)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "configs", "model_registry.json")
with open(MODEL_REGISTRY_PATH, "r", encoding="utf-8") as f:
    MODEL_CHOICES = list(json.load(f).keys())

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [-h, --help], [-v, --version], (-s, --summarize <file_path>), [-o, --output <file_path>], [-m, --model <model_name> | default: BART], [-na, --no-ansi], [-gm, --gui-mode]',
        description= ascii.splash_title,
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=45)
    )
    
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{get_version()}", help="Show version information")
    parser.add_argument("-s", "--summarize", metavar="<file_path>", type=str, required=True, help="File to summarize [*required]")
    parser.add_argument("-o", "--output", metavar="<file_path>", type=str, required=False, help="Path to store summary (optional)")
    parser.add_argument("-m", "--model", metavar="<model_name>", type=model_key_type, choices=MODEL_CHOICES, required=False, default="BART", help="Specify which model to use (optional)")
    parser.add_argument("-na", "--no-ansi", action="store_true", required=False, help="Disable ANSI escape codes in output (optional)")
    parser.add_argument("-gm", "--gui-mode", action="store_true", required=False, help="Enable gui mode for controlled output (optional)")
    
    return parser.parse_args()

def model_key_type(s: str) -> str:
    """Normalize model key to uppercase and return. *(removes case-sensitivity)*"""
    return s.upper()
