FROM python

WORKDIR /app

COPY /app/producer/producer.py /app/

RUN apt-get update && apt-get install -y python3-pip && \
        pip3 install kafka-python && \
        pip3 install praw

RUN chmod +x /app/producer.py

CMD [ "python", "producer.py" ]