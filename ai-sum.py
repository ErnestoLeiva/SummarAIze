import transformers  


TF_ENABLE_ONEDNN_OPTS=0 # This is a workaround for a known issue with TensorFlow and OneDNN optimizations



if __name__ == "__main__":
    # Load the model and tokenizer
    model_name = "facebook/bart-large-cnn"
    model = transformers.AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

    # Example text to summarize
    text = """
    There w
    """

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)

    # Generate summary
    summary_ids = model.generate(inputs["input_ids"], max_length=50, min_length=25, length_penalty=2.0, num_beams=4, early_stopping=True)

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    print("Summary:", summary)