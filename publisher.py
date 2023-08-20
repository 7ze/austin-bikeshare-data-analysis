import os
import json
from datetime import datetime
from google.cloud import pubsub_v1
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Administrator/Downloads/austin-bikeshare-data-analysis-6736edcb4391.json"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{give_path_to_your_gcp_credentials_file}"
# Set your Google Cloud project ID and topic name 
project_id = "austin-bikeshare-data-analysis"
topic_name = "austin-bikeshare-data"

# Creting bigquerey.Client instance
client = bigquery.Client()
dataset_id = "bigquery-public-data.austin_bikeshare"
table_id = "bigquery-public-data.austin_bikeshare.bikeshare_trips"
query = f"SELECT * FROM `{table_id}` LIMIT 10"
query_job = client.query(query)
rows = query_job.result()
row = next(rows)

row_dict = dict(row.items())

for key, value in row_dict.items():
    if isinstance(value, datetime):
        row_dict[key] = value.isoformat()

json_data = json.dumps(row_dict, indent=2)
# Create a PublisherClient instance

publisher = pubsub_v1.PublisherClient()

# Format the topic path
topic_path = publisher.topic_path(project_id, topic_name)

future = publisher.publish(topic_path, json_data.encode("utf-8"))
print(f"Published message: {json_data}")
# Wait for the publish to complete
future.result()
print("Message published.")


