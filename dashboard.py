import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import itertools
import os

st.set_page_config(layout="wide")
st.title("📊 Real-Time Social Media Analysis")

# Upload the CSV file
uploaded_file = st.file_uploader("📁 Upload sentimentdataset.csv", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.balloons()

        # Show raw data
        with st.expander("🔍 Show Raw Data"):
            st.dataframe(df.head())

        # Sentiment Distribution
        st.subheader("📊 Sentiment Distribution")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='sentiment', ax=ax)
        ax.set_title("Sentiment Distribution")
        st.pyplot(fig)

        # Word Cloud
        st.subheader("☁️ Word Cloud of Cleaned Text")
        text = " ".join(df["clean_text"].dropna().tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # Top 10 Keywords
        st.subheader("🔑 Top 10 Keywords")
        words = list(itertools.chain(*[t.split() for t in df["clean_text"].dropna()]))
        common_words = Counter(words).most_common(10)
        if common_words:
            words, counts = zip(*common_words)
            fig, ax = plt.subplots()
            ax.bar(words, counts)
            ax.set_title("Top 10 Keywords")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("No keywords found to display.")

    except Exception as e:
        st.error(f"❌ Critical error: {str(e)}")
else:
    st.info("👆 Please upload the sentimentdataset.csv file to get started.")
