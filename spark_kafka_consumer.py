from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient

# Set up Spark session
spark = SparkSession.builder \
    .appName("KafkaSentimentAnalysis") \
    .getOrCreate()

# Read streaming data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sentiment-topic") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", 100) \
    .load()

# Extract text message from Kafka value
lines = df.selectExpr("CAST(value AS STRING) as text")

# Set up sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

# Register UDF
sentiment_udf = udf(get_sentiment, StringType())
result = lines.withColumn("sentiment", sentiment_udf(lines.text))

# MongoDB setup
mongo_uri = "mongodb+srv://biomedicalinformatics100:biomedicalinformatics100@cluster0.jilvfuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client["TweetDB"]
collection = db["SentimentResults"]

# Write to MongoDB using foreachBatch
def process_batch(batch_df, batch_id):
    records = batch_df.toJSON().map(lambda x: eval(x)).collect()
    if records:
        collection.insert_many(records)

query = result.writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", "output/spark-checkpoint") \
    .start()

query.awaitTermination()
