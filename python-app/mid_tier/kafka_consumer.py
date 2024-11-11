import uuid
import ast

from kafka import KafkaConsumer

from utils import create_postgres_connection, logger
from config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


def _validate_player_data(data: dict) -> bool:
    """Ensure received data matches expected schema before write"""
    if isinstance(player_id := data.get("player_id"), str):
        try:
            player_id = uuid.UUID(player_id)
        except ValueError:
            return False, "Invalid 'player_id' %s: not a valid UUID string.", player_id

    match_id = data.get("match_id")
    if not isinstance(match_id, int):
        return False, "Invalid 'match_id': must be an integer between 10 and 99."

    new_rating = data.get("new_rating")
    if not isinstance(new_rating, float):
        return False, "Invalid 'new_rating': must be a float between 10.0 and 100.0."

    return True, "Data is valid."


def consume_messages() -> None:
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",  # Start reading from the earliest message if no offset is saved
        enable_auto_commit=False,
        group_id="my_consumer_group",
    )
    logger.info(f"Consuming messages from topic: {KAFKA_TOPIC}")

    try:
        for message in consumer:
            logger.info("Processing message")
            data_dict = ast.literal_eval(message.value.decode("utf-8"))

            is_valid, validation_msg = _validate_player_data(data_dict)
            if not is_valid:
                logger.error(f"Validation failed: {validation_msg}")
                continue

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
                    logger.info(
                        "Inserted %s into PostgreSQL",
                        data_dict["player_id"],
                    )

            consumer.commit()
    except KeyboardInterrupt:
        logger.info("Stopped consuming messages.")
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
