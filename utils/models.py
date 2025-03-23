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
    task for T5 model: **\"translation\"** \n
    task for BART and DistilBART models: **\"summarization\"** \n
    """

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
        """Load a model using the raw API. \n
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
        """Summarize text using the specified tokenizer and model. \n"""
        try:
            # Tokenize the input text
            p.info("Tokenizing input text...")
            inputs = tokenizer(
                text, 
                return_tensors="pt", 
                max_length=1024, 
                truncation=True
            )

            # Generate summary
            p.info("Generating summary...")
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
            p.success("Text summarized successfully.\n")
            return summary
        except Exception as e:
            p.error(f"Error during summarization: {str(e)}")
