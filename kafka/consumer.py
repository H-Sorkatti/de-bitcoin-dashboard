import json
from kafka import KafkaConsumer
import psycopg2

consumer = KafkaConsumer(
    'bitcoin_prices',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    database="kestra",
    user="kestra",
    password="k3str4",
    host="localhost",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

#print("Waiting for messages...")

try:
    for message in consumer:
        print(f"Received: {message.value}")

    	# Insert data into the table
        cur.execute("INSERT INTO project_bitcoin (time, asset_id_base, asset_id_quote, rate) VALUES (%s, %s, %s, %s) ON CONFLICT (time) DO NOTHING", (message.value['time'], message.value['asset_id_base'], message.value['asset_id_quote'], message.value['rate']))

     	# Commit the transaction
        conn.commit()

except:
	# Close the cursor and connection
    cur.close()
    conn.close()
