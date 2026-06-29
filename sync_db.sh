#!/bin/bash
set -e

TARGET=${1:-dev}

if [ "$TARGET" != "dev" ] && [ "$TARGET" != "uat" ]; then
  echo "Usage: $0 {dev|uat}"
  exit 1
fi

echo ">>> Dumping data from Main..."
sg docker -c "docker compose exec -T web python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2" > /tmp/seed_sync.json

echo ">>> Copying to $TARGET container..."
if [ "$TARGET" = "uat" ]; then
  sg docker -c "docker compose -p uat cp /tmp/seed_sync.json web:/tmp/seed_sync.json"
  echo ">>> Loading data into UAT..."
  sg docker -c "APP_PORT=8001 DJANGO_DB_PATH=/app/data/uat.sqlite3 docker compose -p uat exec -T web python manage.py loaddata /tmp/seed_sync.json"
else
  sg docker -c "docker compose cp /tmp/seed_sync.json web:/tmp/seed_sync.json"
  echo ">>> Loading data into Dev..."
  sg docker -c "docker compose exec -T web python manage.py loaddata /tmp/seed_sync.json"
fi

echo ">>> Cleaning up..."
rm /tmp/seed_sync.json

echo ">>> Sync completed!"
