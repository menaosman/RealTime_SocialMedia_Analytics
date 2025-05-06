from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB connection
mongo_uri = "mongodb+srv://biomedicalinformatics100:MyNewSecurePass%2123@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
collection = client["sentiment_analysis"]["tweets"]

@app.route('/fetch', methods=['GET'])
def fetch_tweets():
    try:
        cursor = collection.find({}, {"_id": 0, "Text": 1, "Sentiment": 1, "Timestamp": 1})
        tweets = list(cursor)
        for tweet in tweets:
            if isinstance(tweet.get("Timestamp"), datetime):
                tweet["Timestamp"] = tweet["Timestamp"].isoformat()
        return jsonify(tweets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
