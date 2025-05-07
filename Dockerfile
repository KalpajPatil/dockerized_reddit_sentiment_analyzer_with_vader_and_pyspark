FROM bitnami/spark:3.5.5

USER root

# Install Python dependencies
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install pyspark==3.5.5 confluent-kafka

RUN pip3 install vaderSentiment

# Create required directories
RUN mkdir -p /app /spark_output /checkpoint

# Copy the application files
COPY app/reddit_sentiment.py /app/

# Ensure proper permissions
RUN chmod -R 777 /app /spark_output /checkpoint
RUN chmod +x /app/reddit_sentiment.py 

# Set working directory
WORKDIR /app

USER 1001