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

# 🧭 Page Config
st.set_page_config(page_title="Tweet Sentiment Analyzer", layout="wide")
st.title("📊 Tweet Sentiment Analyzer")

# 🎬 Lottie Animation
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_banner = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_puciaact.json")
if lottie_banner:
    st_lottie(lottie_banner, height=300)
else:
    st.warning("⚠️ Animation failed to load.")

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

# 📥 Load CSV
csv_files = sorted(glob.glob("output/results/*.csv"), key=os.path.getmtime)
if csv_files:
    df = pd.concat((pd.read_csv(f, names=["Text", "Sentiment"]) for f in csv_files), ignore_index=True)
    df["Timestamp"] = datetime.fromtimestamp(os.path.getmtime(csv_files[-1]))
else:
    st.error("❌ No CSV files found in output/results/")
    st.stop()

# 😊 Emojis
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

# 🧭 Tabs
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
    trend_df = df.groupby(["Timestamp", "Sentiment"]).size().unstack(fill_value=0)
    st.line_chart(trend_df)

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
            client = MongoClient(mongo_uri)
            db = client["sentiment_analysis"]
            collection = db["tweets"]
            documents = list(collection.find())

            st.write(f"🔍 Fetched {len(documents)} records from MongoDB.")

            if not documents:
                st.warning("⚠️ No documents found in MongoDB.")
            else:
                # Convert to DataFrame
                df_mongo = pd.DataFrame(documents)

                # Ensure _id is string
                if "_id" in df_mongo.columns:
                    df_mongo["_id"] = df_mongo["_id"].astype(str)

                # Parse Timestamp
                if "Timestamp" in df_mongo.columns:
                    df_mongo["Timestamp"] = pd.to_datetime(df_mongo["Timestamp"], errors="coerce")

                # Show debug info
                st.markdown("### 🛠️ Raw MongoDB Sample (2 rows)")
                st.json(df_mongo.head(2).to_dict(orient="records"))

                # Display final DataFrame
                show_cols = [col for col in ["Text", "Sentiment", "Timestamp"] if col in df_mongo.columns]
                if show_cols:
                    st.markdown("### 📋 MongoDB Tweet Records:")
                    st.dataframe(df_mongo[show_cols], use_container_width=True)
                else:
                    st.warning("⚠️ Expected columns not found in MongoDB documents.")

        except Exception as e:
            st.error(f"❌ MongoDB Fetch Error: {e}")
