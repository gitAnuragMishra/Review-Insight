import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM #type: ignore
import yaml #type: ignore

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(config['distilbart_summarization_model']['model_name'], cache_dir=r'D:\models')
model = AutoModelForSeq2SeqLM.from_pretrained(config['distilbart_summarization_model']['model_name'], cache_dir=r'D:\models')

# Check if CUDA is available and move the model to GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def summarise(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)

    # Generate summary on GPU
    summary_ids = model.generate(
        inputs.input_ids,
        max_length=200,
        min_length=100,
        length_penalty=1.0,
        num_beams=8,
        early_stopping=False
    )

    # Decode the summary and move it back to CPU
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
