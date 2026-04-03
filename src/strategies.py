import json
import os
import redis
from kafka import KafkaProducer
from interfaces import IOutputStrategy


# 1. STRATEGY: CONSOLE OUTPUT
class ConsoleStrategy(IOutputStrategy):
    def write(self, data: list):
        print(f"[STRATEGY: CONSOLE] Preparing output...")
        print(f"--- DATA PREVIEW (First 3 records) ---")
        for row in data[:3]:
            print(row)
        print(f"---")
        print(f"Status: Successfully displayed {len(data)} objects in terminal.")


# 2. STRATEGY: WRITE TO JSON FILE
class FileStrategy(IOutputStrategy):
    def __init__(self, filename):
        self.filename = filename

    def write(self, data: list):
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)

            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # Get absolute path for clean logging
            full_path = os.path.abspath(self.filename)
            print(f"[STRATEGY: FILE] Initializing write to local storage...")
            print(f"Location: {full_path}")
            print(f"Status: File successfully generated. Rows written: {len(data)}.")
        except Exception as e:
            print(f"Error while writing to file: {e}")


# 3. STRATEGY: WRITE TO REDIS (DOCKER)
class RedisStrategy(IOutputStrategy):
    def write(self, data: list):
        print(f"[STRATEGY: REDIS] Establishing connection to server localhost:6379...")
        try:
            # Connect to Redis
            r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

            # Clear old data before writing (optional)
            # r.flushdb()

            for i, row in enumerate(data):
                # Store as JSON string under a unique key
                r.set(f"fire_inspection_record:{i}", json.dumps(row))

            print(f"Connection: OK")
            print(f"Status: Transaction completed. {len(data)} keys added to Redis.")
        except redis.ConnectionError:
            print(
                f"Critical Error: Failed to connect to Redis. Check if the Docker container is running."
            )
        except Exception as e:
            print(f"Error during Redis operation: {e}")


# 4. STRATEGY: WRITE TO KAFKA (DOCKER)
class KafkaStrategy(IOutputStrategy):
    def write(self, data: list):
        topic_name = "fire_inspections_stream"
        print(f"[STRATEGY: KAFKA] Connecting to message broker localhost:9092...")
        try:
            producer = KafkaProducer(
                bootstrap_servers=["localhost:9092"],
                value_serializer=lambda x: json.dumps(x).encode("utf-8"),
                retries=5,
            )

            for row in data:
                producer.send(topic_name, value=row)

            producer.flush()  # Wait for all messages to be sent
            print(f"Topic: {topic_name}")
            print(f"Status: Data stream successfully sent. Message count: {len(data)}.")
        except Exception as e:
            print(f"Kafka transfer error: {e}. Check service status in Docker Desktop.")
