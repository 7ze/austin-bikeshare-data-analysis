# to-do:

# Bike Usage Analysis:
# Popular Stations and Routes:
# Station Popularity Over Time:
# Ride Patterns by Day of the Week:
# Write to big query table:

import os
import sys
import json
import apache_beam as beam
from datetime import datetime
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from app.subscriber_type import SubscriberTypeCount
from app.subscriber_type import FormatSubscriberType
from app.bigquery import WriteToBigQuery
from utils.logger import setup_logger


class ParseTimestamp(beam.DoFn):
    """Parses the timestamp from the input string into a timestamp object. The
    string is assumed to be formatted as ISO 8601. For example: 2019-01-14T12:34:56.000Z
    """

    def process(self, element):
        ts = element["start_time"]
        element["start_time"] = datetime.fromisoformat(ts).timestamp()
        yield element


def run(pipeline_options, logger, input_topic, bigquery_dataset, project):
    """Runs the pipeline."""
    try:
        pipeline = beam.Pipeline(options=pipeline_options)
        data = (
            pipeline
            | "Read from PubSub" >> beam.io.ReadFromPubSub(topic=input_topic)
            | "Parse data" >> beam.Map(lambda elem: json.loads(elem))
            | "Parse timestamp" >> beam.ParDo(ParseTimestamp())
            | "Add timestamp"
            >> beam.Map(
                lambda elem: beam.window.TimestampedValue(  # pyright: ignore
                    elem, elem["start_time"]
                )
            )
        )

        subscriber_type_count = (  # pyright:ignore # noqa
            data
            | "Extract and find subscriber type count" >> SubscriberTypeCount()
            | "Format subscriber type count" >> beam.ParDo(FormatSubscriberType())
            | "Write results to BigQuery"
            >> WriteToBigQuery(
                "subscriber_type_count",
                bigquery_dataset,
                {
                    "window_start": "STRING",
                    "window_end": "STRING",
                    "subscriber_type": "STRING",
                    "count": "INTEGER",
                    "processing_time": "STRING",
                },
                project,
            )
        )

        result = pipeline.run()
        result.wait_until_finish()
    except KeyboardInterrupt:
        logger.warning("Interrupted.")
        logger.info("Stopping pipeline...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


def main(known_args, options):
    logger = setup_logger()
    logger.info("starting app...")

    pipeline_options = PipelineOptions(options)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True

    input_topic = known_args.input_topic
    project_id = known_args.project_id
    bigquery_dataset = known_args.bigquery_dataset

    if known_args.no_op:
        print("\nNo-op mode enabled. No data will be read and transformed.")
        print("Configuration values are as follows:")
        print("------------------------------------\n")
        print(f"Input Pub/Sub topic:        {input_topic}")
        print(f"Project ID:                 {project_id}\n")
        print(f"Output BigQuery dataset:    {bigquery_dataset}")
        sys.exit(0)

    run(pipeline_options, logger, input_topic, bigquery_dataset, project_id)
    logger.info("exiting app...")
