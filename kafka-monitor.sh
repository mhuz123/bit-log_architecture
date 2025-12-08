#!/bin/bash

BOOTSTRAP="kafka:9092"
TOPIC="logs"
INTERVAL=10  # seconds, configurable
SLEEP_TIME=0.1 # seconds for sleep between time checks -> free CPU

total_msgs=0
prev_offset=""
prev_time=$(date +%s)

# Keep track of last offsets per partition
declare -A PARTITION_OFFSETS

echo "Starting Kafka '$TOPIC' throughput monitor (every $INTERVAL seconds)"

while true; do
    current_time=$(date +%s)
    elapsed=$((current_time - prev_time))

    if [ $elapsed -ge $INTERVAL ]; then
        timestamp=$(date '+%H:%M:%S')

        # Get latest offsets for the topic partitions
        latest_offsets=$(kafka-run-class.sh kafka.tools.GetOffsetShell \
            --broker-list $BOOTSTRAP --topic $TOPIC --time -1 2>/dev/null)

        if [ -n "$prev_offset" ]; then
            diff=0

            # Process each partition
            while IFS=: read -r topic partition offset; do
                last_offset=${PARTITION_OFFSETS[$partition]:-0}
                new_msgs=$((offset - last_offset))
                diff=$((diff + new_msgs))
                PARTITION_OFFSETS[$partition]=$offset
            done <<< "$latest_offsets"

            total_msgs=$((total_msgs + diff))

            echo "$timestamp | THROUGHPUT | last interval: $diff | total: $total_msgs"
        fi

        prev_offset="set"  # just to skip first iteration
        prev_time=$current_time
    fi

    sleep $SLEEP_TIME
done
