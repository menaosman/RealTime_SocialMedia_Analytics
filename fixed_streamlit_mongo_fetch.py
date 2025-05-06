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

mongo_uri = "mongodb+srv://biomedicalinformatics100:MyNewSecurePass%2123@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Dummy for layout simulation
# Create tabs first
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Tweets Table", "📈 Visual Analytics", "☁️ WordClouds",
    "📤 Download", "📦 MongoDB Upload", "📥 Fetch from MongoDB"
])




with tab6:
    st.subheader("📥 Fetch Tweets from MongoDB Atlas")

    if st.button("Fetch from MongoDB"):
        try:
            client = MongoClient(mongo_uri)
            collection = client["sentiment_analysis"]["tweets"]
            documents = list(collection.find({}, {"_id": 0, "Text": 1, "Sentiment": 1, "Timestamp": 1}))

            if not documents:
                st.warning("⚠️ No documents found in MongoDB.")
            else:
                st.success(f"✅ Retrieved {len(documents)} tweets from MongoDB.")

                # Show raw preview
                st.markdown("### 🧾 Sample Raw Records")
                st.json(documents[:2])

                # Create DataFrame
                df_mongo = pd.DataFrame(documents)

                # Convert Timestamp
                if "Timestamp" in df_mongo.columns:
                    df_mongo["Timestamp"] = pd.to_datetime(df_mongo["Timestamp"], errors="coerce")

                st.markdown("### 📋 MongoDB Tweet Records")
                st.dataframe(df_mongo, use_container_width=True)

        except Exception as e:
            st.error(f"❌ MongoDB Fetch Error: {e}")

