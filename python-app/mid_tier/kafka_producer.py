import time

from kafka import KafkaProducer

from config.settings import KAFKA_BOOTSTRAP_SERVERS
from utils import logger


def create_kafka_producer(server=KAFKA_BOOTSTRAP_SERVERS) -> KafkaProducer:
    """Connect to Kafka and return a producer instance."""
    for attempt in range(5):
        try:
            producer = KafkaProducer(
                bootstrap_servers=server,
            )
            logger.info("Producer connected to Kafka")
            return producer
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} - Kafka connection failed: {e}")
            time.sleep(10)
    logger.error("Failed to connect to Kafka after multiple attempts.")
    raise SystemExit(1)
