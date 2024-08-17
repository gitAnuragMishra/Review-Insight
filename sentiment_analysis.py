import os
from transformers import AutoTokenizer #type: ignore
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax #type: ignore
import yaml #type: ignore
import numpy
import random
os.environ['HF_HOME'] = r'D:\models'
os.environ['HF_HUB_CACHE'] = r'D:\models'

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)



def initialize_model():
    tokenizer = AutoTokenizer.from_pretrained(config['robert_model']['model_name'], cache_dir = config['cache_dir'])
    model = AutoModelForSequenceClassification.from_pretrained(config['robert_model']['model_name'], cache_dir = config['cache_dir'])
    return tokenizer, model

def get_sentiment_score(text):
    
    tokenizer, model = initialize_model()
    encoded_text = tokenizer(text, return_tensors='pt')
    output = model(**encoded_text)
    tensor_scores = output[0][0].detach().tolist()
    numpy_scores = numpy.array(tensor_scores)
    scores = softmax(numpy_scores)
    scores_dict = {
        'roberta_neg' : scores[0],
        'roberta_neu' : scores[1],
        'roberta_pos' : scores[2]
    }
    return scores_dict


def classify_sentiment(sentiment_scores):
    
    neg_score = sentiment_scores['roberta_neg']
    neu_score = sentiment_scores['roberta_neu']
    pos_score = sentiment_scores['roberta_pos']
    
    
    if pos_score > 0.9:
        return random.choice(["Extremely Satisfied", "Overwhelmingly Positive", "Highly Favorable", "Exceptionally Positive"])
    elif pos_score > 0.6:
        return random.choice(["Pleased", "Satisfied", "Favorable", "Happy", "Content", "Encouraging"])
    elif neu_score > 0.4:
        return random.choice(["Moderate", "Mixed", "Indifferent", "Balanced", "Unremarkable", "Average"])
    elif neg_score > 0.6:
        return random.choice(["Dissatisfied", "Unfavorable", "Unhappy", "Disappointed", "Critical", "Subpar"])
    elif neg_score > 0.9:
        return random.choice(["Extremely Dissatisfied", "Overwhelmingly Negative", "Very Unhappy", "Appalled", "Highly Critical", "Strongly Negative"])
    else:
        return "Mixed/Uncertain"


def main():
    text = "I love this product"
    sentiment_score = get_sentiment_score(text)
    sentiment = classify_sentiment(sentiment_score)
    print(sentiment)


if __name__ == "__main__":
    main()