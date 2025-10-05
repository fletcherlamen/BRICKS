#!/bin/bash

# VPS Deployment Script for I PROACTIVE BRICK Orchestration Intelligence
# This script deploys the application on Ubuntu VPS with proper database configuration

set -e

echo "🚀 Starting VPS deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on VPS
if [[ $(hostname -I | grep -o '64\.227\.99\.111') ]]; then
    print_status "Running on VPS (64.227.99.111)"
else
    print_warning "This script is designed for VPS deployment. Current IP: $(hostname -I)"
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if PostgreSQL is running on the VPS
print_status "Checking PostgreSQL connection..."
if ! pg_isready -h localhost -p 5432 -U user -d brick_orchestration; then
    print_error "PostgreSQL is not running or not accessible. Please ensure PostgreSQL is running on the VPS."
    exit 1
fi

print_status "PostgreSQL is running and accessible."

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.vps.yml down || true

# Remove orphaned containers
print_status "Cleaning up orphaned containers..."
docker-compose -f docker-compose.vps.yml down --remove-orphans || true

# Build and start services
print_status "Building and starting services..."
docker-compose -f docker-compose.vps.yml up --build -d

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."
sleep 30

# Check service health
print_status "Checking service health..."

# Check backend health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "✅ Backend is healthy"
else
    print_error "❌ Backend health check failed"
fi

# Check frontend health
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_status "✅ Frontend is healthy"
else
    print_error "❌ Frontend health check failed"
fi

# Check database connection
print_status "Checking database connection..."
if curl -f http://localhost:8000/api/v1/database/health > /dev/null 2>&1; then
    print_status "✅ Database connection is healthy"
else
    print_error "❌ Database connection failed"
fi

# Show running containers
print_status "Running containers:"
docker-compose -f docker-compose.vps.yml ps

# Show logs
print_status "Recent logs:"
docker-compose -f docker-compose.vps.yml logs --tail=20

print_status "🎉 VPS deployment completed!"
print_status "Frontend: http://64.227.99.111:3000"
print_status "Backend: http://64.227.99.111:8000"
print_status "API Docs: http://64.227.99.111:8000/docs"

echo ""
print_status "To view logs: docker-compose -f docker-compose.vps.yml logs -f"
print_status "To stop services: docker-compose -f docker-compose.vps.yml down"
print_status "To restart services: docker-compose -f docker-compose.vps.yml restart"
