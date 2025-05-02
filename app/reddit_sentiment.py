import traceback
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, udf, lit
from pyspark.sql.types import StructType, StringType, ArrayType, DoubleType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
OUTPUT_PATH = "/spark_output"
CHECKPOINT_LOCATION = "/newcheckpoints"

def setup_spark_context():
    global spark
    spark = SparkSession.builder \
        .appName("RedditSentimentStream") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,com.mysql:mysql-connector-j:8.2.0") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

def process_data():
    schema = StructType() \
        .add("title", StringType()) \
        .add("link", StringType()) \
        .add("comments", ArrayType(StringType()))


    raw_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "reddit_posts_from_r_adidas_may1_6") \
        .option("startingOffsets", "latest") \
        .load()

    parsed_df = raw_df.selectExpr("CAST(value AS STRING) as json_str") \
        .select(from_json(col("json_str"), schema).alias("data")) \
        .select("data.*")

    #explode the comments array into seperate rows
    comments_df = parsed_df.withColumn("comment", explode(col("comments"))) \
                        .select("title", "link", "comment")

    # Define a UDF for sentiment score using VADER
    analyzer = SentimentIntensityAnalyzer()

    #user-defined function which will apply to every row of our df on "comment" column
    @udf(returnType= DoubleType())
    def get_sentiment_score(text):
        if text:
            return float(analyzer.polarity_scores(text)["compound"])
        return 0.0

    # @udf(returnType= DoubleType())
    # def get_random_sentiment(dummy):
    #     return random.uniform(-1.0,1.0)

    scored_df = comments_df.withColumn("sentiment", get_sentiment_score(col("comment")))

    #get average sentiment on each post
    agg_df = scored_df.groupBy("title", "link").avg("sentiment") \
                    .withColumnRenamed("avg(sentiment)", "avg_sentiment")

    try:
       scored_df.writeStream \
            .format("csv") \
            .option("path", OUTPUT_PATH) \
            .option("checkpointLocation", CHECKPOINT_LOCATION) \
            .option("header", "true") \
            .trigger(processingTime='5 seconds') \
            .start() \
            .awaitTermination()
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    setup_spark_context()
    process_data()
