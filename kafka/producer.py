import os
import time
import requests
import json
from kafka import KafkaProducer

API_KEY = os.getenv("COINAPI_KEY")  # Make sure this is set
API_URL = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

headers = {
    'X-CoinAPI-Key': API_KEY
}

while True:
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()

        price_data = {
            "time": data["time"],
            "asset_id_base": data["asset_id_base"],
            "asset_id_quote": data["asset_id_quote"],
            "rate": data["rate"]
        }

        print(f"Sending: {price_data}")
        producer.send('bitcoin_prices', price_data)
        producer.flush()

    except Exception as e:
        print("Error:", e)

    time.sleep(5)  # Wait between fetches
