import os
import pickle
from google.cloud import pubsub_v1
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{give_path_to_your_gcp_credentials_file}"
# Set your Google Cloud project ID and topic name 
project_id = "austin-bikeshare-data-analysis"
topic_name = "austin-bikeshare-data"

# Creting bigquerey.Client instance
client = bigquery.Client()
dataset_id = "bigquery-public-data.austin_bikeshare"
table_id = "bigquery-public-data.austin_bikeshare.bikeshare_trips"
query = f"SELECT * FROM `{table_id}` LIMIT 10"
query_job = client.query(query)
results = query_job.result()

# Create a PublisherClient instance
publisher = pubsub_v1.PublisherClient()

# Format the topic path
topic_path = publisher.topic_path(project_id, topic_name)

# Define the message to publish
for row in results:
    message_data = pickle.dumps(row)
    # Publish the message
    future = publisher.publish(topic_path, message_data)
    print(f"Published message: {message_data}")
    # Wait for the publish to complete
    future.result()
    print("Message published.")
