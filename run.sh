#!/bin/bash

# Unified Deployment Script for I PROACTIVE BRICK Orchestration Intelligence
# Works for both local development and VPS deployment

set -e

echo "🚀 Starting I PROACTIVE BRICK Orchestration Intelligence..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_header() {
    echo -e "${BLUE}[BRICK]${NC} $1"
}

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

# VPS Configuration - Always use VPS endpoints
VPS_IP="64.227.99.111"
CURRENT_IP=$(hostname -I | awk '{print $1}')

print_header "Configuring for VPS endpoints (64.227.99.111)"
export ENVIRONMENT=production
export DEBUG=false
export REACT_APP_API_URL="http://64.227.99.111:8000"
# Always use VPS database
export DATABASE_URL="postgresql://user:password@64.227.99.111:5432/brick_orchestration"

print_status "Environment: $ENVIRONMENT"
print_status "Debug: $DEBUG"
print_status "API URL: $REACT_APP_API_URL"
print_status "Database URL: $DATABASE_URL"

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down || true

# Remove orphaned containers
print_status "Cleaning up orphaned containers..."
docker-compose down --remove-orphans || true

# Build and start services
print_status "Building and starting services..."
docker-compose up --build -d

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
docker-compose ps

# Show access URLs - VPS endpoints
print_header "🎉 VPS Deployment completed!"
print_status "Frontend: http://64.227.99.111:3000"
print_status "Backend: http://64.227.99.111:8000"
print_status "API Docs: http://64.227.99.111:8000/docs"
print_status "Local Frontend: http://localhost:3000"
print_status "Local Backend: http://localhost:8000"

echo ""
print_status "To view logs: docker-compose logs -f"
print_status "To stop services: docker-compose down"
print_status "To restart services: docker-compose restart"
