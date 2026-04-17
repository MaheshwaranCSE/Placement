#!/bin/bash
# scripts/restore_db.sh
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <path_to_backup.sql.gz>"
  exit 1
fi

BACKUP_FILE=$1
DB_NAME="${POSTGRES_DB:-placement_db}"
DB_USER="${POSTGRES_USER:-placement_user}"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: File $BACKUP_FILE not found."
    exit 1
fi

echo "Warning: This will overwrite the current database."
read -p "Are you sure? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

echo "Dropping and recreating database ${DB_NAME}..."
# Ensure no connections exist
psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${DB_NAME}';" || true
dropdb -U postgres ${DB_NAME} || true
createdb -U postgres -O ${DB_USER} ${DB_NAME}

echo "Restoring from ${BACKUP_FILE}..."
gunzip -c ${BACKUP_FILE} | psql -U ${DB_USER} -d ${DB_NAME}

echo "Restore completed."
