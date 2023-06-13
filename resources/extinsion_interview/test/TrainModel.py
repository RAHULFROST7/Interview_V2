from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
import joblib

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
 
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def sentimentAnalyzer(text):
    # Tasks:
    # emoji, emotion, hate, irony, offensive, sentiment
    # stance/abortion, stance/atheism, stance/climate, stance/feminist, stance/hillary

    task='sentiment'
    MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

    # define the cache filenames
    tokenizer_cache_filename = f"{MODEL}_tokenizer.joblib"
    model_cache_filename = f"{MODEL}_model.joblib"
    labels_cache_filename = f"{MODEL}_labels.joblib"

    # try to load from cache
    try:
        # load tokenizer, model, and labels from cache
        tokenizer = joblib.load(tokenizer_cache_filename)
        model = joblib.load(model_cache_filename)
        labels = joblib.load(labels_cache_filename)

    except FileNotFoundError:
        # download label mapping
        labels=[]
        mapping_link = "mapping.txt"
        with urllib.request.urlopen(mapping_link) as f:
            html = f.read().decode('utf-8').split("\n")
            csvreader = csv.reader(html, delimiter='\t')
        labels = [row[1] for row in csvreader if len(row) > 1]

        # load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)

        # save tokenizer, model, and labels to cache
        joblib.dump(tokenizer, tokenizer_cache_filename)
        joblib.dump(model, model_cache_filename)
        joblib.dump(labels, labels_cache_filename)
    
    # text = "The weather today is bad"
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    c=0
    lists = []
    for i in range(scores.shape[0]):
        l = labels[ranking[i]]
        s = scores[ranking[i]]
        lists.append(f"{l}:{np.round(float(s), 2)}")
        c+=1
        if c >= 2 :
            break
        else:
            continue
    return lists
print(sentimentAnalyzer("Rahul is feeling so good"))
    
