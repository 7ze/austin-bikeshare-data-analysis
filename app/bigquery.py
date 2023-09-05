"""
A helper class which contains the logic to translate the user's custom
dict into a BigQuery table row and then write it to BigQuery.
"""

import apache_beam as beam


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
