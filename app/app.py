import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from dotenv import dotenv_values
from utils.logger import setup_logger
import json
import sys
import os

env_config = dotenv_values(".env")


def run(pipeline_options, logger, input_topic):
    try:
        pipeline = beam.Pipeline(options=pipeline_options)
        data = (
            pipeline
            | "Read from PubSub" >> beam.io.ReadFromPubSub(topic=input_topic)
            | "Parse data" >> beam.Map(lambda x: json.loads(x))
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

    input_topic = (
        known_args.input_topic
        if known_args.input_topic is not None
        else env_config.get("TOPIC_ID")
    )

    # todo: implement no-op
    if known_args.no_op:
        print("\nNo-op mode enabled. No data will be read and transformed.")
        print("Configuration values are as follows:")
        print("------------------------------------\n")
        print(f"Input Pub/Sub topic: {input_topic}")
        sys.exit(0)

    run(pipeline_options, logger, input_topic)
    logger.info("exiting app...")


# to-do:
# 1. handle the edge cases where in case of inactivity the pipeline should be
# gracefully shutdown

# Subscriber Type Analysis:
# Popular Stations and Routes:
# Duration Analysis:
# Bike Usage Analysis:
# Time-based Patterns:
# Subscriber Behavior:
# Station Popularity Over Time:
# Subscriber Retention Analysis:
# Bike Availability:
# Subscriber Demographics (If Available):
# Ride Patterns by Day of the Week:

# 2. write to big query table:
# add command line arguments to take in the table id
# update no op mode to print the table id
