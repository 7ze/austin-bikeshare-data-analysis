"""
This module contains a pipeline that calculates the number of trips by
bike type in a given time window.
"""

import apache_beam as beam
from datetime import datetime


# initialize constants
BIKE_TYPE_WINDOW_DURATION = 1 * 60  # 1 minute


class BikeTypeCount(beam.PTransform):
    """Extracts the bike type from the input dictionary and outputs a
    tuple of the bike type and a count of 1. The count can then be
    aggregated to find the total number of trips by a bike type.
    """

    def __init__(self):
        beam.PTransform.__init__(self)
        self.window_duration = BIKE_TYPE_WINDOW_DURATION

    def expand(self, pcoll):
        return (
            pcoll
            | "Window into fixed windows"
            >> beam.WindowInto(
                beam.window.FixedWindows(self.window_duration)  # pyright: ignore
            )
            | "Extract bike types" >> beam.Map(lambda elem: (elem["bike_type"], 1))
            | "Count bike types" >> beam.CombinePerKey(sum)  # pyright: ignore
        )


class FormatBikeType(beam.DoFn):
    """Formats the bike data count into a dictionary."""

    def process(self, element, window=beam.DoFn.WindowParam):
        (bike_type, count) = element
        start = window.start.to_utc_datetime().isoformat()  # pyright: ignore
        end = window.end.to_utc_datetime().isoformat()  # pyright: ignore
        yield {
            "window_start": start,
            "window_end": end,
            "bike_type": bike_type,
            "count": count,
            "processing_time": datetime.utcnow().isoformat(),
        }
