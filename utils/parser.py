from argparse import ArgumentParser

# flags
NO_OP_FLAG = "-n"
DATA_SOURCE_FLAG = "-s"
DATE_COLUMN_FLAG = "-d"
OUTPUT_TOPIC_FLAG = "-t"
ROWS_LIMIT_FLAG = "-r"
MAX_OFFSET_MINS_FLAG = "-m"
MAX_SLEEP_SECONDS_FLAG = "-x"
INPUT_TOPIC_FLAG = "-i"

# descriptions
NO_OP_DESC = "dry run, does not perform any operation, purely for debugging"
DATA_SOURCE_DESC = "bigquery table to read from"
DATE_COLUMN_DESC = "date column to transform"
OUTPUT_TOPIC_DESC = "pub/sub topic to publish to"
ROWS_LIMIT_DESC = "number of rows to query from data source"
MAX_OFFSET_MINS_DESC = "maximum offset limit in minutes"
MAX_SLEEP_SECONDS_DESC = "maximum sleep limit in seconds"
INPUT_TOPIC_DESC = "pub/sub topic to read from"


def setup_parser_main():
    parser = ArgumentParser(description="austin bikeshare data analysis pipeline")
    parser.add_argument(NO_OP_FLAG, "--no-op", help=NO_OP_DESC, action="store_true")
    parser.add_argument(INPUT_TOPIC_FLAG, "--input-topic", help=INPUT_TOPIC_DESC)
    args = parser.parse_known_args()
    return args


def setup_parser_publisher():
    parser = ArgumentParser(
        description="transforms existing data to simulate real time streaming data"
    )
    parser.add_argument(NO_OP_FLAG, "--no-op", help=NO_OP_DESC, action="store_true")
    parser.add_argument(DATA_SOURCE_FLAG, "--data-source", help=DATA_SOURCE_DESC)
    parser.add_argument(DATE_COLUMN_FLAG, "--date-column", help=DATE_COLUMN_DESC)
    parser.add_argument(OUTPUT_TOPIC_FLAG, "--output-topic", help=OUTPUT_TOPIC_DESC)
    parser.add_argument(ROWS_LIMIT_FLAG, "--rows-limit", help=ROWS_LIMIT_DESC, type=int)
    parser.add_argument(
        MAX_OFFSET_MINS_FLAG, "--max-offset-mins", help=MAX_OFFSET_MINS_DESC, type=int
    )
    parser.add_argument(
        MAX_SLEEP_SECONDS_FLAG,
        "--max-sleep-seconds",
        help=MAX_SLEEP_SECONDS_DESC,
        type=int,
    )
    args = parser.parse_known_args()
    return args
