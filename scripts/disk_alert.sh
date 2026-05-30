#!/bin/bash

# CloudPulse Disk Usage Alert Script
# This script checks disk usage and writes alert status to a log file.

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

ALERT_DIR="/home/ubuntu/cloudpulse-alerts"
ALERT_FILE="$ALERT_DIR/disk_alert.log"
THRESHOLD=80
DATE=$(date +%Y-%m-%d_%H-%M-%S)

mkdir -p "$ALERT_DIR"

DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -ge "$THRESHOLD" ]; then
    echo "$DATE WARNING: Disk usage is ${DISK_USAGE}% which is above threshold ${THRESHOLD}%" >> "$ALERT_FILE"
else
    echo "$DATE OK: Disk usage is ${DISK_USAGE}% which is below threshold ${THRESHOLD}%" >> "$ALERT_FILE"
fi
