#!/bin/bash

# Update VPS with Latest Memory Delete Fixes
# Run this script ON THE VPS (64.227.99.111)

echo "🔄 Updating VPS with Latest Memory Delete Fixes"
echo "=============================================="

# Navigate to the project directory
cd ~/orchestration || { echo "❌ Project directory not found. Please ensure you're in the correct directory."; exit 1; }

# Pull latest changes (if using git)
echo "📥 Pulling latest changes..."
git pull origin main 2>/dev/null || echo "⚠️  Git pull failed or not using git. Continuing..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Clean up unused resources
echo "🧹 Cleaning up unused Docker resources..."
docker system prune -f

# Rebuild and start services
echo "🔨 Rebuilding and starting services with latest fixes..."
docker-compose up -d --build --force-recreate

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Test the delete endpoint
echo "🧪 Testing delete memory endpoint..."
sleep 10

# Get a memory ID to test with
echo "📋 Getting available memories..."
MEMORY_RESPONSE=$(curl -s http://localhost:8000/api/v1/memory/)
echo "Memory list response: $MEMORY_RESPONSE"

# Extract first memory ID for testing
FIRST_MEMORY_ID=$(echo "$MEMORY_RESPONSE" | grep -o '"memory_id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "Testing with memory ID: $FIRST_MEMORY_ID"

if [ -n "$FIRST_MEMORY_ID" ]; then
    echo "🗑️  Testing delete endpoint..."
    DELETE_RESPONSE=$(curl -s -X DELETE "http://localhost:8000/api/v1/memory/$FIRST_MEMORY_ID")
    echo "Delete response: $DELETE_RESPONSE"
    
    if echo "$DELETE_RESPONSE" | grep -q "deleted successfully"; then
        echo "✅ Delete memory endpoint is working correctly!"
    else
        echo "❌ Delete memory endpoint is still not working properly."
        echo "Response: $DELETE_RESPONSE"
    fi
else
    echo "⚠️  No memories found to test delete functionality."
fi

# Check service status
echo "📊 Checking service status..."
docker-compose ps

echo ""
echo "🎉 VPS update completed!"
echo "========================"
echo "✅ Frontend: http://64.227.99.111:3000"
echo "✅ Backend API: http://64.227.99.111:8000"
echo "✅ Memory Delete: Should now work without 'Not Found' errors"
echo ""
echo "🔧 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
echo ""
echo "⚠️  If delete still doesn't work, check the logs:"
echo "   docker-compose logs backend | tail -20"
echo "================================"
