from kafka import KafkaProducer
import pandas as pd
import time

# Load dataset
df = pd.read_csv("sentimentdataset.csv")

# Set up Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Send each message
for i, row in df.iterrows():
    text = str(row["Text"])
    producer.send("sentiment-topic", value=text.encode('utf-8'))
    print(f"Sent: {text}")
    time.sleep(1)  # Simulate streaming with delay
