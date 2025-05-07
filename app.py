import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from streamlit_lottie import st_lottie
from datetime import datetime
import requests
from pymongo import MongoClient

st.set_page_config(page_title="Tweet Sentiment Analyzer", layout="wide")
st.title("📊 Tweet Sentiment Analyzer")

# Load animation (cached)
@st.cache_data(show_spinner=False)
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

# MongoDB Config
mongo_uri = "mongodb+srv://biomedicalinformatics100:MyNewSecurePass%2123@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Cached sentiment analyzer
@st.cache_data
def analyze_sentiment(df_raw):
    analyzer = SentimentIntensityAnalyzer()
    df = df_raw.copy()
    df['text'] = df['text'].astype(str)

    def get_sentiment(text):
        score = analyzer.polarity_scores(text)['compound']
        return 'positive' if score >= 0.05 else 'negative' if score <= -0.05 else 'neutral'

    df['Sentiment'] = df['text'].apply(get_sentiment)
    return df

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Analyze Uploaded CSV", "☁️ WordClouds", "📥 Download", 
    "📦 Upload to MongoDB", "📤 Fetch from MongoDB", "📈 Visuals from Fetched Data"
])

# ---- TAB 1: Analysis ----
with tab1:
    if uploaded_file and st.session_state.start_clicked:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()

        if 'text' not in df.columns:
            st.error("❌ The uploaded file must contain a 'Text' column.")
        else:
            df = analyze_sentiment(df)
            st.success("✅ Sentiment analysis completed!")
            st.dataframe(df[['text', 'Sentiment']])

            st.subheader("📊 Sentiment Bar Chart")
            st.bar_chart(df['Sentiment'].value_counts())

            st.subheader("🔎 Filter by Keyword")
            keyword = st.text_input("Keyword:")
            if keyword:
                keyword_df = df[df['text'].str.contains(keyword, case=False, na=False)]
                st.write(f"{len(keyword_df)} tweets match:")
                st.dataframe(keyword_df[['text', 'Sentiment']])
                st.bar_chart(keyword_df['Sentiment'].value_counts())

# ---- TAB 2: WordClouds ----
with tab2:
    if uploaded_file and st.session_state.start_clicked:
        st.subheader("🌥 WordClouds by Sentiment")
        for sentiment in ['positive', 'neutral', 'negative']:
            subset = df[df['Sentiment'] == sentiment]
            text = " ".join(subset['text'].astype(str))
            if text:
                wc = WordCloud(width=800, height=400, background_color='white').generate(text)
                st.markdown(f"#### {sentiment.capitalize()} Tweets")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.warning(f"No {sentiment} tweets available.")

# ---- TAB 3: Download ----
with tab3:
    if uploaded_file and st.session_state.start_clicked:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "sentiment_results.csv", "text/csv")

# ---- TAB 4: Upload to MongoDB ----
with tab4:
    if uploaded_file and st.session_state.start_clicked:
        if st.button("📦 Push to MongoDB"):
            try:
                client = MongoClient(mongo_uri)
                collection = client["sentiment_analysis"]["tweets"]
                upload_df = df[['text', 'Sentiment']].copy()
                upload_df['Timestamp'] = datetime.now()
                collection.insert_many(upload_df.to_dict("records"))
                st.success("✅ Uploaded to MongoDB!")
            except Exception as e:
                st.error(f"❌ MongoDB Upload Error: {e}")

# ---- TAB 5: Fetch from MongoDB ----
with tab5:
    st.subheader("📤 Fetch Tweets from MongoDB")
    if st.button("Fetch Now"):
        try:
            response = requests.get("http://127.0.0.1:5000/fetch", timeout=20)
            if response.status_code == 200:
                fetched_data = response.json()
                st.success(f"✅ Retrieved {len(fetched_data)} tweets")
                st.session_state['mongo_data'] = pd.DataFrame(fetched_data)
                st.dataframe(st.session_state['mongo_data'][['Text', 'Sentiment']])
            else:
                st.error(f"⚠️ Failed with status {response.status_code}")
        except Exception as e:
            st.error(f"❌ Request Error: {e}")

# ---- TAB 6: Visuals from MongoDB ----
with tab6:
    if 'mongo_data' in st.session_state:
        mongo_df = st.session_state['mongo_data'].copy()
        if "Timestamp" in df_mongo.columns:
             df_mongo["Timestamp"] = pd.to_datetime(df_mongo["Timestamp"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M")

        st.subheader("📊 MongoDB Sentiment Bar Chart")
        st.bar_chart(mongo_df['Sentiment'].value_counts())

        if 'Timestamp' in mongo_df.columns:
            st.subheader("📈 MongoDB Sentiment Over Time")
            timeline = mongo_df.groupby([pd.Grouper(key='Timestamp', freq='D'), 'Sentiment']).size().unstack().fillna(0)
            st.line_chart(timeline)
    else:
        st.info("ℹ️ No MongoDB data loaded yet.")
