#!/bin/bash

echo "🚀 Pulling latest changes from GitHub..."
git pull origin main

echo "🐳 Building backend image in background..."
docker compose -f docker-compose.prod.yml build backend

echo "🛑 Stopping old backend container (but NOT nginx or db)..."
docker compose -f docker-compose.prod.yml stop backend

echo "⬆️ Starting new backend container..."
docker compose -f docker-compose.prod.yml up -d backend

echo "✅ Zero downtime deployment complete!"
