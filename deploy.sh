#!/bin/bash

# I PROACTIVE BRICK Orchestration Intelligence - VPS Deployment Script
# VPS IP: 64.227.99.111

echo "🚀 Deploying I PROACTIVE BRICK Orchestration Intelligence to VPS..."
echo "=================================================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create production environment file
echo "📝 Creating production environment configuration..."
cat > .env << EOF
# I PROACTIVE BRICK Orchestration Intelligence - Production Environment Variables

# Application Settings
APP_NAME="I PROACTIVE BRICK Orchestration Intelligence"
APP_VERSION="1.0.0"
DEBUG=false
ENVIRONMENT=production

# API Keys - Add your actual keys here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here

# Database Configuration
DATABASE_URL=postgresql://brick_user:brick_password@postgres:5432/brick_orchestration
POSTGRES_USER=brick_user
POSTGRES_PASSWORD=brick_password
POSTGRES_DB=brick_orchestration

# Redis Configuration
REDIS_URL=redis://redis:6379

# CrewAI Configuration
CREWAI_API_KEY=your_crewai_api_key_here
CREWAI_BASE_URL=https://api.crewai.com

# Mem0.ai Configuration
MEM0_API_KEY=your_mem0_api_key_here
MEM0_BASE_URL=https://api.mem0.ai

# Security (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=your-secret-key-change-in-production-$(date +%s)
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production-$(date +%s)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings for VPS (More permissive)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "http://64.227.99.111:3000", "http://64.227.99.111:8000", "https://64.227.99.111:3000", "https://64.227.99.111:8000", "http://64.227.99.111", "https://64.227.99.111", "*"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
EOF

echo "✅ Environment configuration created"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Clean up unused Docker resources
echo "🧹 Cleaning up unused Docker resources..."
docker system prune -f

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build --force-recreate

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service status
echo "📊 Checking service status..."
docker-compose ps

# Test API endpoints
echo "🧪 Testing API endpoints..."
sleep 10

# Test backend health
echo "Testing backend health..."
curl -s http://64.227.99.111:8000/health | head -3

# Test frontend
echo "Testing frontend..."
curl -s http://64.227.99.111:3000 | head -3

echo ""
echo "🎉 Deployment completed!"
echo "=================================================================="
echo "✅ Frontend: http://64.227.99.111:3000"
echo "✅ Backend API: http://64.227.99.111:8000"
echo "✅ API Documentation: http://64.227.99.111:8000/docs"
echo "✅ Enhanced Memory: http://64.227.99.111:3000/enhanced-memory"
echo "✅ UBIC Health: http://64.227.99.111:3000/ubic-health"
echo ""
echo "🔧 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
echo ""
echo "⚠️  Remember to:"
echo "   1. Add your real API keys to the .env file"
echo "   2. Change the SECRET_KEY and JWT_SECRET_KEY"
echo "   3. Configure SSL/HTTPS for production use"
echo "   4. Set up proper firewall rules"
echo "=================================================================="
