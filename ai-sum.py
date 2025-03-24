import sys
from utils.ansi_helpers import Printer
from utils.timer import Timer as timer
from utils.arg_parser import parse_args
from utils.file_handling import verify_file_path, verify_output_path, read_file, write_file
from utils.version_helper import get_version
from utils.models import Models


def main() -> None:
    """Main function to summarize text."""
    
    ### Parse args and store in args variable
    args = parse_args()

    ### Initliaze the printer object from ansi_helpers
    p: Printer = Printer(no_ansi=args.no_ansi, gui_mode=args.gui_mode)

    ### Alert the user that the script is starting 
    p.success(f"SummarAIzing...\tv{get_version()}\n")

    ### Check if input file exists and if output directory exists, if not then print error message and exit
    args.summarize = verify_file_path(p, args.summarize)
    if args.output:
        args.output = verify_output_path(p, args.output)

    ### Read it and store it in text variable
    text: (str | None) = read_file(p, args.summarize)

    ### Load the model and tokenizer
    selected_model = Models.MODEL_MAP[args.model.upper()]
    tokenizer, model = Models.use_raw(p, selected_model)

    ### Start the text summarization process and time it
    with timer("Text Summarization", args.gui_mode, args.no_ansi):
        summary = Models.summarAIze_raw(p, tokenizer, model, text)

    ### print the results
    if not args.gui_mode and not args.output: # Standard CLI mode
        p.result(f"SummarAIzation: {summary}")
    
    elif args.output:   # Output flag is set
        write_file(p, args.output, summary)
    
    else:   # GUI mode is set or other cases i guess ------------------------------ CAN MODIFY THIS LATER DURING DEVELOPMENT OF GUI -------------------------------------------------!!!!!!!!!!!!!!!!!!!!!!
        print(f"{summary}")
    sys.exit(0)


if __name__ == "__main__":
    main()