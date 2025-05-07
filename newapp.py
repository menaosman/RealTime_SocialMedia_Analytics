import streamlit as st
import pandas as pd
import os
import glob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import requests
from streamlit_lottie import st_lottie
from pymongo import MongoClient

# 🔑 MongoDB URI
mongo_uri = "mongodb+srv://biomedicalinformatics100:MyNewSecurePass%2123@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# ⚙️ Page setup
st.set_page_config(page_title="Tweet Sentiment Analyzer", layout="wide")
st.title("📊 Tweet Sentiment Analyzer")

# 🎬 Load Lottie animation (with caching)
@st.cache_data(show_spinner=False)
def load_lottie_url(url):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_puciaact.json")
if lottie:
    st_lottie(lottie, height=300)
else:
    st.warning("⚠️ Lottie animation failed to load.")

# 🧾 Welcome message
st.markdown("""
Welcome to the **Tweet Sentiment Analyzer**! 👋  
Upload your dataset to:
- ✅ Detect sentiment (positive, neutral, negative)  
- ☁️ Generate WordClouds  
- 📈 Track sentiment trends over time  
- 🔍 Filter tweets by keywords
""")

# 📥 Load latest CSV
@st.cache_data(show_spinner=True)
def load_latest_csv():
    files = sorted(glob.glob("output/results/*.csv"), key=os.path.getmtime)
    if not files:
        return None, None
    latest = files[-1]
    df = pd.read_csv(latest, names=["Text", "Sentiment"])
    df["Timestamp"] = datetime.fromtimestamp(os.path.getmtime(latest))
    return df, len(files)

df, file_count = load_latest_csv()
if df is None:
    st.error("❌ No CSV files found in output/results/")
    st.stop()

# 😊 Add emoji to sentiments
def sentiment_with_emoji(sentiment):
    return {
        "positive": "😊 Positive",
        "neutral": "😐 Neutral",
        "negative": "😠 Negative"
    }.get(sentiment, sentiment)

df["Sentiment (Emoji)"] = df["Sentiment"].apply(sentiment_with_emoji)

# 🔍 Keyword filter
st.subheader("🔎 Filter by Keyword")
keyword = st.text_input("Enter a keyword to search tweets:")
if keyword:
    df = df[df["Text"].str.contains(keyword, case=False)]

st.success(f"✅ Loaded {len(df)} tweets from {file_count} file(s)")

# 🗂️ Interface tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Tweets Table", "📈 Visual Analytics", "☁️ WordClouds",
    "📤 Download", "📦 MongoDB Upload", "📥 Fetch from MongoDB"
])

with tab1:
    st.subheader("📋 Tweets Table")
    st.dataframe(df[["Text", "Sentiment (Emoji)", "Timestamp"]], use_container_width=True)

with tab2:
    st.subheader("📊 Sentiment Distribution")
    fig1, ax1 = plt.subplots()
    df["Sentiment"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1)
    ax1.set_ylabel('')
    st.pyplot(fig1)

    st.subheader("📈 Sentiment Over Time")
    timeline = df.groupby(["Timestamp", "Sentiment"]).size().unstack(fill_value=0)
    st.line_chart(timeline)

    st.subheader("📊 Sentiment Bar Chart")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df, x="Sentiment", palette="Dark2", ax=ax2)
    st.pyplot(fig2)

with tab3:
    st.subheader("☁️ WordClouds")
    for sentiment in ["positive", "neutral", "negative"]:
        st.markdown(f"### {sentiment.capitalize()} Tweets")
        text = " ".join(df[df["Sentiment"] == sentiment]["Text"])
        if text.strip():
            wc = WordCloud(width=800, height=400, background_color="white").generate(text)
            st.image(wc.to_array())
        else:
            st.info("No data for this sentiment.")

with tab4:
    st.subheader("📥 Download Results")
    st.download_button("Download CSV", df.to_csv(index=False), "sentiment_results.csv", "text/csv")

with tab5:
    st.subheader("📦 Push to MongoDB Atlas")
    if st.button("📤 Upload to MongoDB"):
        try:
            client = MongoClient(mongo_uri)
            collection = client["sentiment_analysis"]["tweets"]
            upload_df = df[["Text", "Sentiment", "Timestamp"]].dropna().to_dict("records")
            if upload_df:
                collection.insert_many(upload_df)
                st.success(f"✅ Uploaded {len(upload_df)} tweets.")
            else:
                st.warning("⚠️ No data to upload.")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")

with tab6:
    st.subheader("📥 Fetch Tweets from MongoDB Atlas")
    if st.button("Fetch from MongoDB"):
        try:
            client = MongoClient(
                mongo_uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=30000
            )
            collection = client["sentiment_analysis"]["tweets"]
            cursor = collection.find({}, {"_id": 0, "Text": 1, "Sentiment": 1, "Timestamp": 1})
            data = list(cursor)

            if data:
                st.success(f"✅ Retrieved {len(data)} tweets from MongoDB.")
                df_mongo = pd.DataFrame(data)

                if "Timestamp" in df_mongo.columns:
                    df_mongo["Timestamp"] = pd.to_datetime(df_mongo["Timestamp"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M")

                df_mongo["Sentiment (Emoji)"] = df_mongo["Sentiment"].apply(sentiment_with_emoji)
                st.dataframe(df_mongo[["Text", "Sentiment (Emoji)", "Timestamp"]], use_container_width=True)

            else:
                st.warning("⚠️ No documents found in MongoDB.")
        except Exception as e:
            st.error(f"❌ MongoDB fetch error: {e}")
