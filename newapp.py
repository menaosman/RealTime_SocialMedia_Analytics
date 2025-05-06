import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from streamlit_lottie import st_lottie
import requests
from pymongo import MongoClient

# MongoDB URI (encoded)
mongo_uri = "mongodb+srv://biomedicalinformatics100:MyNewSecurePass%2123@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

st.set_page_config(page_title="Tweet Sentiment Analyzer", layout="wide")

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
- 🌥 Generate WordClouds
- 📈 Track sentiment trends over time
- 🔍 Filter tweets by keywords
""")

uploaded_file = st.file_uploader("📂 Upload a CSV file with a 'Text' column", type=["csv"])

if "start_clicked" not in st.session_state:
    st.session_state.start_clicked = False

if st.button("🚀 Start Sentiment Analysis"):
    st.session_state.start_clicked = True

if uploaded_file and st.session_state.start_clicked:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()

    if 'text' not in df.columns:
        st.error("❌ The uploaded file must contain a 'Text' column.")
    else:
        analyzer = SentimentIntensityAnalyzer()

        def get_sentiment(text):
            score = analyzer.polarity_scores(str(text))['compound']
            if score >= 0.05:
                return 'positive'
            elif score <= -0.05:
                return 'negative'
            else:
                return 'neutral'

        df['Sentiment'] = df['text'].astype(str).apply(get_sentiment)

        st.success("✅ Sentiment analysis completed!")
        st.dataframe(df[['text', 'Sentiment']])

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results as CSV", csv, "sentiment_results.csv", "text/csv")

        st.subheader("📈 Sentiment Distribution (Bar Chart)")
        st.bar_chart(df['Sentiment'].value_counts())

        sentiment_filter = st.selectbox("🔍 Filter by Sentiment", ['all', 'positive', 'neutral', 'negative'])
        if sentiment_filter != 'all':
            filtered_df = df[df['Sentiment'] == sentiment_filter]
            st.write(f"Showing {len(filtered_df)} {sentiment_filter} tweets:")
            st.dataframe(filtered_df[['text', 'Sentiment']])

        st.subheader("🌥 WordClouds by Sentiment")
        for sentiment in ['positive', 'neutral', 'negative']:
            subset = df[df['Sentiment'] == sentiment]
            text = " ".join(subset['text'].astype(str))
            if text:
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                st.markdown(f"#### {sentiment.capitalize()} Tweets")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.warning(f"No {sentiment} tweets available for WordCloud.")

        st.subheader("🔎 Filter by Keyword")
        keyword = st.text_input("Enter a keyword to search for tweets:")
        if keyword:
            keyword_df = df[df['text'].str.contains(keyword, case=False, na=False)]
            st.write(f"Found {len(keyword_df)} tweets containing '{keyword}':")
            st.dataframe(keyword_df[['text', 'Sentiment']])
            st.bar_chart(keyword_df['Sentiment'].value_counts())

        st.subheader("🧮 Sentiment Summary")
        counts = df['Sentiment'].value_counts()
        st.write(counts)

        st.subheader("📊 Sentiment Breakdown (Pie Chart)")
        fig1, ax1 = plt.subplots()
        ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

        if 'timestamp' in df.columns:
            st.subheader("🕒 Sentiment Over Time")
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            timeline = df.groupby([pd.Grouper(key='timestamp', freq='D'), 'Sentiment']).size().unstack().fillna(0)
            st.line_chart(timeline)

# 🧲 Fetch from MongoDB
st.subheader("📥 Fetch Tweets from MongoDB Atlas")
if st.button("Fetch from MongoDB"):
    try:
        client = MongoClient(mongo_uri)
        collection = client["sentiment_analysis"]["tweets"]
        mongo_df = pd.DataFrame(collection.find())

        if not mongo_df.empty:
            mongo_df["_id"] = mongo_df["_id"].astype(str)
            if "Timestamp" in mongo_df.columns:
                mongo_df["Timestamp"] = pd.to_datetime(mongo_df["Timestamp"])

            display_cols = [col for col in ["Text", "Sentiment", "Timestamp"] if col in mongo_df.columns]
            st.success(f"✅ Retrieved {len(mongo_df)} tweets from MongoDB:")
            st.dataframe(mongo_df[display_cols], use_container_width=True)
            st.bar_chart(mongo_df["Sentiment"].value_counts())
        else:
            st.warning("⚠️ No data found in MongoDB.")
    except Exception as e:
        st.error(f"❌ Error fetching from MongoDB: {e}")
