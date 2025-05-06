# Streamlit MongoDB Tweet App with Fix for Fetch

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

mongo_uri = st.secrets["MONGO_URI"]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Tweets Table", "📈 Visual Analytics", "☁️ WordClouds",
    "📤 Download", "📦 MongoDB Upload", "📥 Fetch from MongoDB"
])
with tab6:
    st.subheader("📥 Fetch Tweets from MongoDB Atlas")

    if st.button("Fetch from MongoDB"):
        try:
            client = MongoClient(
                mongo_uri,
                tls=True,
                tlsAllowInvalidCertificates=True
            )
            collection = client["sentiment_analysis"]["tweets"]
            cursor = collection.find({}, {"_id": 0, "Text": 1, "Sentiment": 1, "Timestamp": 1})

            data = list(cursor)

            if data:
                st.success(f"✅ Retrieved {len(data)} tweets from MongoDB.")
                df_mongo = pd.DataFrame(data)
                if "Timestamp" in df_mongo.columns:
                    df_mongo["Timestamp"] = pd.to_datetime(df_mongo["Timestamp"], errors="coerce")
                st.json(data[:2])
                st.dataframe(df_mongo, use_container_width=True)
            else:
                st.warning("⚠️ No documents found in MongoDB.")
        except Exception as e:
            st.error(f"❌ MongoDB fetch error: {e}")
