#!/bin/bash

# I PROACTIVE BRICK Orchestration Intelligence - Startup Script

set -e

echo "🚀 Starting I PROACTIVE BRICK Orchestration Intelligence..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Create environment file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating environment file from template..."
    cp backend/env.example backend/.env
    echo "⚠️  Please update backend/.env with your API keys before starting the services."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p data/grafana
mkdir -p data/prometheus

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose pull

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
docker-compose ps

# Display access information
echo ""
echo "✅ I PROACTIVE BRICK Orchestration Intelligence is running!"
echo ""
echo "🌐 Access URLs:"
echo "   Frontend:     http://localhost:3000"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo "   Grafana:      http://localhost:3001 (admin/admin)"
echo "   Prometheus:   http://localhost:9090"
echo ""
echo "📊 Monitoring:"
echo "   View logs:    docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:      docker-compose restart"
echo ""
echo "🔧 Configuration:"
echo "   Update API keys in backend/.env"
echo "   Restart backend: docker-compose restart backend"
echo ""

# Test API endpoint
echo "🧪 Testing API endpoint..."
if curl -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo "✅ API is responding correctly"
else
    echo "⚠️  API may not be ready yet. Please wait a moment and check http://localhost:8000/api/v1/health"
fi

echo "🎉 Setup complete! Happy orchestrating!"
