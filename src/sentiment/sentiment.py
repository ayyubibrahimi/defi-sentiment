import pandas as pd
import os
import re
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

def classify_sentiment(comment, classifier, max_length=512):
    sentiment_labels = ["Negative", "Positive"]
    
    result = classifier(comment, max_length=max_length, truncation=True)
    sentiment_label = sentiment_labels[int(result[0]['label'][-1])]
    
    return sentiment_label

def analyze_sentiment(directory, model_name, max_length=512):
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            
            comments_df = df[df["data_type"] == "comment"].copy()
            comments_df.loc[:, "sentiment"] = comments_df["body"].apply(lambda x: classify_sentiment(x, classifier, max_length))
            
            total_comments = len(comments_df)
            positive_comments = len(comments_df[comments_df["sentiment"] == "Positive"])
            negative_comments = len(comments_df[comments_df["sentiment"] == "Negative"])
            
            positive_percentage = (positive_comments / total_comments) * 100 if total_comments > 0 else 0
            negative_percentage = (negative_comments / total_comments) * 100 if total_comments > 0 else 0
            
            post_id = re.findall(r"(\w+)_data\.csv", filename)[0]
            
            print(f"Sentiment Metrics for Post ID: {post_id}")
            print(f"Total Comments: {total_comments}")
            print(f"Positive Comments: {positive_comments} ({positive_percentage:.2f}%)")
            print(f"Negative Comments: {negative_comments} ({negative_percentage:.2f}%)")
            print("---")
    
    print("Sentiment analysis completed.")

if __name__ == "__main__":
    directory = "../data/output_extraction"
    model_name = "kk08/CryptoBERT"
    max_length = 512
    
    analyze_sentiment(directory, model_name, max_length)