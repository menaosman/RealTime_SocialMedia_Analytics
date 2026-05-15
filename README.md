<div align="center">

# 📡 Real-Time Social Media Sentiment Analysis Pipeline

**A cloud-native, production-grade streaming analytics system built with Apache Kafka, Apache Spark, Docker, and MongoDB Atlas — deployed via CI/CD to Railway Cloud Platform.**

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-2.8-231F20?style=flat-square&logo=apache-kafka&logoColor=white)](https://kafka.apache.org)
[![Apache Spark](https://img.shields.io/badge/Apache_Spark-3.3-E25A1C?style=flat-square&logo=apache-spark&logoColor=white)](https://spark.apache.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Railway](https://img.shields.io/badge/Deployed-Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)](https://railway.app)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[Overview](#-overview) · [Architecture](#-architecture) · [Results](#-results--performance) · [Tech Stack](#-tech-stack) · [Setup](#-quick-start) · [Dashboards](#-dashboards) · [Contact](#-contact)

</div>

---

## 🧠 Overview

This system continuously streams and analyzes social media data in **near real-time**, applying NLP-based sentiment classification at scale. Built end-to-end from raw data ingestion to interactive dashboards — designed to mirror production-grade cloud analytics pipelines used in industry.

### What it does

| Stage | Technology | Description |
|-------|-----------|-------------|
| **Ingest** | Apache Kafka | Streams 10,000+ tweets/hour via producer-consumer architecture |
| **Process** | Apache Spark Structured Streaming | Applies VADER sentiment analysis on each micro-batch in real time |
| **Store** | MongoDB Atlas | Persists processed sentiment records with timestamps and keywords |
| **Serve** | Flask REST API | Exposes analytics endpoints with sub-200ms average response time |
| **Visualize** | Streamlit + Flask Dashboards | Interactive charts, WordClouds, trend graphs with auto-refresh |
| **Deploy** | Docker + GitHub Actions + Railway | Fully automated CI/CD pipeline with zero-downtime releases |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW                                    │
│                                                                     │
│  Twitter/Mock API                                                   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────┐      ┌──────────────────────┐                     │
│  │  Kafka      │      │  Spark Structured     │                     │
│  │  Producer   │─────▶│  Streaming            │                     │
│  │  (tweets)   │      │  (VADER Sentiment)    │                     │
│  └─────────────┘      └──────────┬───────────┘                     │
│                                  │                                  │
│                                  ▼                                  │
│                        ┌─────────────────┐                         │
│                        │  MongoDB Atlas  │                         │
│                        │  (Persistence)  │                         │
│                        └────────┬────────┘                         │
│                                 │                                   │
│              ┌──────────────────┼──────────────────┐               │
│              ▼                  ▼                  ▼               │
│       ┌────────────┐    ┌──────────────┐   ┌────────────┐          │
│       │  Flask API │    │  Streamlit   │   │  Flask     │          │
│       │  (REST)    │    │  Dashboard   │   │  Dashboard │          │
│       └────────────┘    └──────────────┘   └────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT PIPELINE                             │
│                                                                     │
│  Git Push → GitHub Actions → Docker Build → Railway Cloud Deploy   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**Stream Layer — Apache Kafka**
- Kafka producer fetches and streams tweets into a dedicated topic
- Consumer groups allow multiple Spark workers to consume in parallel
- Configured with Docker Compose for local development and Railway for cloud

**Processing Layer — Apache Spark**
- Spark Structured Streaming reads from the Kafka topic in micro-batches
- VADER (Valence Aware Dictionary and sEntiment Reasoner) classifies each tweet as Positive / Negative / Neutral
- Aggregated results are written to MongoDB Atlas in real time

**Storage Layer — MongoDB Atlas**
- Stores raw tweet text, sentiment label, confidence score, keyword tags, and timestamp
- Indexed on timestamp and sentiment for efficient dashboard queries

**API Layer — Flask REST**
- RESTful endpoints for fetching sentiment summaries, filtered results, and raw records
- Benchmarked at **< 200ms average response time** under concurrent load (validated via Postman)

**Visualization Layer — Dual Dashboards**
- **Streamlit**: Pie charts, bar plots, sentiment trend lines, WordClouds, keyword filtering, CSV export, auto-refresh
- **Flask + Chart.js**: Interactive charts with Lottie animations, real-time MongoDB polling

**CI/CD — GitHub Actions + Railway**
- Every push to `main` triggers automated testing → Docker image build → Railway deployment
- Docker Compose manages multi-service local orchestration (Kafka, Spark, MongoDB, Flask, Streamlit)

---

## 📊 Results & Performance

| Metric | Value |
|--------|-------|
| **Streaming throughput** | 10,000+ tweets / hour |
| **Average API response time** | < 200ms (Flask on Railway) |
| **Sentiment classification latency** | Near real-time (micro-batch < 2s) |
| **Deployment pipeline** | Fully automated (0 manual steps after push) |
| **Uptime** | Continuous via Railway cloud hosting |
| **Dashboard refresh rate** | Auto-refresh every 30 seconds |

### Sentiment Distribution (Sample Run)

```
Positive  ████████████████░░░░  48.3%
Neutral   █████████░░░░░░░░░░░  27.1%
Negative  ████████░░░░░░░░░░░░  24.6%
```

> Tested on a 72-hour continuous stream of ~720,000 tweets using keyword-filtered topics.

---

## 🛠 Tech Stack

### Core Pipeline

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Message Broker** | Apache Kafka 2.8 | Real-time tweet streaming |
| **Stream Processor** | Apache Spark 3.3 (Structured Streaming) | VADER NLP + aggregation |
| **NLP Engine** | VADER (vaderSentiment) | Sentiment classification |
| **Database** | MongoDB Atlas | Processed result storage |
| **Backend API** | Flask (Python) | REST endpoints |
| **Frontend (1)** | Streamlit | Interactive analytics dashboard |
| **Frontend (2)** | HTML / CSS / Chart.js / Lottie | Flask-served dashboard |

### DevOps & Cloud

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Containerization** | Docker + Docker Compose | Multi-service orchestration |
| **CI/CD** | GitHub Actions | Automated test → build → deploy |
| **Cloud Platform** | Railway | Production deployment |
| **Testing** | Postman + Chrome DevTools | API + frontend benchmarking |
| **Version Control** | Git + GitHub | Source control |

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- MongoDB Atlas account (free tier works)
- A Twitter Developer account or use the included mock data generator

### 1. Clone the repository

```bash
git clone https://github.com/menaosman/realtime-sentiment-pipeline.git
cd realtime-sentiment-pipeline
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# MongoDB
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/sentiment_db

# Twitter API (optional — mock generator works without this)
TWITTER_BEARER_TOKEN=your_bearer_token_here

# Flask
FLASK_SECRET_KEY=your_secret_key
FLASK_PORT=5000

# Kafka
KAFKA_BROKER=kafka:9092
KAFKA_TOPIC=tweets
```

### 3. Start all services with Docker Compose

```bash
docker-compose up --build
```

This starts:
- Zookeeper (Kafka dependency)
- Kafka broker
- Spark master + worker
- MongoDB (local, for development)
- Flask API server
- Streamlit dashboard

### 4. Access the dashboards

| Service | URL |
|---------|-----|
| Streamlit Dashboard | http://localhost:8501 |
| Flask Dashboard | http://localhost:5000 |
| Flask API | http://localhost:5000/api/sentiment |
| Kafka UI (optional) | http://localhost:8080 |

### 5. Run the tweet producer

```bash
# Using mock data (no Twitter API required)
python producer/mock_producer.py

# Using real Twitter API
python producer/twitter_producer.py
```

---

## 📡 API Reference

### `GET /api/sentiment`
Returns aggregated sentiment counts.

```json
{
  "positive": 4832,
  "negative": 2461,
  "neutral": 2710,
  "total": 9003,
  "last_updated": "2025-04-12T14:30:00Z"
}
```

### `GET /api/tweets?sentiment=positive&limit=20`
Returns filtered tweet records.

```json
{
  "tweets": [
    {
      "text": "Amazing technology...",
      "sentiment": "positive",
      "score": 0.87,
      "timestamp": "2025-04-12T14:29:45Z",
      "keywords": ["technology", "amazing"]
    }
  ]
}
```

### `GET /api/trends?window=1h`
Returns sentiment trend data over a time window (`1h`, `6h`, `24h`, `7d`).

---

## 📊 Dashboards

### Streamlit Dashboard
- **Sentiment pie chart** — live distribution of Positive / Negative / Neutral
- **Time-series trend graph** — sentiment shifts over configurable time windows
- **WordCloud** — most frequent words per sentiment category
- **Keyword filter** — search and filter tweets by topic in real time
- **CSV export** — download processed data for offline analysis
- **Auto-refresh** — updates every 30 seconds without page reload

### Flask Dashboard
- **Real-time bar charts** (Chart.js) with animated transitions
- **Tweet feed table** — live scrolling table of latest classified tweets
- **Lottie animations** — visual feedback for loading and sentiment states
- **RESTful backend** — all data fetched from the Flask API layer

---

## 📁 Project Structure

```
realtime-sentiment-pipeline/
│
├── producer/
│   ├── twitter_producer.py      # Streams real tweets to Kafka
│   └── mock_producer.py         # Generates mock tweet data (no API needed)
│
├── spark/
│   └── sentiment_processor.py   # Spark Structured Streaming + VADER
│
├── api/
│   ├── app.py                   # Flask REST API
│   └── routes/
│       ├── sentiment.py
│       └── trends.py
│
├── dashboards/
│   ├── streamlit_app.py         # Streamlit dashboard
│   └── flask_dashboard/         # Flask + Chart.js + Lottie dashboard
│       ├── templates/
│       └── static/
│
├── docker-compose.yml           # Full multi-service orchestration
├── Dockerfile                   # Flask API container
├── .github/
│   └── workflows/
│       └── deploy.yml           # CI/CD: test → build → Railway deploy
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔄 CI/CD Pipeline

Every push to `main` automatically:

1. **Runs tests** — unit tests for Flask API and Spark processing logic
2. **Builds Docker image** — containerizes the Flask API
3. **Pushes to Docker Hub** — tags with commit SHA and `latest`
4. **Deploys to Railway** — zero-downtime rolling deployment
5. **Health check** — verifies API responds within 5 seconds post-deploy

```yaml
# .github/workflows/deploy.yml (simplified)
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest tests/
      - name: Build and push Docker image
        run: |
          docker build -t menaosman/sentiment-pipeline:${{ github.sha }} .
          docker push menaosman/sentiment-pipeline:${{ github.sha }}
      - name: Deploy to Railway
        run: railway up
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run API tests only
pytest tests/test_api.py -v

# Run with coverage report
pytest tests/ --cov=api --cov-report=term-missing
```

API endpoints were benchmarked using **Postman** (response time validation) and **Chrome DevTools** (Streamlit frontend rendering performance).

---

## 🗺 Roadmap

- [ ] Add Twitter API v2 streaming support
- [ ] Implement topic modelling (LDA) alongside sentiment
- [ ] Add multi-language sentiment support (Arabic NLP)
- [ ] Kubernetes deployment config (Helm chart)
- [ ] Grafana dashboard integration via MongoDB connector
- [ ] Add alerting (PagerDuty / Slack webhook) for sentiment anomalies

---

## 👤 Author

**Mena Mohamed Osman**
Computer Engineering (Cybersecurity) — Galala University | GPA 3.8

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/mena-osman-b92641238)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/menaosman)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:mennnamohamed200@gmail.com)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

⭐ **If you found this project useful, please consider giving it a star!** ⭐

*Built with ❤️ as part of a Cloud Computing & Big Data course project — extended into a production-grade system.*

</div>
