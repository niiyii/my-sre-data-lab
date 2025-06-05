import os
import time
from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka configuration
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'my-kafka-headless.data-processing.svc.cluster.local:9092')
INPUT_TOPIC = os.getenv('INPUT_TOPIC', 'raw-data')
OUTPUT_TOPIC = os.getenv('OUTPUT_TOPIC', 'processed-data')

# Dummy "data lake" output path (for local testing or mount PVC)
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/tmp/processed_data')

def process_message(message):
    try:
        data = json.loads(message.value.decode('utf-8'))
        # Simple transformation: uppercase a field and add a timestamp
        processed_data = {
            "id": data.get("id"),
            "value_upper": data.get("value", "").upper(),
            "processed_at": time.time()
        }
        print(f"Processed: {processed_data}")
        return json.dumps(processed_data).encode('utf-8')
    except Exception as e:
        print(f"Error processing message: {message.value}. Error: {e}")
        return None

def main():
    print(f"Starting ETL consumer from {INPUT_TOPIC} to {OUTPUT_TOPIC} via {KAFKA_BROKERS}")
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_BROKERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='etl-group'
    )
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)

    for message in consumer:
        processed_msg = process_message(message)
        if processed_msg:
            producer.send(OUTPUT_TOPIC, processed_msg)
            producer.flush()
        else:
            print(f"Skipping failed message: {message.value}")
    consumer.close()
    producer.close()

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    main()