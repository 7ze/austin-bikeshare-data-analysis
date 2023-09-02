# to-do:

# Subscriber Type Analysis:
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
import json
import sys
import os


def run(pipeline_options, logger, input_topic):
    try:
        pipeline = beam.Pipeline(options=pipeline_options)
        data = (
            pipeline
            | "Read from PubSub" >> beam.io.ReadFromPubSub(topic=input_topic)
            | "Parse data" >> beam.Map(lambda elem: json.loads(elem))
        )

        _ = data | "print data" >> beam.Map(print)

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

    # todo: implement no-op
    if known_args.no_op:
        print("\nNo-op mode enabled. No data will be read and transformed.")
        print("Configuration values are as follows:")
        print("------------------------------------\n")
        print(f"Input Pub/Sub topic: {input_topic}")
        sys.exit(0)

    run(pipeline_options, logger, input_topic)
    logger.info("exiting app...")
