# Football Stats Data Ingestion MVP

This repository contains a minimal viable product (MVP) for ingesting football statistics data from a mock API,
processing it through a Kafka queue, and storing it in a PostgreSQL database. All services are containerized using
Docker for reproducible setup and execution. Please find my proposal for a complete data architecture (pdf), and data architecture diagrams (png) included in this repository. 

While I ensured to stick to the suggested time limit of this task, I also acknowledge that this repository has multiple areas for improvement - code re-factoring, module re-naming, and including a testing infrastructure will be critical for facilitating contributions, and ensuring robustness to errors.  

## Project Structure

- **docker-compose.yaml**: Configures all services including Zookeeper, Kafka, PostgreSQL, the mock API, and the Python
  data ingestion app which uses kafka topics.

- **mock-api/**: Contains a mock API server that simulates football stats data (runs on port 5001).

  - `football_stats_server.py`: API server script that returns players with score updates.

- **python-app/**: The main ingestion app that consumes data from the API, processes it, and sends it to Kafka and
  PostgreSQL.
  - `app.py`: Entry point for the data ingestion and processing logic.
  - `config/settings.py`: Configuration file with app settings.
  - `mid_tier/kafka_consumer.py` & `mid_tier/kafka_producer.py`: Modules for Kafka integration.

## Prerequisites

Ensure you have **Docker** installed on your system.

## Getting Started

To get the entire stack up and running:

1. Clone this repository.
2. Open a terminal in the project root directory.
3. Start all services with the following command:

   ```bash
   docker-compose up --build
   ```

This command will:

- Start Zookeeper and Kafka for message queuing.
- Start PostgreSQL as the database.
- Start the mock API to simulate football stats data.
- Start the Python app to consume and process data from the mock API.

## Stopping the Services

To stop all running services, press `CTRL+C` in the terminal where `docker-compose` is running, or run:

```bash
docker-compose down
```

## Database Utils

To create or delete the postgresql database, start a python shell within the `python-app` container:

```bash
docker-compose run python-app python
```

Then, import the utils file to use or verify any of the values.

```ipython
>>> import utils
>>> utils.fetch_all_rows()
```
