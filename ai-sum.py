import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Workaround for a known issue with TensorFlow and OneDNN optimizations

from transformers import AutoModelForSeq2SeqLM, AutoModelForCausalLM, AutoTokenizer, pipeline
import sys
import argparse


splash_title = """\
╔══════════════════════════════════════════════════════════════════════════════════╗
║███████╗██╗   ██╗███╗   ███╗███╗   ███╗ █████╗ ██████╗  █████╗ ██╗███████╗███████╗║
║██╔════╝██║   ██║████╗ ████║████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║╚══███╔╝██╔════╝║
║███████╗██║   ██║██╔████╔██║██╔████╔██║███████║██████╔╝███████║██║  ███╔╝ █████╗  ║
║╚════██║██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██╔══██╗██╔══██║██║ ███╔╝  ██╔══╝  ║
║███████║╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██║██║███████╗███████╗║
║╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝║
╟────────────────────────────────────────────────────────────────┐ est. 2025 ┆ FIU ║
║        Summarize text using AI.                                └─────────────────╢
╚══════════════════════════════════════════════════════════════════════════════════╝\
"""


def main():
    parser = argparse.ArgumentParser(
        usage='%(prog)s [-h, --help] --summarize <input_text> [--no-ansi]',
        description= splash_title,
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=45)
    )
    
    parser.add_argument("-s", "--summarize", metavar="<input_text>", type=str, required=True, help="Text to summarize [*required]")
    parser.add_argument("--no-ansi", action="store_true", help="Disable ANSI escape codes in output (optional)")
    args = parser.parse_args()

    # ANSI escape codes
    RED = "\033[91m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    # ANSI color coded symbols
    ERROR= f"{RED}✗ {RESET}"
    INFO= f"{CYAN}▶▶ {RESET}"
    SUCCESS= f"{GREEN}√ {RESET}"

    # just sets all the variables that use ANSI escape codes to empty strings if --no-ansi is passed
    if args.no_ansi:
        RED = GREEN = CYAN = RESET = ERROR = INFO = SUCCESS = ""

    if not args.no_ansi:
        print(f"{SUCCESS}SummarAIzing text...\n")

    # Load the model and tokenizer
    try:
        model_name = "facebook/bart-large-cnn"
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

    except Exception as e:
        print(f"{ERROR}Error loading model and tokenizer: {str(e)}")
        sys.exit(1)

    # Input text to summarize
    text = args.summarize


    try:
        # Tokenize the input text
        inputs = tokenizer(
            text, 
            return_tensors="pt", 
            max_length=1024, 
            truncation=True
        )

        # Generate summary
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )

        # Decode the summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        print(f"{ERROR}Error summarizing text: {str(e)}")
        sys.exit(1)

    if not args.no_ansi:
        print(f"{INFO}SummarAIzation: {summary}")
    else:
        print(f"{summary}")
    sys.exit(0)


if __name__ == "__main__":
    main()
