#!/bin/bash

# I PROACTIVE BRICK Orchestration Intelligence - Stop Script

echo "🛑 Stopping I PROACTIVE BRICK Orchestration Intelligence..."

# Stop and remove containers
docker-compose down

# Optional: Remove volumes (uncomment if you want to clear all data)
# echo "🗑️  Removing volumes..."
# docker-compose down -v

echo "✅ All services stopped successfully!"
echo ""
echo "💡 To start again, run: ./scripts/start.sh"
echo "💡 To remove all data, run: docker-compose down -v"
