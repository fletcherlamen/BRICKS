#!/bin/bash

# I PROACTIVE BRICK Orchestration Intelligence - Startup Script
# This script sets up and starts the complete MVP system

set -e

echo "🚀 Starting I PROACTIVE BRICK Orchestration Intelligence MVP"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Docker and Docker Compose are available"

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    if [ -f env.example ]; then
        cp env.example .env
        print_warning "Please edit .env file and add your API keys before continuing."
        print_warning "Required API keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_GEMINI_API_KEY"
        read -p "Press Enter after adding your API keys..."
    else
        print_error "env.example file not found. Cannot create .env file."
        exit 1
    fi
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p backend/logs
mkdir -p frontend/build
mkdir -p nginx/ssl

# Build and start services
print_status "Building and starting Docker containers..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 10

# Check if services are running
print_status "Checking service health..."

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U brick_user -d brick_orchestration > /dev/null 2>&1; then
    print_success "PostgreSQL is ready"
else
    print_error "PostgreSQL is not ready"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_success "Redis is ready"
else
    print_error "Redis is not ready"
fi

# Check Backend API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Backend API is ready"
else
    print_warning "Backend API is starting up..."
    sleep 5
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend API is ready"
    else
        print_error "Backend API is not responding"
    fi
fi

# Check Frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend is ready"
else
    print_warning "Frontend is starting up..."
    sleep 5
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend is ready"
    else
        print_error "Frontend is not responding"
    fi
fi

# Display access information
echo ""
echo "🎉 I PROACTIVE BRICK Orchestration Intelligence MVP is ready!"
echo "=========================================================="
echo ""
echo "📊 Dashboard:     http://localhost:3000"
echo "🔗 API Docs:      http://localhost:8000/docs"
echo "💚 Health Check:  http://localhost:8000/health"
echo "📈 Metrics:       http://localhost:8000/metrics"
echo ""
echo "🔧 Services:"
echo "   • Frontend:    React Dashboard"
echo "   • Backend:     FastAPI Orchestration Engine"
echo "   • Database:    PostgreSQL"
echo "   • Cache:       Redis"
echo "   • AI Systems:  CrewAI, Mem0.ai, Multi-Model Router"
echo ""
echo "📋 Quick Commands:"
echo "   • View logs:   docker-compose logs -f"
echo "   • Stop:        docker-compose down"
echo "   • Restart:     docker-compose restart"
echo "   • Shell:       docker-compose exec backend bash"
echo ""
echo "🚀 Ready to orchestrate AI systems for strategic business intelligence!"
echo ""

# Show container status
print_status "Container Status:"
docker-compose ps
