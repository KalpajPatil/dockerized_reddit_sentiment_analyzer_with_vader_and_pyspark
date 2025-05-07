import time
import praw
import traceback
import json
import confluent_kafka

KAFKA_TOPIC = "reddit_posts_from_r_adidas"

reddit = praw.Reddit(
    client_id="KmHb_sStduvNxMCeJmPX_w", #enter your own reddit client id
    client_secret="Ns3JCr238oVfaYquTLpLsJyPjUAd3Q", #enter your own reddit client secret key
    user_agent="adidas_subreddit_data/1.0"
)

subreddit = reddit.subreddit("adidas")

#data to write to Kafka topic
sample_posts = []

try:
    global posts_dict
    posts = []
    posts_dict = {}
    for post in subreddit.hot(limit=200):
        data_dict = {}
        comment_list = []
        post.comments.replace_more(limit=0)
        if post.stickied:
            continue
        data_dict["title"] = post.title
        data_dict["link"] = f"https://reddit.com{post.permalink}"
        for comment in post.comments.list():
            comment_item = {}
            if comment.body and comment.body != "[deleted]":
                author = comment.author.name if comment.author else "Anonymous"
                body_snippet = comment.body[:].replace('\n', ' ')
                #comment.score = total upvotes - total downvotes on a comment
                comment_score = comment.score
                comment_item["comment"] = body_snippet
                comment_item["score"] = comment_score
                comment_list.append(comment_item)
        data_dict["comments"] = comment_list
        posts.append(data_dict)
    posts_dict["posts"] = posts
except Exception as e:
        print(f"exception = {e}")
        traceback.print_exc()

sample_posts = posts_dict["posts"]

def deliver_sample_data():
    # Create producer
    producer = confluent_kafka.Producer(
        {
            "bootstrap.servers" : "kafka:9092"
        }
    )
    
    print("Connected to Kafka broker, sending sample data...")

    for post in sample_posts:
        print(f"Sending post: {post['title']}")
        producer.poll(1.0)
        producer.produce(
            topic = KAFKA_TOPIC,
            value = json.dumps(post).encode('utf-8'),
        )
    print("Sample data sent successfully!")
    producer.flush()


if __name__ == "__main__":
    # Wait for Kafka to be ready
    time.sleep(15)
    deliver_sample_data()