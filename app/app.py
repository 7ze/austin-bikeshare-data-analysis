import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from utils.logger import setup_logger


def run(options):
    logger = setup_logger()
    logger.info("starting app...")

    logger.debug(options)
    pipeline_options = PipelineOptions(options)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=pipeline_options) as pipeline:
        _ = (
            pipeline
            | "Create elements" >> beam.Create(["Hello", "World!"])
            | "Print elements" >> beam.Map(print)
        )

    logger.info("exiting app...")
