import os
from transformers import AutoTokenizer #type: ignore
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax #type: ignore
import yaml #type: ignore
import numpy
import random
import torch

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
    encoded_text = tokenizer(text, return_tensors='pt', truncation=True, padding = 'max_length', max_length=512)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    encoded_text = encoded_text.to(device)
    
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

def classify_sentiment(sentiment_scores): #input = dict, output = string
    
    neg_score = sentiment_scores['roberta_neg']
    neu_score = sentiment_scores['roberta_neu']
    pos_score = sentiment_scores['roberta_pos']
    
    
    if pos_score > 0.9:
        return random.choice(["Extremely Satisfied", "Overwhelmingly Positive", "Highly Favorable", "Exceptionally Positive"])
    elif pos_score > 0.6 or neg_score < 0.2:
        return random.choice(["Pleased", "Satisfied", "Favorable", "Happy"])
    elif neu_score > 0.4:
        return random.choice(["Moderate", "Mixed", "Balanced", "Average"])
    elif neg_score > 0.6 or pos_score < 0.2:
        return random.choice(["Dissatisfied", "Unfavorable", "Unhappy", "Disappointed"])
    elif neg_score > 0.9:
        return random.choice(["Extremely Dissatisfied", "Overwhelmingly Negative", "Very Unhappy", "Strongly Negative"])
    else:
        return "Uncertain"

def aggregate_sentiment_scores(reviews): #input = list of strings, output = dict
    total_scores = {'roberta_neg': 0, 'roberta_neu': 0, 'roberta_pos': 0}
    
    for review in reviews:
        sentiment_scores = get_sentiment_score(review)
        total_scores['roberta_neg'] += sentiment_scores['roberta_neg']
        total_scores['roberta_neu'] += sentiment_scores['roberta_neu']
        total_scores['roberta_pos'] += sentiment_scores['roberta_pos']
    
    #total_scores = {k: v / len(reviews) for k, v in total_scores.items()}
    num_reviews = len(reviews)
    aggregate_scores = {
        'roberta_neg': total_scores['roberta_neg'] / num_reviews,
        'roberta_neu': total_scores['roberta_neu'] / num_reviews,
        'roberta_pos': total_scores['roberta_pos'] / num_reviews
    }
    
    return aggregate_scores

def classify_overall_sentiment(reviews):
    aggregated_score = aggregate_sentiment_scores(reviews)
    overall_sentiment = classify_sentiment(aggregated_score)
    return aggregated_score, overall_sentiment

def get_star_rating(aggregated_scores):

    score = normalizer(aggregated_scores)
    stars = "⭐" * round(score/2)
    return stars 
    # neg_score = aggregated_scores['roberta_neg']
    # neu_score = aggregated_scores['roberta_neu']
    # pos_score = aggregated_scores['roberta_pos']
    
    # star_ratings = {
    #     "5 stars": "⭐⭐⭐⭐⭐",
    #     "4 stars": "⭐⭐⭐⭐",
    #     "3 stars": "⭐⭐⭐",
    #     "2.5 stars": "⭐⭐✨",
    #     "2 stars": "⭐⭐",
    #     "1 star": "⭐"
    # } # emoji dictionary
    
    # if pos_score > 0.9:
    #     return star_ratings["5 stars"]
    # elif pos_score > 0.6 or neg_score < 0.2:
    #     return star_ratings["4 stars"]
    # elif neu_score > 0.4:
    #     return star_ratings["3 stars"]
    # elif neg_score > 0.6 or pos_score < 0.2:
    #     return star_ratings["2 stars"]
    # elif neg_score > 0.9:
    #     return star_ratings["1 star"]
    # else:
    #     return star_ratings["2.5 stars"]

def normalizer(scores):

    neg = scores['roberta_neg']
    neu = scores['roberta_neu']
    pos = scores['roberta_pos']

    score = (neg * 1) + (neu * 5.5) + (pos * 9)
    
    return max(1, min(score, 10))

def main():
    text = "The boat airdopes are based on bluetooth v 5.0 and later and they will work great with all the devices having the same bluetooth version i.e v5.0 or newer however in case of older versions there is a lot of latency lag. The voice is also kind of high so you will not be able to listen to anything on 100 percent anyhow... 50 to 60 is an ideal level for all the movies and games as well as music. Your ears will hurt after prolonged usage of these if you dont select the right size of air caps... 3 sizes are already provided inside the box."
    sentiment_score = get_sentiment_score(text)
    sentiment = classify_sentiment(sentiment_score)
    print(sentiment)
    print(sentiment_score)
    print(normalizer(sentiment_score))
    print(get_star_rating(sentiment_score))

if __name__ == "__main__":
    main()