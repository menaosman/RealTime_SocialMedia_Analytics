import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Real-Time Social Media Analysis")

try:
    # Verify file exists
    if not os.path.exists("sentimentdataset.csv"):
        st.error("Data file missing! Upload it first")
    else:
        df = pd.read_csv("sentimentdataset.csv")
        st.balloons()  # Visual confirmation it loaded

        # Your dashboard code here
        st.write(df.head())

except Exception as e:
    st.error(f"Critical error: {str(e)}")
    raise e  # Will appear in Colab output
