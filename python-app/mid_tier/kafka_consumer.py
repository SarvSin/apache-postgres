import ast

from kafka import KafkaConsumer

from utils import create_postgres_connection, logger
from config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


def consume_messages():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",  # Start reading from the earliest message if no offset is saved
        enable_auto_commit=True,
        group_id="my_consumer_group",
    )
    logger.info(f"Consuming messages from topic: {KAFKA_TOPIC}")

    try:
        for message in consumer:
            logger.info("Processing message")
            data_dict = ast.literal_eval(message.value.decode("utf-8"))

            with create_postgres_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO player_ratings (player_id, match_id, last_updated, rating) VALUES (%s, %s, %s, %s)",
                        (
                            data_dict["player_id"],
                            data_dict["match_id"],
                            data_dict["timestamp"],
                            data_dict["new_rating"],
                        ),
                    )
                    logger.info("Inserted data into PostgreSQL")
    except KeyboardInterrupt:
        logger.info("Stopped consuming messages.")
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
