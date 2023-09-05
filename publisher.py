"""
Real-time Data Simulator for Pub/Sub

This script queries data from a BigQuery dataset and simulates real-time data
by transforming the date column and publishing it to a Pub/Sub topic. The data
is randomly offset to create a time difference. The script supports command-line
arguments and configuration via a .env file.

Usage:
    python3 publisher.py [--data-source DATA_SOURCE] [--date-column DATE_COLUMN]
                  [--rows-limit ROWS_LIMIT] [--max-offset-mins MAX_OFFSET_MINS]
                  [--output-topic OUTPUT_TOPIC] [--max-sleep-seconds MAX_SLEEP_SECONDS] 
                  [--no-op]

Options:
    --data-source        Specify the source BigQuery dataset (default from .env)
    --date-column        Specify the date column to transform (default from .env)
    --output-topic       Specify the Pub/Sub topic to publish to (default from .env)
    --rows-limit         Specify the number of rows to query (default from .env)
    --max-offset-mins    Specify the maximum offset in minutes (default from .env)
    --max-sleep-seconds  Specify the maximum sleep time in seconds (default from .env)
    --no-op              Enable no-op mode to show configuration without publishing

Note:
    This script utilizes the Google Cloud BigQuery and Pub/Sub APIs, so make sure
    you have the necessary credentials and permissions set up. Configuration
    options can be set in the '.env' file or provided as command-line arguments.
    For details on the required .env variables, refer to the project documentation.
"""

from google.cloud import bigquery
from google.cloud import pubsub_v1
from datetime import datetime, timedelta
from utils.parser import setup_parser_publisher
import random
import json
import time
import sys
import os


def sleep_random(max_sleep_seconds):
    try:
        rand_factor = random.randint(1, max_sleep_seconds)
        time.sleep(rand_factor)
        pass
    except Exception as e:
        print(f"Error sleeping: {e}")
        return


def generate_random_offset(offset_mins_limit):
    rand_factor = random.randint(-1, 1)
    offset_minutes = random.randint(0, offset_mins_limit)
    offset = rand_factor * timedelta(minutes=offset_minutes)
    return offset


def fetch_data_from_bigquery(data_source, rows_limit):
    try:
        bigquery_client = bigquery.Client()
        query = f"SELECT * FROM {data_source} LIMIT {rows_limit}"
        query_job = bigquery_client.query(query)
        rows = query_job.result()
        return rows
    except Exception as e:
        print(f"Error fetching data from BigQuery: {e}")
        return []


def transform_and_publish(
    rows, date_column, offset_mins_limit, output_topic, max_sleep_mins
):
    try:
        publisher = pubsub_v1.PublisherClient()
        for row in rows:
            row = dict(row.items())
            offset = generate_random_offset(offset_mins_limit)
            row[date_column] = (datetime.now() + offset).isoformat()
            row = json.dumps(row, indent=4)
            future = publisher.publish(output_topic, row.encode("utf-8"))
            future.result()
            print(row)
            sleep_random(max_sleep_mins)  # sleep randomly to simulate real-time data
            print("Published message to Pub/Sub topic.")

    except KeyboardInterrupt:
        print("Interrupted.")
        print("Stopping publisher...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    except Exception as e:
        print(f"Error transforming and publishing data: {e}")
        return


if __name__ == "__main__":
    (known_args, _) = setup_parser_publisher()
    data_source = known_args.data_source
    date_column = known_args.date_column
    output_topic = known_args.output_topic
    rows_limit = known_args.rows_limit
    max_offset_mins = known_args.max_offset_mins
    max_sleep_seconds = known_args.max_sleep_seconds
    if known_args.no_op:
        print("\nNo-op mode enabled. No data will be published.")
        print("Configuration values are as follows:")
        print("------------------------------------\n")
        print(f"Data source:                            {data_source}")
        print(f"Date column to be transformed:          {date_column}")
        print(f"Pub/Sub topic to publish to:            {output_topic}")
        print(f"Number of rows to be queried:           {rows_limit}")
        print(f"Maximum possible offset in mins:        {max_offset_mins}")
        print(f"Maximum sleep time in seconds:          {max_sleep_seconds}")
        sys.exit(0)
    rows = fetch_data_from_bigquery(data_source, rows_limit)
    transform_and_publish(
        rows, date_column, max_offset_mins, output_topic, max_sleep_seconds
    )
