import streamlit as st
import pandas as pd
import os
import glob
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import requests
from streamlit_lottie import st_lottie
from pymongo import MongoClient

# 🔑 Global MongoDB URI
mongo_uri = "mongodb+srv://biomedicalinformatics100:MyNewSecurePass%2123@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# 🧭 Set page config (must be FIRST)
st.set_page_config(page_title="Tweet Sentiment Analyzer", layout="wide")

# 📽️ Welcome Banner
st.title("📊 Tweet Sentiment Analyzer")

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_banner = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_puciaact.json")
if lottie_banner:
    st_lottie(lottie_banner, height=300)
else:
    st.warning("⚠️ Animation failed to load. Check your internet or animation link.")

st.markdown("""
Welcome to the **Tweet Sentiment Analyzer**! 👋  
Upload your dataset to:
- ✅ Detect sentiment (positive, neutral, negative)  
- ☁️ Generate WordClouds  
- 📈 Track sentiment trends over time  
- 🔍 Filter tweets by keywords
""")

# 🔁 Auto-refresh every 30 sec
st_autorefresh(interval=30 * 1000, key="datarefresh")

# 📥 Load latest CSV
csv_files = sorted(glob.glob("output/results/*.csv"), key=os.path.getmtime)
if csv_files:
    df = pd.concat((pd.read_csv(f, names=["Text", "Sentiment"]) for f in csv_files), ignore_index=True)
else:
    st.error("❌ No CSV files found in the `output/results/` folder.")
    st.stop()

# ⏰ Add Timestamp
timestamps = [datetime.fromtimestamp(os.path.getmtime(f)) for f in csv_files]
if timestamps:
    df["Timestamp"] = pd.to_datetime(timestamps[-1])

# 🎭 Emojis
def sentiment_with_emoji(sentiment):
    return {
        "positive": "😊 Positive",
        "neutral": "😐 Neutral",
        "negative": "😠 Negative"
    }.get(sentiment, sentiment)

df["Sentiment (Emoji)"] = df["Sentiment"].apply(sentiment_with_emoji)

# 🔍 Filter
st.subheader("🔎 Filter by Keyword")
keyword = st.text_input("Enter a keyword to search tweets:")
if keyword:
    df = df[df["Text"].str.contains(keyword, case=False)]

st.success(f"✅ Loaded {len(df)} tweets")

# 🗂️ Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Tweets Table", "📈 Visual Analytics", "☁️ WordClouds",
    "📤 Download", "📦 MongoDB Upload", "📥 Fetch from MongoDB"
])

with tab1:
    st.subheader("📋 Tweets Table")
    st.dataframe(df[["Text", "Sentiment (Emoji)", "Timestamp"]], use_container_width=True)

with tab2:
    st.subheader("📊 Sentiment Distribution (Pie Chart)")
    sentiment_counts = df["Sentiment"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    st.subheader("📈 Sentiment Over Time")
    if "Timestamp" in df.columns:
        trend_df = df.groupby(["Timestamp", "Sentiment"]).size().unstack(fill_value=0)
        st.line_chart(trend_df)

    st.subheader("📊 Sentiment Bar Chart")
    fig_bar, ax_bar = plt.subplots()
    sns.countplot(data=df, x="Sentiment", palette="Dark2", ax=ax_bar)
    st.pyplot(fig_bar)

with tab3:
    st.subheader("☁️ Wordclouds by Sentiment")
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
    st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="sentiment_results.csv", mime="text/csv")

with tab5:
    st.subheader("📦 Push to MongoDB Atlas")
    if st.button("📤 Upload to MongoDB"):
        try:
            client = MongoClient(mongo_uri)
            db = client["sentiment_analysis"]
            collection = db["tweets"]
            upload_df = df[["Text", "Sentiment", "Timestamp"]].dropna().to_dict("records")
            if upload_df:
                collection.insert_many(upload_df)
                st.success(f"✅ Uploaded {len(upload_df)} tweets to MongoDB.")
            else:
                st.warning("⚠️ No data to upload.")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")

with tab6:
    st.subheader("📥 Fetch Tweets from MongoDB Atlas")
    if st.button("Fetch from MongoDB"):
        try:
            client = MongoClient(mongo_uri)
            collection = client["sentiment_analysis"]["tweets"]
            mongo_df = pd.DataFrame(collection.find())
            if not mongo_df.empty:
                st.success("✅ Retrieved data from MongoDB:")
                st.dataframe(mongo_df[["Text", "Sentiment", "Timestamp"]])
            else:
                st.warning("⚠️ No data found in MongoDB.")
        except Exception as e:
            st.error(f"❌ Error fetching from MongoDB: {e}")
