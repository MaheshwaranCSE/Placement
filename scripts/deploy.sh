#!/bin/bash
# scripts/deploy.sh
set -e

echo "Pulling latest code..."
git pull origin main

echo "Rebuilding and starting containers..."
docker-compose build
docker-compose up -d

echo "Running migrations..."
docker-compose exec -T web flask db upgrade

echo "Restarting Nginx..."
docker-compose restart nginx

echo "Deployment complete."
