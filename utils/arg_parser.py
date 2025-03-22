import argparse
from utils.version_helper import get_version
from utils.ascii_art import ASCII_art as ascii

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
    parser.add_argument("-m", "--model", metavar="<model_name>", type=str, choices=["BART", "DistilBART", "T5"], required=False, default="BART", help="Specify which model to use (optional)")
    parser.add_argument("-na", "--no-ansi", action="store_true", required=False, help="Disable ANSI escape codes in output (optional)")
    parser.add_argument("-gm", "--gui-mode", action="store_true", required=False, help="Enable gui mode for controlled output (optional)")
    
    return parser.parse_args()