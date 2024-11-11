import threading
import time
import json
import requests
import logging

from mid_tier.kafka_consumer import consume_messages
from mid_tier.kafka_producer import create_kafka_producer
from utils import create_postgres_connection, setup_postgres_table, fetch_all_rows

from config.settings import (
    MOCK_API_URL,
    KAFKA_TOPIC,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def ingest_data(producer, topic=KAFKA_TOPIC):
    """Fetch data from the mock API and send it to Kafka"""
    try:
        # Fetch data from the mock API
        response = requests.get(MOCK_API_URL)
        response.raise_for_status()
        data = response.json()

        # Prepare and publish message
        data_str = json.dumps(data)
        producer.send(topic, data_str.encode("utf-8"))
        producer.flush()  # Ensure all messages are sent

        logger.info(f"Sent data to Kafka: {data_str}")

    except Exception as e:
        logger.error(f"Failed to ingest data: {e}")


def main():
    producer = create_kafka_producer()
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

    with create_postgres_connection() as conn:
        setup_postgres_table(conn)

    counter = 0
    while True:
        ingest_data(producer)
        counter += 1
        time.sleep(5)

        if counter % 5 == 0:
            fetch_all_rows()


if __name__ == "__main__":
    main()