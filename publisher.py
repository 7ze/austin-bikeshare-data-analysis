import os
from google.cloud import pubsub_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{Path_Of_GCP_Credentials.json}"
# Set your Google Cloud project ID and topic name
project_id = "austin-bikeshare-data-analysis"
topic_name = "austin-bikeshare-data"

# Create a PublisherClient instance
publisher = pubsub_v1.PublisherClient()

# Format the topic path
topic_path = publisher.topic_path(project_id, topic_name)

# Define the message to publish
message_data = b'Hello, Pub/Sub!'

# Publish the message
future = publisher.publish(topic_path, message_data)
print(f"Published message: {message_data}")

# Wait for the publish to complete
future.result()
print("Message published.")