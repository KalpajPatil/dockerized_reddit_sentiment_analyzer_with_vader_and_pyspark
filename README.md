<!-- Add badges here -->
<p align="center">
  <img src="https://img.shields.io/badge/docker-ready-blue?logo=docker" alt="Docker Ready" />
  <img src="https://img.shields.io/badge/PySpark-v3.0-orange?logo=apache-spark" alt="PySpark" />
  <img src="https://img.shields.io/badge/VADER-Sentiment-green" alt="VADER Sentiment" />
  <img src="https://img.shields.io/badge/python-3.8-yellow?logo=python" alt="Python 3.8" />
</p>

# 🧠 Reddit Sentiment Analyzer (Dockerized)  
*Using VADER & PySpark*

A project that fetches hot posts from the **r/adidas** subreddit, streams them via Kafka, processes and analyzes sentiment with PySpark & VADER, and exports the results in CSV / Excel. All containerized with Docker + Docker Compose for easy deployment.

---

## 📚 Table of Contents

- [Features](#-features)  
- [Architecture](#-architecture)  
- [Getting Started](#-getting-started)  
- [Usage](#-usage)  
- [Project Structure](#-project-structure)  
- [Requirements](#-requirements)  
- [Contributing](#-contributing)  
- [License](#-license)  

---

## ✅ Features

- Pulls “hot” posts from **r/adidas** subreddit  
- Converts Reddit data to JSON, pushes into a **Kafka** topic  
- Consumes Kafka topic using **PySpark**, applies VADER sentiment analysis  
- Outputs results to:  
  - Excel file under `excel_data/`  
  - CSV file under `final_csv/`  
- Fully dockerized setup: one command to build + run all components

---

## 🏗 Architecture

```text
[ Reddit (r/adidas) ]  
        └─> Reddit Scraper  
               └─> JSON → Kafka Topic  
                       └─> PySpark Job  
                             ├─> Sentiment Analysis (VADER)  
                             └─> Save outputs (Excel / CSV)

🚀 Getting Started
Prerequisites

Docker

Docker Compose

(Optional) Python 3.8+ if you want to run parts locally

Setup & Run
# Clone the repo
git clone https://github.com/KalpajPatil/dockerized_reddit_sentiment_analyzer_with_vader_and_pyspark.git
cd dockerized_reddit_sentiment_analyzer_with_vader_and_pyspark

# Build and start all services
docker-compose up --build


This will start:

Reddit scraper

Kafka broker

PySpark processing

Output saving

📦 Usage

Once everything is up, the scraper will fetch posts and push to Kafka automatically.

PySpark job listens on Kafka, processes text, runs sentiment via VADER.

Final outputs will be in:

excel_data/ → Excel file(s)

final_csv/ → CSV format

Check those directories to see processed data.

🗂 Project Structure
/
├── app/                    # Main application code (scraper, consumer etc.)
├── excel_data/             # Output: Excel files
├── final_csv/              # Output: CSV files
├── spark_output/           # Spark internal output / metadata
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md

⚙ Requirements

Python dependencies (for non-docker/local dev):

vaderSentiment

pyspark

Kafka client (e.g. kafka-python)

Reddit API wrapper (e.g. praw or custom)

Ports used (default, if applicable):

Kafka broker port

Any other ports exposed by services

Adjust docker-compose.yml / configs if needed.
