
import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Tweet Sentiment Analyzer", layout="wide")
st.title("📊 Tweet Sentiment Analyzer")

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

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results as CSV", csv, "sentiment_results.csv", "text/csv")

        # Show sentiment distribution
        st.subheader("📈 Sentiment Distribution")
        st.bar_chart(df['Sentiment'].value_counts())

        # Filtered view
        sentiment_filter = st.selectbox("🔍 Filter by Sentiment", ['all', 'positive', 'neutral', 'negative'])
        if sentiment_filter != 'all':
            filtered_df = df[df['Sentiment'] == sentiment_filter]
            st.write(f"Showing {len(filtered_df)} {sentiment_filter} tweets:")
            st.dataframe(filtered_df[['Text', 'Sentiment']])
