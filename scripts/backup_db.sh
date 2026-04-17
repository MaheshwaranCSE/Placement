#!/bin/bash
# scripts/backup_db.sh
set -e

BACKUP_DIR="/backup"
DB_NAME="${POSTGRES_DB:-placement_db}"
DB_USER="${POSTGRES_USER:-placement_user}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="placement_${TIMESTAMP}.sql.gz"

mkdir -p ${BACKUP_DIR}

echo "Starting backup of ${DB_NAME}..."
pg_dump -U ${DB_USER} ${DB_NAME} | gzip > ${BACKUP_DIR}/${FILENAME}

# Keep last 30 days
find ${BACKUP_DIR} -name "placement_*.sql.gz" -type f -mtime +30 -delete

echo "Backup completed successfully: ${BACKUP_DIR}/${FILENAME}"

# Optional S3 Upload
if [ -n "$BACKUP_S3_BUCKET" ]; then
    echo "Uploading to S3..."
    # aws s3 cp ${BACKUP_DIR}/${FILENAME} s3://${BACKUP_S3_BUCKET}/
fi
