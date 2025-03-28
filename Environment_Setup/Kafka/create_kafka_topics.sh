#!/bin/bash

TOPIC_FILE="/home/Environment_Setup/Kafka/kafka_topics.txt"

if [ ! -f "$TOPIC_FILE" ]; then
  echo "Error: kafka_topics.txt not found!"
  exit 1
fi

echo "Creating topics..."
while IFS= read -r TOPIC || [ -n "$TOPIC" ]; do
  kafka-topics --create --if-not-exists \
    --topic "$TOPIC" \
    --bootstrap-server kafka:9092 \
    --partitions 3 \
    --replication-factor 1
  echo "Created topic: $TOPIC"
done < "$TOPIC_FILE"

echo "All topics created!"

# List all topics in Kafka
echo "Listing all topics in Kafka:"
kafka-topics --bootstrap-server kafka:9092 --list