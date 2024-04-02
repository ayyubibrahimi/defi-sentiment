import praw
import pandas as pd
from datetime import datetime, timedelta
import os

def extract_data(subreddit_name, client_id, client_secret, user_agent, output_directory, time_window_days):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subreddit = reddit.subreddit(subreddit_name)
    current_timestamp = datetime.utcnow()
    
    os.makedirs(output_directory, exist_ok=True)
    
    post_data = []
    comment_data = []
    
    for post in subreddit.new(limit=None):
        post_timestamp = datetime.utcfromtimestamp(post.created_utc)
        print(f"Processing post: {post.title}")
        
        if current_timestamp - post_timestamp <= timedelta(days=time_window_days):
            post_info = {
                "data_type": "post",
                "post_id": post.id,
                "title": post.title,
                "author": post.author.name if post.author else None,
                "created_utc": post.created_utc,
                "score": post.score,
                "num_comments": post.num_comments,
                "url": post.url,
                "body": post.selftext
            }
            post_data.append(post_info)
            
            post.comments.replace_more(limit=None)
            for comment in post.comments.list():
                print(f"Processing comment: {comment.body[:50]}...")
                comment_info = {
                    "data_type": "comment",
                    "post_id": post.id,
                    "comment_id": comment.id,
                    "author": comment.author.name if comment.author else None,
                    "created_utc": comment.created_utc,
                    "score": comment.score,
                    "body": comment.body
                }
                comment_data.append(comment_info)
    
    combined_data = post_data + comment_data
    combined_df = pd.DataFrame(combined_data)
    
    filename = f"{output_directory}/combined_data.csv"
    combined_df.to_csv(filename, index=False)
    
    print("Data extraction completed.")

if __name__ == "__main__":
    client_id = "X6yBUfvCAvEu84hNy7O-_w"
    client_secret = "zJAUcg1M_KSPLd5eU-DLnp0cSEbiMg"
    user_agent = "defi/1.0 (http://localhost:8080; ayyub.ibrahimi@gmail.com)"
    
    subreddit_name = "defi"
    output_directory = "../data/output_extraction"
    time_window_days = 30
    
    extract_data(subreddit_name, client_id, client_secret, user_agent, output_directory, time_window_days)