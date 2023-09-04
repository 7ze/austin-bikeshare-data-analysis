"""
Pipeline for processing and analyzing data from the Austin Bikeshare System.

This is the entry point of the application. It is used to run the application.
It sets up the pipeline and performs the processing and analysis of the data.
The script supports command-line arguments and configuration via a .env file.

Usage:
    python3 main.py [--input-topic INPUT_TOPIC] [--bigquery-dataset BIGQUERY_DATASET]
                    [--project PROJECT] [--runner RUNNER] [--no-op]

Options:
    --input-topic        Specify the Pub/Sub topic to read from (default from .env)
    --bigquery-dataset   Specify the BigQuery dataset to write to (default from .env)
    --project            Specify the GCP project to use (default from .env)
    --runner             Specify the Beam runner to use (default from .env)
    --no-op              Enable no-op mode to show configuration without running

Note:
    This script utilizes the Google Cloud BigQuery and Pub/Sub APIs, so make sure
    you have the necessary credentials and permissions set up. Configuration
    options can be set in the '.env' file or provided as command-line arguments.
    For details on the required .env variables, refer to the project documentation.
"""

from utils.parser import setup_parser_main
from app import app


if __name__ == "__main__":
    app.main(*setup_parser_main())
