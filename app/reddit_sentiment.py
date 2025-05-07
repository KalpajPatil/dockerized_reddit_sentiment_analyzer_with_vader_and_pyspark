import traceback
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, udf, lit
from pyspark.sql.types import StructType, StringType, ArrayType, DoubleType, IntegerType, StructField
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

OUTPUT_PATH = "/spark_output"
CHECKPOINT_LOCATION = "/checkpoint"

def setup_spark_context():
    global spark
    spark = SparkSession.builder \
        .appName("RedditSentimentStream") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,com.mysql:mysql-connector-j:8.2.0") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

def process_data():
    comment_schema = StructType([StructField("comment", StringType(), True), StructField("score", IntegerType(), True)])

    schema = StructType() \
        .add("title", StringType()) \
        .add("link", StringType()) \
        .add("comments", ArrayType(comment_schema)) \

    raw_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "reddit_posts_from_r_adidas") \
        .option("startingOffsets", "latest") \
        .load()

    parsed_df = raw_df.selectExpr("CAST(value AS STRING) as json_str") \
        .select(from_json(col("json_str"), schema).alias("data")) \
        .select("data.*")
    
    comments_df = parsed_df.select(
        "title",
        "link",
        explode("comments").alias("comment_struct")
    ).select(
        "title",
        "link",
        col("comment_struct.comment").alias("comment"),
        col("comment_struct.score").alias("score")
    )

    #explode the comments array into seperate rows
    # comments_df = parsed_df.withColumn("comment", explode(col("comments"))) \
    #                     .select("title", "link", "comment")

    analyzer = SentimentIntensityAnalyzer()

    #user-defined function which will apply to every row of our df on "comment" column
    @udf(returnType= DoubleType())
    def get_sentiment_score(text):
        if text:
            return float(analyzer.polarity_scores(text)["compound"])
        return 0.0

    #df with sentiment scores column
    scored_df = comments_df.withColumn("sentiment", get_sentiment_score(col("comment")))

    try:
       scored_df.writeStream \
            .format("csv") \
            .option("path", OUTPUT_PATH + "/output_data") \
            .option("checkpointLocation", CHECKPOINT_LOCATION) \
            .option("header", "true") \
            .option("escape", '"') \
            .option("multiLine", True) \
            .trigger(processingTime='3 seconds') \
            .start() \
            .awaitTermination()
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    setup_spark_context()
    process_data()
