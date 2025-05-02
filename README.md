1. A simple sentiment analyzer app that pulls data from r/adidas from the 'Hot' posts of the subreddit.

2. Pulled data is converted to JSON format and written to a Kafka topic

3. A PySpark application uses this Kafka topic as a source to perform data processing and sentiment analysis.

4. Resulting dataframe is written to csv files under /spark_output
