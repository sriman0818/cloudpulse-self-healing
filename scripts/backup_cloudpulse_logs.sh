#!/bin/bash

# CloudPulse Docker Container Log Backup Script
# This script backs up logs from the cloudpulse-engine Docker container.

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

BACKUP_DIR="/home/ubuntu/cloudpulse-backups"
CONTAINER_NAME="cloudpulse-engine"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

LOG_FILE="$BACKUP_DIR/cloudpulse_logs_$DATE.log"
ARCHIVE_FILE="$BACKUP_DIR/cloudpulse_logs_$DATE.tar.gz"
STATUS_FILE="$BACKUP_DIR/backup_status.log"

mkdir -p "$BACKUP_DIR"

echo "Backup started at $DATE" >> "$STATUS_FILE"

if docker ps --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    docker logs "$CONTAINER_NAME" > "$LOG_FILE" 2>&1

    tar -czf "$ARCHIVE_FILE" "$LOG_FILE"

    rm "$LOG_FILE"

    echo "Backup successful: $ARCHIVE_FILE" >> "$STATUS_FILE"
else
    echo "Backup failed: Container $CONTAINER_NAME is not running" >> "$STATUS_FILE"
fi

find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +7 -delete

echo "Old backups older than 7 days cleaned" >> "$STATUS_FILE"
echo "----------------------------------------" >> "$STATUS_FILE"
