from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow access from Streamlit

mongo_uri = "mongodb+srv://biomedicalinformatics100:MyNewSecurePass%2123@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
collection = client["sentiment_analysis"]["tweets"]

@app.route("/tweets", methods=["GET"])
def get_tweets():
    cursor = collection.find({}, {"_id": 0, "Text": 1, "Sentiment": 1, "Timestamp": 1})
    data = list(cursor)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
