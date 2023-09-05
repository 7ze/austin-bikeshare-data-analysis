"""
This module contains a pipeline that calculates the number of trips by
subscriber type in a given time window.
"""

import apache_beam as beam
from datetime import datetime

# initialize constants
SUBSCRIBER_TYPE_WINDOW_DURATION = 1 * 60  # 1 minute


class SubscriberTypeCount(beam.PTransform):
    """Extracts the subscriber type from the input dictionary and outputs a
    tuple of the subscriber type and a count of 1. The count can then be
    aggregated to find the total number of trips by a subscriber type.
    """

    def __init__(self):
        beam.PTransform.__init__(self)
        self.window_duration = SUBSCRIBER_TYPE_WINDOW_DURATION

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
