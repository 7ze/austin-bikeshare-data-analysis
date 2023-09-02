from argparse import ArgumentParser
from dotenv import dotenv_values

env_config = dotenv_values(".env")

# flags
NO_OP_FLAG = "-n", "--no-op"
DATA_SOURCE_FLAG = "-s", "--data-source"
DATE_COLUMN_FLAG = "-d", "--date-column"
OUTPUT_TOPIC_FLAG = "-t", "--output-topic"
ROWS_LIMIT_FLAG = "-r", "--rows-limit"
MAX_OFFSET_MINS_FLAG = "-m", "--max-offset-mins"
MAX_SLEEP_SECONDS_FLAG = "-x", "--max-sleep-seconds"
INPUT_TOPIC_FLAG = "-i", "--input-topic"
BIGQUERY_DATASET_FLAG = "-b", "--bigquery-dataset"
PROJECT_ID_FLAG = "-p", "--project-id"

# descriptions
NO_OP_DESC = "dry run, does not perform any operation, purely for debugging"
DATA_SOURCE_DESC = "bigquery table to read from"
DATE_COLUMN_DESC = "date column to transform"
OUTPUT_TOPIC_DESC = "pub/sub topic to publish to"
ROWS_LIMIT_DESC = "number of rows to query from data source"
MAX_OFFSET_MINS_DESC = "maximum offset limit in minutes"
MAX_SLEEP_SECONDS_DESC = "maximum sleep limit in seconds"
INPUT_TOPIC_DESC = "pub/sub topic to read from"
BIGQUERY_DATASET_DESC = "bigquery dataset to write to"
PROJECT_ID_DESC = "project id to use"


def setup_parser_main():
    parser = ArgumentParser(description="austin bikeshare data analysis pipeline")
    parser.add_argument(*NO_OP_FLAG, help=NO_OP_DESC, action="store_true")
    parser.add_argument(
        *INPUT_TOPIC_FLAG,
        type=str,
        default=env_config.get("TOPIC_ID"),
        help=INPUT_TOPIC_DESC,
    )
    parser.add_argument(
        *BIGQUERY_DATASET_FLAG,
        type=str,
        default=env_config.get("BIGQUERY_DATASET"),
        help=BIGQUERY_DATASET_DESC,
    )
    parser.add_argument(
        *PROJECT_ID_FLAG,
        type=str,
        default=env_config.get("PROJECT_ID"),
        help=PROJECT_ID_DESC,
    )
    args = parser.parse_known_args()
    return args


def setup_parser_publisher():
    parser = ArgumentParser(
        description="transforms existing data to simulate real time streaming data"
    )
    parser.add_argument(*NO_OP_FLAG, help=NO_OP_DESC, action="store_true")
    parser.add_argument(
        *DATA_SOURCE_FLAG,
        type=str,
        default=env_config.get("DATA_SOURCE"),
        help=DATA_SOURCE_DESC,
    )
    parser.add_argument(
        *DATE_COLUMN_FLAG,
        type=str,
        default=env_config.get("DATE_COLUMN"),
        help=DATE_COLUMN_DESC,
    )
    parser.add_argument(
        *OUTPUT_TOPIC_FLAG,
        type=str,
        default=env_config.get("TOPIC_ID"),
        help=OUTPUT_TOPIC_DESC,
    )
    parser.add_argument(
        *ROWS_LIMIT_FLAG,
        type=int,
        default=int(env_config.get("ROWS_LIMIT") or 0),
        help=ROWS_LIMIT_DESC,
    )
    parser.add_argument(
        *MAX_OFFSET_MINS_FLAG,
        type=int,
        default=int(env_config.get("MAX_OFFSET_MINS") or 0),
        help=MAX_OFFSET_MINS_DESC,
    )
    parser.add_argument(
        *MAX_SLEEP_SECONDS_FLAG,
        type=int,
        default=int(env_config.get("MAX_SLEEP_SECONDS") or 0),
        help=MAX_SLEEP_SECONDS_DESC,
    )
    args = parser.parse_known_args()
    return args
