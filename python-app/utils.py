import logging
import psycopg2

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


from config.settings import (
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
)


def create_postgres_connection() -> psycopg2.extensions.connection:
    """Establish a PostgreSQL connection with automatic cleanup using context manager."""
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        logger.error(f"PostgreSQL connection failed: {e}")
        raise SystemExit(1)


def setup_postgres_table() -> None:
    """Ensure the player_ratings table exists in PostgreSQL."""
    with create_postgres_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS player_ratings (
                player_id UUID PRIMARY KEY,
                match_id INTEGER NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rating DECIMAL(5, 2) NOT NULL
            );

            """
            )
        logger.info("Table setup complete.")


def drop_players_table():
    """Ensure the player_ratings table exists in PostgreSQL."""
    with create_postgres_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE player_ratings;")
        logger.info("Deleted player_ratings table")


def fetch_all_rows():
    """Logs all rows in a database table"""
    with create_postgres_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM player_ratings;")
            rows = cursor.fetchall()
            logger.info("Contents of the player_ratings table:")
            if rows:
                for row in rows:
                    logger.info(row)
            else:
                logger.info("No data found in the player_ratings table.")
