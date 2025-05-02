import time
import praw
import traceback
import json
from kafka import KafkaProducer

reddit = praw.Reddit(
    client_id="your_client_id", #enter your own reddit client id
    client_secret="your_client_secret", #enter your own reddit client secret key
    user_agent="adidas_subreddit_data/1.0"
)

subreddit = reddit.subreddit("adidas")
# Sample data to produce to Kafka topic
sample_posts = []

try:
    global posts_dict
    posts = []
    posts_dict = {}
    for post in subreddit.hot(limit=11):
        data_dict = {}
        comment_list = []
        post.comments.replace_more(limit=0)
        if post.title.startswith("For all the"):
            continue
        data_dict["title"] = post.title
        data_dict["link"] = f"https://reddit.com{post.permalink}"
        for comment in post.comments.list():
            if comment.body and comment.body != "[deleted]":
                author = comment.author.name if comment.author else "Anonymous"
                body_snippet = comment.body[:150].replace('\n', ' ')
                comment_list.append(body_snippet)
        data_dict["comments"] = comment_list
        posts.append(data_dict)
    posts_dict["posts"] = posts
except Exception as e:
        print(f"exception = {e}")
        traceback.print_exc()

sample_posts = posts_dict["posts"]

def deliver_sample_data():
    # Create producer
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    print("Connected to Kafka broker, sending sample data...")
    
    # Produce each post with delay
    for post in sample_posts:
        print(f"Sending post: {post['title']}")
        producer.send('reddit_posts_from_r_adidas_may1_6', post)
        producer.flush()
    
    print("Sample data sent successfully!")

if __name__ == "__main__":
    # Wait for Kafka to be ready
    time.sleep(10)
    deliver_sample_data()