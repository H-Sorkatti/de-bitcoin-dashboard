import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'bitcoin_prices',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Waiting for messages...")

for message in consumer:
    print(f"Received: {message.value}")
