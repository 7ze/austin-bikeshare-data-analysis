# to-do:

# Bike Usage Analysis:
# Popular Stations and Routes:
# Station Popularity Over Time:
# Ride Patterns by Day of the Week:
# Write to big query table:

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from utils.logger import setup_logger
from datetime import datetime
import json
import sys
import os


class ParseTimestamp(beam.DoFn):
    """Parses the timestamp from the input string into a timestamp object. The
    string is assumed to be formatted as ISO 8601. For example: 2019-01-14T12:34:56.000Z
    """

    def process(self, element):
        ts = element["start_time"]
        element["start_time"] = datetime.fromisoformat(ts).timestamp()
        yield element


class SubscriberTypeCount(beam.PTransform):
    """Extracts the subscriber type from the input dictionary and outputs a
    tuple of the subscriber type and a count of 1. The count can then be
    aggregated to find the total number of trips by a subscriber type.
    """

    def __init__(self):
        beam.PTransform.__init__(self)
        self.window_duration = 1 * 60  # 1 minute

    def expand(self, pcoll):
        return (
            pcoll
            | "Window into fixed windows"
            >> beam.WindowInto(
                beam.window.FixedWindows(self.window_duration)  # pyright: ignore
            )
            | "Extract subscriber types"
            >> beam.Map(lambda elem: (elem["subscriber_type"], 1))
            | "Count subscriber types" >> beam.CombinePerKey(sum)  # pyright: ignore
        )


class FormatSubscriberType(beam.DoFn):
    """Formats the subscriber type count into a dictionary."""

    def process(self, element, window=beam.DoFn.WindowParam):
        (subscriber_type, count) = element
        start = window.start.to_utc_datetime().isoformat()  # pyright: ignore
        end = window.end.to_utc_datetime().isoformat()  # pyright: ignore
        yield {
            "window_start": start,
            "window_end": end,
            "subscriber_type": subscriber_type,
            "count": count,
            "processing_time": datetime.utcnow().isoformat(),
        }


class WriteToBigQuery(beam.PTransform):
    """Generate, format, and write BigQuery table row information."""

    def __init__(self, table_name, dataset, schema, project):
        """Initializes the transform.
        Args:
            table_name: Name of the BigQuery table to use.
            dataset: Name of the dataset to use.
            schema: Dictionary in the format {'column_name': 'bigquery_type'}
            project: Name of the Cloud project containing BigQuery table.
        """
        beam.PTransform.__init__(self)
        self.table_name = table_name
        self.dataset = dataset
        self.schema = schema
        self.project = project

    def get_schema(self):
        """Build the output table schema."""
        return ", ".join("%s:%s" % (col, self.schema[col]) for col in self.schema)

    def expand(self, pcoll):
        return (
            pcoll
            | "Convert to row"
            >> beam.Map(lambda elem: {col: elem[col] for col in self.schema})
            | beam.io.WriteToBigQuery(
                self.table_name, self.dataset, self.project, self.get_schema()
            )
        )


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
            | "Extract subscriber type trips count" >> SubscriberTypeCount()
            | "Format subscriber type trips count" >> beam.ParDo(FormatSubscriberType())
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
