#!/bin/bash

BOOTSTRAP="kafka:9092"
TOPIC="logs"
INTERVAL=10  # seconds, configurable

total_msgs=0
prev_offset=""
prev_time=$(date +%s)

echo "Starting Kafka topic '$TOPIC' throughput monitor (every $INTERVAL seconds, infinite)..."
echo "Time | Logs in last $INTERVAL sec | Total logs"

while true; do
    current_time=$(date +%s)
    elapsed=$((current_time - prev_time))

    if [ $elapsed -ge $INTERVAL ]; then
        # Get latest offsets for the topic partitions
        current_offset=$(kafka-run-class.sh kafka.tools.GetOffsetShell \
            --broker-list $BOOTSTRAP --topic $TOPIC --time -1 \
            2>/dev/null | awk -F ":" '{sum+=$3} END {print sum}')

        if [ -n "$prev_offset" ]; then
            diff=$((current_offset - prev_offset))
            total_msgs=$((total_msgs + diff))
            timestamp=$(date '+%H:%M:%S')
            echo "$timestamp | $diff | $total_msgs"
        fi

        prev_offset=$current_offset
        prev_time=$current_time
    fi

    sleep 0.2
done
