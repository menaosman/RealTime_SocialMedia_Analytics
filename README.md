
# 📊 Real-Time Social Media Analytics Dashboard

This project implements a real-time social media analytics system using **Apache Spark**, **NLTK**, and **Streamlit** to visualize sentiment analysis on user-generated text.

---

## 🚀 Live App

🔗 [Click here to open the live Streamlit app](https://menaosman-realtime-socialmedia-analytics.streamlit.app)

---

## 🧠 Features

- 📁 Upload your own CSV file with social media comments
- 🧹 Text cleaning (lowercasing, punctuation removal)
- 💬 Sentiment classification using **VADER (NLTK)**
- 📊 Sentiment distribution chart
- ☁️ Word cloud of most common words
- 🔑 Top 10 keywords bar chart

---

## 🛠 How to Use

1. Visit the Streamlit app.
2. Click **Browse files** and upload a CSV file with the following columns:
   - `Text` – original post/comment
   - `clean_text` – preprocessed version of the post
   - `sentiment` – sentiment label: `positive`, `neutral`, or `negative`
3. View instant insights and visualizations.

---

## 🧪 Example Dataset

You can use the included `ready_for_streamlit.csv` for testing, or upload your own dataset after processing.

---

## 📂 Project Structure

```
├── dashboard.py            # Streamlit frontend app
├── requirements.txt        # Required Python packages
├── ready_for_streamlit.csv # Sample dataset
```

---

## 🧰 Tools Used

- **Google Colab** – preprocessing & sentiment scoring
- **Apache Spark (PySpark)** – data processing
- **NLTK (VADER)** – sentiment analysis
- **Streamlit** – interactive dashboard
- **GitHub + Streamlit Cloud** – cloud deployment

---

## 👩‍💻 Author

Mena Osman  
Computer Engineer
Mariam Eslam  
AI Engineer
Nayera Ibrahime, Mariam Mostafa, yomna refaat,reem ramada
Biomedical Informatics | 2025  
GitHub: [@menaosman](https://github.com/menaosman)

---
