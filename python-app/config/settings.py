import os
import logging

# Configuration variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = "test_topic"

POSTGRES_DB = os.getenv("POSTGRES_DB", "exampledb")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")

MOCK_API_URL = os.getenv("MOCK_API_URL", "http://mock-api:5001/data")