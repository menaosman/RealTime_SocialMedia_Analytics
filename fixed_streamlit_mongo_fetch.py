# Streamlit MongoDB Tweet App with Fix for TLS/SSL

import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

st.set_page_config(page_title="MongoDB Tweet Fetcher", layout="wide")

# MongoDB Atlas URI (⚠️ You can move this to st.secrets later)
mongo_uri = "mongodb+srv://biomedicalinformatics100:MyNewSecurePass%2123@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Tweets Table", "📈 Visual Analytics", "☁️ WordClouds",
    "📤 Download", "📦 MongoDB Upload", "📥 Fetch from MongoDB"
])

with tab6:
    st.subheader("📥 Fetch Tweets from MongoDB Atlas")

    if st.button("Fetch from MongoDB"):
        try:
            # ✅ Fixed TLS + Timeout + Insecure Dev Certificate
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
                    df_mongo["Timestamp"] = pd.to_datetime(df_mongo["Timestamp"], errors="coerce")
                st.dataframe(df_mongo, use_container_width=True)
                st.json(data[:2])  # show sample
            else:
                st.warning("⚠️ No documents found in MongoDB.")

        except Exception as e:
            st.error(f"❌ MongoDB fetch error: {e}")
