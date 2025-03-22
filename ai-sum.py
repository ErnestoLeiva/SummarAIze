import sys
import os
from utils.ansi_helpers import Printer
from utils.timer import Timer as timer
from utils.arg_parser import parse_args

def main():
    """Main function to summarize text."""
    
    ### Parse args and store in args variable
    args = parse_args()


    ### Initliaze the printer object from ansi_helpers
    p = Printer(no_ansi=args.no_ansi)


    ### Check if --no-ansi is passed and if so call static disabel method in ansi helper class
    if not args.no_ansi:
        p.success(f"SummarAIzing...\n")


    ### Validate input text file to summarize
    input_path = os.path.normpath(args.summarize)
    if not os.path.isfile(input_path):
        alt_path = os.path.join(os.getcwd(), input_path.lstrip(r"\/"))
        if os.path.isfile(alt_path):
            args.summarize = alt_path
        else:
            p.error(f"File not found: {args.summarize}")
    else:
        args.summarize = input_path
    
    ## If its valid then we will go ahead and yeah just read it
    with open(args.summarize, 'r', encoding='utf-8') as file:
        text = file.read()


    ### Import the Models class from custom_classes.Models
    # i start this import here because it helps with improve performance for help screen flag [-h, --help]
    try:
        from utils.models import Models 
    except ImportError as e:
        p.error(f"Error importing Models class: {str(e)}")
    except Exception as e:
        p.error(f"Unexpected error importing Models class: {str(e)}")
    

    ### Load the model and tokenizer
    try:
        selected_model = Models.MODEL_MAP[args.model.upper()]
        tokenizer, model = Models.use_raw(selected_model)
    except Exception as e:
        p.error(f"Error loading model and tokenizer: {str(e)}")


    ### Start the text summarization process and time it
    with timer("Text Summarization", args.gui_mode, args.no_ansi):
        try:
            summary = Models.summarAIze(tokenizer, model, text)
        except Exception as e:
            p.error(f"Error summarizing text: {str(e)}")

    # print the results
    if not args.gui_mode:
        p.info(f"SummarAIzation: {summary}")
    else:
        print(f"{summary}")
    sys.exit(0)


if __name__ == "__main__":
    main()