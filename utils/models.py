import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Workaround for a known issue with TensorFlow and OneDNN optimizations
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
    def use_pipeline(model_task: str = "summarization", model_name: str = MODEL_MAP["BART"]) -> object:
        """Load a model using the pipeline API. \n
        Returns:
            *object*: A *pipeline* object for the specified task and model.
        """
        from transformers import pipeline
        return pipeline(
            task=model_task,
            model=model_name,
            tokenizer=model_name
        )
    
    @staticmethod
    def use_raw(model_name: str = MODEL_MAP["BART"]) -> tuple:
        """Load a model using the raw API. \n
        Returns:
            *tuple*: A tuple containing the tokenizer and model objects.
        """
        return (
            AutoTokenizer.from_pretrained(model_name),
            AutoModelForSeq2SeqLM.from_pretrained(model_name)
        )
    
    @staticmethod
    def summarAIze(tokenizer: AutoTokenizer, model: AutoModelForSeq2SeqLM, text: str) -> str:
        """Summarize text using the specified tokenizer and model. \n"""

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
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
