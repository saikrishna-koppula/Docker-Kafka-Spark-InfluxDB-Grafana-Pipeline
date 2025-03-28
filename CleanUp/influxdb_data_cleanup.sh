#!/bin/bash

# Load environment variables from .env file
source ./../.env

# Define variables
INFLUXDB_URL="http://localhost:8086/api/v2/delete"
INFLUXDB_ORG="primary"
BUCKETS=("Data_Bucket")  # List of buckets to clean
START="1970-01-01T00:00:00Z"
STOP="2030-12-31T23:59:59Z"

# Check if the token is loaded
if [ -z "$INFLUX_TOKEN" ]; then
  echo "Error: INFLUXDB_TOKEN not set. Check your .env file."
  exit 1
fi

for BUCKET in "${BUCKETS[@]}"; do
  echo "Deleting data from bucket: $BUCKET"

  curl --request POST "${INFLUXDB_URL}?org=${INFLUXDB_ORG}&bucket=${BUCKET}" \
    --header "Authorization: Token ${INFLUX_TOKEN}" \
    --header "Content-Type: application/json" \
    --data "{
      \"start\": \"${START}\",
      \"stop\": \"${STOP}\"
    }"

  echo "Data deleted from bucket: $BUCKET"
done