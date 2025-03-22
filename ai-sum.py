import sys
import argparse
from custom_classes.ANSI_helpers import Symbols as symb
from custom_classes.ASCII_art import ASCII_art as ascii
from custom_classes.Timer import Timer as timer

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [-h, --help], [-s, --summarize <file_path>], [-o, --output <file_path>], [-m, --model <model_name> | default: BART], [-na, --no-ansi], [-gm, --gui-mode]',
        description= ascii.splash_title,
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=45)
    )
    
    parser.add_argument("-s", "--summarize", metavar="<file_path>", type=str, required=True, help="File to summarize [*required]")
    parser.add_argument("-o", "--output", metavar="<file_path>", type=str, required=False, help="Path to store summary (optional)")
    parser.add_argument("-m", "--model", metavar="<model_name>", type=str, required=False, default="BART", help="Specify which model to use (optional)")
    parser.add_argument("-na", "--no-ansi", action="store_true", required=False, help="Disable ANSI escape codes in output (optional)")
    parser.add_argument("-gm", "--gui-mode", action="store_true", required=False, help="Enable gui mode for controlled output (optional)")
    return parser.parse_args()

def main():
    """Main function to summarize text."""
    
    # parse args and store in args variable
    args = parse_args()


    # check if --no-ansi is passed and if so call static disabel method in ansi helper class
    if args.no_ansi:
        symb.disable()
    else:
        print(f"{symb.SUCCESS}SummarAIzing...\n")


    from custom_classes.Models import Models # i start this import here because it helps with improve performance for help screen flag [-h, --help]
    # check if manual model is passed and if so check if it is valid
    if args.model:
        model_key = args.model.upper()
        if model_key not in Models.MODEL_MAP:
            print(f'{symb.ERROR}Invalid model name. Available models: {", ".join(Models.MODEL_MAP.keys())}')
            sys.exit(1)
        selected_model = Models.MODEL_MAP[model_key]
    else:
        selected_model = Models.MODEL_MAP["BART"]


    # Load the model and tokenizer
    try:
        tokenizer, model = Models.use_raw(Models.MODEL_MAP[args.model.upper()])
    except Exception as e:
        print(f"{symb.ERROR}Error loading model and tokenizer: {str(e)}")
        sys.exit(1)


    # Input text to summarize ############### !!!!!!!!!!!!!! CHANGE TO FILE INPUT !!!!!!!!!!!!! ################
    text = args.summarize

    # Start the text summarization process and time it
    with timer("Text Summarization", args.gui_mode, args.no_ansi):
        try:
            summary = Models.summarAIze(tokenizer, model, text)
        except Exception as e:
            print(f"{symb.ERROR}Error summarizing text: {str(e)}")
            sys.exit(1)

    # print the results
    if not args.no_ansi:
        print(f"{symb.INFO}SummarAIzation: {summary}")
    else:
        print(f"{summary}")
    sys.exit(0)


if __name__ == "__main__":
    main()
