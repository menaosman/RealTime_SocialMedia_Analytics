
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud

st.set_page_config(page_title="Tweet Sentiment Analyzer", layout="wide")
st.title("📊 Tweet Sentiment Analyzer")

# ✅ Landing with image in layout
col1, col2 = st.columns([2, 3])
with col1:
    st.markdown("### Welcome to the **Tweet Sentiment Analyzer**! 👋")
    st.markdown("""
Upload your dataset to:

- ✅ Detect sentiment (positive, neutral, negative)
- 🌥 Generate WordClouds
- 📈 Track sentiment trends over time
- 🔍 Filter tweets by keywords
    """)

with col2:
   st.image("https://i.imgur.com/h5wU9Kv.png", use_column_width=True)


start = st.button("🚀 Start Sentiment Analysis")

if start:
    uploaded_file = st.file_uploader("📂 Upload a CSV file with a 'Text' column", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Text' not in df.columns:
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

            df['Sentiment'] = df['Text'].astype(str).apply(get_sentiment)

            st.success("✅ Sentiment analysis completed!")
            st.dataframe(df[['Text', 'Sentiment']])

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Results as CSV", csv, "sentiment_results.csv", "text/csv")

            st.subheader("📈 Sentiment Distribution (Bar Chart)")
            st.bar_chart(df['Sentiment'].value_counts())

            sentiment_filter = st.selectbox("🔍 Filter by Sentiment", ['all', 'positive', 'neutral', 'negative'])
            if sentiment_filter != 'all':
                filtered_df = df[df['Sentiment'] == sentiment_filter]
                st.write(f"Showing {len(filtered_df)} {sentiment_filter} tweets:")
                st.dataframe(filtered_df[['Text', 'Sentiment']])

            st.subheader("🌥 WordClouds by Sentiment")
            for sentiment in ['positive', 'neutral', 'negative']:
                subset = df[df['Sentiment'] == sentiment]
                text = " ".join(subset['Text'].astype(str))
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
                keyword_df = df[df['Text'].str.contains(keyword, case=False, na=False)]
                st.write(f"Found {len(keyword_df)} tweets containing '{keyword}':")
                st.dataframe(keyword_df[['Text', 'Sentiment']])
                st.bar_chart(keyword_df['Sentiment'].value_counts())

            st.subheader("🧮 Sentiment Summary")
            counts = df['Sentiment'].value_counts()
            st.write(counts)

            st.subheader("📊 Sentiment Breakdown (Pie Chart)")
            fig1, ax1 = plt.subplots()
            ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            if 'Timestamp' in df.columns:
                st.subheader("🕒 Sentiment Over Time")
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                timeline = df.groupby([pd.Grouper(key='Timestamp', freq='D'), 'Sentiment']).size().unstack().fillna(0)
                st.line_chart(timeline)
