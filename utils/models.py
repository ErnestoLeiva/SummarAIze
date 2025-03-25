import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Workaround for a known issue with TensorFlow and OneDNN optimizations
from utils.ansi_helpers import Printer

# workaround for NameError exception on runtime.
# happens with type checking for summarAIze function since im defining the types for the parameters before its actually imported
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Models:
    """Handles loading models in pipeline or raw format.\n
    **Models**: \n
    - *BART*: facebook/bart-large-cnn \n
    - *DistilBART*: sshleifer/distilbart-cnn-12-6 \n
    - *T5*: google-t5/t5-small \n
    """

    MODEL_MAP = {
        "BART": "facebook/bart-large-cnn",
        "DISTILBART": "sshleifer/distilbart-cnn-12-6",
        "T5": "google-t5/t5-small"
    }
    """
    **Pipeline usage:**
    - task for T5 model: **\"translation\"** \n
    - task for BART and DistilBART models: **\"summarization\"** \n
    """

    MODEL_TOKEN_LIMIT_MAP = {
            "BART": 1024,
            "DISTILBART": 1024,
            "T5": 512
        }
    """Each model has its own token limits, typically 1,024 tokens though."""

    ### GLOBALS
    # "Dummy" max length to avoid HuggingFace/Transformer warnings
    TOKENIZER_DUMMY_MAX = 99999

    # Summarization settings:
    DEFAULT_SUMMARY_RATIO = 0.3        # 30% of the input length
    DEFAULT_MIN_TOKENS = 80           # lower clamp -> at least 80 tokens
    DEFAULT_OVERLAP_RATIO = 0.1             # 10% overlap ratio for chunked summarization
    DEFAULT_LENGTH_PENALTY_THRESHOLD = 800  # by token count: if input < 800 => length_penalty=1.0; else 2.0


    @staticmethod
    def use_pipeline(p: Printer, model_task: str = "summarization", model_name: str = MODEL_MAP["BART"]) -> object:
        """Load a model using the pipeline API. \n
        Returns:
            *object*: A *pipeline* object for the specified task and model.
        """
        p.info("Loading pipeline...")
        from transformers import pipeline
        try:
            pipe = pipeline(
                task=model_task, 
                model=model_name, 
                tokenizer=model_name
                )
            p.success("Pipeline loaded successfully.\n")
            return pipe
        except Exception as e:
            p.error(f"Error loading pipeline: {str(e)}")
    
    @staticmethod
    def use_raw(p: Printer, model_name: str = MODEL_MAP["BART"]) -> tuple:
        """
        Load a model using the raw API. \n
        (AutoTokenizer and AutoModelForSeq2SeqLM) \n
        Args:
            printer (Printer): The printer object for logging.
            model_name (str): The name of the model to load.

        Returns:
            *tuple*: A tuple containing the tokenizer and model objects.
        """
        try:
            p.info("Loading model and tokenizer...")
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            p.success("Model and tokenizer loaded successfully.\n")
            return (
                tokenizer, 
                model
            )
        except Exception as e:
            p.error(f"Error loading model/tokenizer: {str(e)}")
    
    @staticmethod
    def summarAIze_raw(p: Printer, tokenizer: "AutoTokenizer", model: "AutoModelForSeq2SeqLM", text: str) -> str:
        """
        Summarize text using the specified tokenizer and model. (Direct Model Load) \n
        Dynamically adjusts generation parameters based on input length. \n
        Breaks text into chunks if it exceeds the model's maximum token limit. \n
        Args:
            printer (Printer): The printer object for logging.
            tokenizer (AutoTokenizer): The tokenizer for the model.
            model (AutoModelForSeq2SeqLM): The model for summarization.
            text (str): The input text to summarize.
        Returns:
            str: The summarized text.
        """
        
        try:
            # Consider model's token limit
            model_name, token_limit = Models.get_token_limit(p, model)
            
            # Tokenize to get input length only (avoiding warnings using global dummy variable)
            tokens = tokenizer.encode(
                text, 
                max_length=Models.TOKENIZER_DUMMY_MAX,
                truncation=False
                )
            input_length = len(tokens)
            
            ### [CHUNKING CONDITION] If the input is too long, use chunking method
            if input_length > token_limit:
                p.info(f"Input exceeds token limit for {model_name} model ({input_length} > {token_limit}), using chunked summarization...")
                return Models.summarAIze_raw_chunked(p, tokenizer, model, text, token_limit)

            # Tokenize the input text
            p.info("Tokenizing input text...")
            inputs = tokenizer(
                text, 
                return_tensors="pt", 
                max_length=token_limit, 
                truncation=True
            )

            # Handle input token length and dynamically adjust generation parameters
            input_length = inputs["input_ids"].shape[1]
            summary_ratio = Models.DEFAULT_SUMMARY_RATIO # currently set to 30%(0.3) of the input length
            target_length = int(input_length * summary_ratio) # Prevent extreme short or extreme long
            target_length = max(Models.DEFAULT_MIN_TOKENS, min(target_length, token_limit)) # atleast 80 tokens, or if target_length is greater than 80, but less than [token_limit] we use that. otherwise its capped at [token_limit] tokens.
            max_length = target_length
            min_length = int(0.7 * max_length)
            length_penalty = 1.0 if input_length < Models.DEFAULT_LENGTH_PENALTY_THRESHOLD else 2.0 # doing this helps with not over summarizing shorts, and under summarizing longs..

            # Generate summary
            p.info("Generating summary...")
            summary_ids = model.generate(
                inputs["input_ids"],
                max_length=max_length,
                min_length=min_length,
                length_penalty=length_penalty,  
                num_beams=4,
                early_stopping=True,
                do_sample=False
            )

            # Decode the summary
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            p.success("Text summarized successfully.\n")
            return summary
        except Exception as e:
            p.error(f"Error during summarization: {str(e)}")

    @staticmethod
    def summarAIze_raw_chunked(p: Printer, tokenizer: "AutoTokenizer", model: "AutoModelForSeq2SeqLM", text: str, token_limit: int) -> str:
        """
        Summarize the chunks then return concatenated summaries. \n
        Args:
            printer (Printer): The printer object for logging.
            tokenizer (AutoTokenizer): The tokenizer for the model.
            model (AutoModelForSeq2SeqLM): The model for summarization.
            text (str): The input text to summarize.
            token_limit (int): The models token limit
        Returns:
            str:
            The concatenated summarized text chunks.
        """
        try:
            chunks = Models.split_into_chunks(p, text, tokenizer, max_tokens=token_limit)
            summaries = []
            for i, chunk in enumerate(chunks):
                p.info(f"Tokenizing & Summarizing chunk {i+1}/{len(chunks)}...")
                
                # Tokenize chunk text
                inputs = tokenizer(
                    chunk,
                    return_tensors="pt",
                    max_length=token_limit,
                    truncation=True
                )

                # Handle input(chunk) token length and dynamically adjust generation parameters
                chunk_length = inputs["input_ids"].shape[1]
                summary_ratio = Models.DEFAULT_SUMMARY_RATIO  # 30% of the chunk 
                target_length = int(chunk_length * summary_ratio) # Prevent extreme short or extreme long
                target_length = max(Models.DEFAULT_MIN_TOKENS, min(target_length, token_limit)) # atleast 80 tokens, or if target_length is greater than 80, but less than [token_limit] we use that. otherwise its capped at [token_limit] tokens.
                max_length = target_length
                min_length = int(0.7 * max_length)
                length_penalty = 1.0 if chunk_length < Models.DEFAULT_LENGTH_PENALTY_THRESHOLD else 2.0 # doing this helps with not over summarizing shorts, and under summarizing longs..

                summary_ids = model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=length_penalty,
                    num_beams=4,
                    early_stopping=True,
                    do_sample=False
                )
                summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                summaries.append(summary)

            final_summary = "\n\n".join(summaries)
            p.success(f"Text summarized successfully. (Chunk count: {len(chunks)})\n")
            return final_summary
        except Exception as e:
            p.error(f"Error during chunked summarization: {str(e)}")

    @staticmethod
    def split_into_chunks(p: Printer, text: str, tokenizer: "AutoTokenizer", max_tokens: int = 1024) -> list[str]:
        """
        Splits text into overlapping chunks. \n
        Useful for long texts that exceed the model's maximum token limit. \n
        Args:
            printer (Printer): The printer object for logging.
            text (str): The input text to split.
            tokenizer_path (str): Path to the tokenizer model.
            max_tokens (int): Maximum number of tokens per chunk.
            overlap (int): Number of overlapping tokens between chunks.
        Returns:
            list[str]: A list of text chunks.
        """
        try:
            p.info("Tokenizing and splitting text into chunks...")
            
            tokens = tokenizer.encode(
                text, 
                max_length=Models.TOKENIZER_DUMMY_MAX, # Dummy limit so that transformers warning does not appear in output, provided token_limit (sequence) is greater than model limit
                truncation=False
                )

            overlap = int(max_tokens * Models.DEFAULT_OVERLAP_RATIO) # will do a %10 overlap of chunk size -> starts at 90% index of previous index for next index
            stride = max_tokens - overlap
            chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), stride)]
            decoded_chunks = [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]

            p.success(f"Text split into {len(decoded_chunks)} chunks.\n")
            return decoded_chunks
        except Exception as e:
            p.error(f"Error splitting text into chunks: {str(e)}")

    @staticmethod
    def get_token_limit(p: Printer, model: "AutoModelForSeq2SeqLM") -> tuple[str, int]:
        """
        Return the max input token limit based on the model. \n
        Args:
            p (Printer): The printer object for logging.
            model_name (str): The name of the model.
        Returns:
            int: The maximum input token limit.
        """
        
        # Extract model name from model object
        try:
            model_path = model.name_or_path.lower()
            model_name = None

            for key, path in Models.MODEL_MAP.items():
                if path.lower() in model_path:
                    model_name = key.upper()
                    break
        except Exception as e:
            p.error(f"Failed to detect model key from model object: {str(e)}")

        # Determine token limit from extracted model name
        if model_name in Models.MODEL_TOKEN_LIMIT_MAP:
            return model_name, Models.MODEL_TOKEN_LIMIT_MAP[model_name] # retruns the value from limit map
        else:
            p.error("Unable to determine model tokenization limit: Invalid/Unknown model")# fallback if for some reason its not in model token limit map
