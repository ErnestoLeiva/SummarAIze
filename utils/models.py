import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Workaround for a known issue with TensorFlow and OneDNN optimizations
from utils.ansi_helpers import Printer
from typing import TYPE_CHECKING # used for NameError runtime exception 
if TYPE_CHECKING:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Models:
    """Handles loading models in pipeline or raw format.\n
    ***
    **Model Support**:
    - BART: facebook/bart-large-cnn
    - DistilBART: sshleifer/distilbart-cnn-12-6
    - T5: google-t5/t5-small
    
    **Model Data (from model_registry.json)**:
    - hf_path: Hugging Face model identifier (e.g. "facebook/bart-large-cnn")
    - token_limit: Max input token length supported by each model (e.g. 1024 for BART)
    - task: 
        - "summarization" for BART and DistilBART
        - "translation" for T5

    **Configurable Keys (from summarization.json)**:
    - TOKENIZER_DUMMY_MAX: Dummy max to suppress tokenizer warnings
    - DEFAULT_SUMMARY_RATIO: Target summary length as % of input
    - DEFAULT_MIN_TOKENS: Minimum tokens allowed for a summary
    - DEFAULT_OVERLAP_RATIO: Chunk overlap % (for long input splitting)
    - DEFAULT_LENGTH_PENALTY_THRESHOLD: Controls when length_penalty becomes 2.0
    - DEFAULT_DO_SAMPLE: Enable sampling mode
    - DEFAULT_NUM_BEAMS: Number of beams for beam search
    - DEFAULT_EARLY_STOP: Whether to stop early during beam decoding
    - DEFAULT_TOP_K: Top-k sampling value (used only if sampling)
    - DEFAULT_TOP_P: Top-p (nucleus) sampling value
    - DEFAULT_TEMPERATURE: Sampling temperature (optional)
    """
    
    # Absolute PATH
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # config setup -> handles model behavior with parameters 
    CONFIG_PATH = os.path.join(PROJECT_ROOT, "configs", "summarization.json")
    CONFIG = {}

    # model setup -> handles model registry: what models are available, their paths, and their token limits
    MODEL_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "configs", "model_registry.json")
    MODEL_REGISTRY = {}

    @classmethod
    def load_config(cls) -> None:
        """Load summarization configuration and model registry from JSON files."""
        import json
        with open(cls.CONFIG_PATH, "r", encoding="utf-8") as f:
            cls.CONFIG = json.load(f)
        with open(cls.MODEL_REGISTRY_PATH, "r", encoding="utf-8") as f:
            cls.MODEL_REGISTRY = json.load(f)

    @staticmethod
    def use_pipeline(p: Printer, model_key: str = "BART") -> object:
        """
        Load a model using the pipeline API. \n
        ***
        Returns:
            *object*: A *pipeline* object for the specified task and model.
        """
        p.info("Loading pipeline...")
        from transformers import pipeline
        try:
            model_task = Models.MODEL_REGISTRY[model_key]["task"]
            hf_path = Models.MODEL_REGISTRY[model_key]["hf_path"]

            pipe = pipeline(
                task=model_task, 
                model=hf_path, 
                tokenizer=hf_path
                )
            p.success("Pipeline loaded successfully.\n")
            return pipe
        except Exception as e:
            p.error(f"Error loading pipeline: {str(e)}")
    
    @staticmethod
    def use_raw(p: Printer, model_key: str = "BART") -> tuple:
        """
        Load a model using the raw API. \n
        *(AutoTokenizer and AutoModelForSeq2SeqLM)* \n
        ***
        Args:
            printer (Printer): The printer object for logging.
            model_key (str): The name of the model to load.

        Returns:
            *tuple*: A tuple containing the tokenizer and model objects.
        """
        try:
            p.info("Loading model and tokenizer...")
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            hf_path = Models.MODEL_REGISTRY[model_key]["hf_path"]
            
            tokenizer = AutoTokenizer.from_pretrained(hf_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(hf_path)
            
            p.success("Model and tokenizer loaded successfully.")
            return (
                tokenizer, 
                model
            )
        except Exception as e:
            p.error(f"Error loading model/tokenizer: {str(e)}")
    
    @staticmethod
    def summarAIze_raw(p: Printer, tokenizer: "AutoTokenizer", model: "AutoModelForSeq2SeqLM", text: str) -> str:
        """
        Summarize text using the specified tokenizer and model. *(Direct Model Load)* \n
        Dynamically adjusts generation parameters based on input length. \n
        Breaks text into chunks if it exceeds the model's maximum token limit. \n
        ***
        Args:
            printer (Printer): The printer object for logging.
            tokenizer (AutoTokenizer): The tokenizer for the model.
            model (AutoModelForSeq2SeqLM): The model for summarization.
            text (str): The input text to summarize.
        Returns:
            str: The summarized text.
        """
        
        try:
            cfg = Models.CONFIG
            
            # Consider model's token limit
            model_name, token_limit = Models.get_token_limit(p, model)
            
            # Tokenize to get input length only (avoiding warnings using global dummy variable)
            tokens = tokenizer.encode(
                text, 
                max_length=cfg["TOKENIZER_DUMMY_MAX"],
                truncation=False
                )
            input_length = len(tokens)
            
            ### [CHUNKING CONDITION] If the input is too long, use chunking method
            if input_length > token_limit:
                p.warning(f"Input exceeds token limit for {model_name} model ({input_length} > {token_limit}), using chunked summarization...")
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
            kwargs = Models.get_generation_kwargs(input_length, token_limit)

            # Generate summary
            p.info("Generating summary...")
            summary_ids = model.generate(inputs["input_ids"], **kwargs)

            # Decode the summary
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            p.success("Text summarized successfully.")
            return summary
        except Exception as e:
            p.error(f"Error during summarization: {str(e)}")

    @staticmethod
    def summarAIze_raw_chunked(p: Printer, tokenizer: "AutoTokenizer", model: "AutoModelForSeq2SeqLM", text: str, token_limit: int) -> str:
        """
        Summarize the chunks then return concatenated summaries. \n
        ***
        Args:
            printer (Printer): The printer object for logging.
            tokenizer (AutoTokenizer): The tokenizer for the model.
            model (AutoModelForSeq2SeqLM): The model for summarization.
            text (str): The input text to summarize.
            token_limit (int): The model's token limit
        Returns:
            str: The concatenated summarized text chunks.
        """
        try:
            from concurrent.futures import ThreadPoolExecutor
            from multiprocessing import cpu_count


            decoded_chunks, chunks = Models.split_into_chunks(p, text, tokenizer, token_limit)

            def summarize_chunk(i: int, chunk: str) -> str:
                p.info(f"Summarizing chunk {i + 1}/{len(decoded_chunks)}...")
                inputs = tokenizer(
                    chunk,
                    return_tensors="pt",
                    max_length=token_limit,
                    truncation=True
                )
                chunk_len = inputs["input_ids"].shape[1]
                kwargs = Models.get_generation_kwargs(chunk_len, token_limit)
                summary_ids = model.generate(inputs["input_ids"], **kwargs)
                return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

            with ThreadPoolExecutor(max_workers=min(cpu_count(), len(chunks))) as executor:
                summaries = list(executor.map(lambda i_chunk: summarize_chunk(*i_chunk), enumerate(decoded_chunks)))

            final_summary = "\n\n".join(summaries)
            p.success(f"Text summarized successfully. (Chunk count: {len(summaries)})")
            return final_summary

        except Exception as e:
            p.error(f"Error during chunked summarization: {str(e)}")

    @staticmethod
    def split_into_chunks(p: Printer, text: str, tokenizer: "AutoTokenizer", max_tokens: int = 1024) -> tuple[list[str], list[str]]:
        """
        Splits text into overlapping chunks. \n
        Useful for long texts that exceed the model's maximum token limit. \n
        ***
        Args:
            printer (Printer): The printer object for logging.
            text (str): The input text to split.
            tokenizer_path (str): Path to the tokenizer model.
            max_tokens (int): Maximum number of tokens per chunk.
        Returns:
            tuple:
            - list[str]: A list of decoded text chunks.
            - list[list[int]]: A list of raw token ID chunks
        """
        
        try:
            cfg = Models.CONFIG

            p.info("Tokenizing and splitting text into chunks...")
            
            tokens = tokenizer.encode(
                text, 
                max_length=cfg["TOKENIZER_DUMMY_MAX"], # Dummy limit so that transformers warning does not appear in output, provided token_limit (sequence) is greater than model limit
                truncation=False
                )

            overlap = int(max_tokens * cfg["DEFAULT_OVERLAP_RATIO"]) # will do a %10 overlap of chunk size -> starts at 90% index of previous chunk
            stride = max_tokens - overlap
            chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), stride)]
            decoded_chunks = [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]

            p.success(f"Text split into {len(decoded_chunks)} chunks.")
            return decoded_chunks, chunks
        except Exception as e:
            p.error(f"Error splitting text into chunks: {str(e)}")

    @staticmethod
    def get_token_limit(p: Printer, model: "AutoModelForSeq2SeqLM") -> tuple[str, int]:
        """
        Return the max input token limit based on the model. \n
        ***
        Args:
            p (Printer): The printer object for logging.
            model (AutoModelForSeq2SeqLM): The model object.
        Returns:
            tuple: 
                - str: The model name; Ex: 'BART' \n
                - int: The maximum input token limit for that model.
        """
        
        # Extract model name from model_registry config
        try:
            model_path = model.name_or_path.lower()
            model_key = None

            for key, info in Models.MODEL_REGISTRY.items():
                if info["hf_path"].lower() in model_path:
                    model_key = key
                    break
        except Exception as e:
            p.error(f"Failed to detect model key from model object: {str(e)}")

        if model_key and "token_limit" in Models.MODEL_REGISTRY[model_key]:
            return model_key, Models.MODEL_REGISTRY[model_key]["token_limit"]
        else:
            p.error("Unable to determine model tokenization limit: Invalid/Unknown model")# fallback if for some reason its not in model_registry config

    @staticmethod
    def get_generation_kwargs(input_len: int, token_limit: int) -> dict:
        """
        Generate the summarization parameters based off the **'summarization.json'** config \n
        ***
        Args:
            input_len (int): The token length of the input.
            token_limit (int): The token length limit of the current model.
        Returns:
            dict:
                - TOKENIZER_DUMMY_MAX: Dummy max to suppress tokenizer warnings
                - DEFAULT_SUMMARY_RATIO: Target summary length as % of input
                - DEFAULT_MIN_TOKENS: Minimum tokens allowed for a summary
                - DEFAULT_OVERLAP_RATIO: Chunk overlap % (for long input splitting)
                - DEFAULT_LENGTH_PENALTY_THRESHOLD: Controls when length_penalty becomes 2.0
                - DEFAULT_DO_SAMPLE: Enable sampling mode
                - DEFAULT_NUM_BEAMS: Number of beams for beam search
                - DEFAULT_EARLY_STOP: Whether to stop early during beam decoding
                - DEFAULT_TOP_K: Top-k sampling value (used only if sampling)
                - DEFAULT_TOP_P: Top-p (nucleus) sampling value
                - DEFAULT_TEMPERATURE: Sampling temperature (optional)
        """
        
        cfg = Models.CONFIG
        
        summary_len = int(input_len * cfg["DEFAULT_SUMMARY_RATIO"])
        summary_len = max(cfg["DEFAULT_MIN_TOKENS"], min(summary_len, token_limit))
        penalty = 1.0 if input_len < cfg["DEFAULT_LENGTH_PENALTY_THRESHOLD"] else 2.0

        return {
            "max_length": summary_len,
            "min_length": int(0.7 * summary_len),
            "length_penalty": penalty if not cfg["DEFAULT_DO_SAMPLE"] else None,
            "num_beams": cfg["DEFAULT_NUM_BEAMS"] if not cfg["DEFAULT_DO_SAMPLE"] else 1,
            "early_stopping": cfg["DEFAULT_EARLY_STOP"] if not cfg["DEFAULT_DO_SAMPLE"] else False,
            "do_sample": cfg["DEFAULT_DO_SAMPLE"],
            "top_k": cfg["DEFAULT_TOP_K"] if cfg["DEFAULT_DO_SAMPLE"] else None,
            "top_p": cfg["DEFAULT_TOP_P"] if cfg["DEFAULT_DO_SAMPLE"] else None,
        }
