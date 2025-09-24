#!/bin/bash

# VPS Deployment Script for I PROACTIVE BRICK Orchestration Intelligence
# Ubuntu VPS Deployment with IP: 64.227.99.111

set -e

echo "🚀 VPS DEPLOYMENT SCRIPT"
echo "========================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# VPS Configuration
VPS_IP="64.227.99.111"
VPS_API_URL="http://${VPS_IP}:8000"
VPS_FRONTEND_URL="http://${VPS_IP}:3000"

echo -e "${BLUE}VPS IP: ${VPS_IP}${NC}"
echo -e "${BLUE}API URL: ${VPS_API_URL}${NC}"
echo -e "${BLUE}Frontend URL: ${VPS_FRONTEND_URL}${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command_exists docker; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

if ! command_exists docker-compose; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Create VPS environment file
echo -e "${YELLOW}Creating VPS environment configuration...${NC}"

cat > .env << EOF
# VPS Deployment Environment Variables
VPS_API_URL=${VPS_API_URL}
ENVIRONMENT=production

# Database Configuration
DATABASE_URL=postgresql://brick_user:brick_password@postgres:5432/brick_orchestration
POSTGRES_USER=brick_user
POSTGRES_PASSWORD=brick_password
POSTGRES_DB=brick_orchestration

# Redis Configuration
REDIS_URL=redis://redis:6379

# AI API Keys (Add your actual keys here)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GOOGLE_GEMINI_API_KEY=your-google-gemini-api-key-here

# Security (Change these in production)
SECRET_KEY=your-production-secret-key-change-this
JWT_SECRET_KEY=your-production-jwt-secret-key-change-this

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
ENABLE_METRICS=true

# CORS Origins (VPS specific)
CORS_ORIGINS=http://${VPS_IP}:3000,http://${VPS_IP}:8000,https://${VPS_IP}:3000,https://${VPS_IP}:8000,http://${VPS_IP},https://${VPS_IP}
EOF

echo -e "${GREEN}✅ VPS environment file created${NC}"
echo ""

# Copy HTTP-only nginx config for initial deployment (no SSL required)
echo -e "${YELLOW}Configuring Nginx for HTTP-only deployment...${NC}"
cp nginx/nginx-http-only.conf nginx/nginx.conf

# Stop existing containers
echo -e "${YELLOW}Stopping existing containers...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.vps.yml down --remove-orphans || true

# Remove old images to force rebuild
echo -e "${YELLOW}Removing old images...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.vps.yml down --rmi all --volumes --remove-orphans || true

# Build and start services
echo -e "${YELLOW}Building and starting services...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.vps.yml up --build -d

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 30

# Check service health
echo -e "${YELLOW}Checking service health...${NC}"

# Check backend health
echo "Checking backend health..."
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    docker-compose logs backend
    exit 1
fi

# Check frontend health
echo "Checking frontend health..."
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is healthy${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
    docker-compose logs frontend
    exit 1
fi

# Check database health
echo "Checking database health..."
if docker-compose -f docker-compose.yml -f docker-compose.vps.yml exec postgres pg_isready -U brick_user -d brick_orchestration >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Database is healthy${NC}"
else
    echo -e "${RED}❌ Database health check failed${NC}"
    docker-compose -f docker-compose.yml -f docker-compose.vps.yml logs postgres
    exit 1
fi

# Check Redis health
echo "Checking Redis health..."
if docker-compose -f docker-compose.yml -f docker-compose.vps.yml exec redis redis-cli ping >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis is healthy${NC}"
else
    echo -e "${RED}❌ Redis health check failed${NC}"
    docker-compose -f docker-compose.yml -f docker-compose.vps.yml logs redis
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 VPS DEPLOYMENT COMPLETE!${NC}"
echo ""

# Display service URLs
echo -e "${BLUE}📊 SERVICE URLs:${NC}"
echo -e "${BLUE}Frontend: http://${VPS_IP}:3000${NC}"
echo -e "${BLUE}Backend API: http://${VPS_IP}:8000${NC}"
echo -e "${BLUE}API Documentation: http://${VPS_IP}:8000/docs${NC}"
echo -e "${BLUE}Health Check: http://${VPS_IP}:8000/health${NC}"
echo ""

# Display test commands
echo -e "${BLUE}🧪 TEST COMMANDS:${NC}"
echo "Test API health:"
echo "curl http://${VPS_IP}:8000/health"
echo ""
echo "Test strategic analysis:"
echo "curl -X POST http://${VPS_IP}:8000/api/v1/orchestration/strategic-analysis \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"task_type\": \"strategic_analysis\", \"goal\": \"Test VPS deployment\"}'"
echo ""
echo "Test file upload:"
echo "curl -X POST http://${VPS_IP}:8000/api/v1/memory/upload \\"
echo "  -F 'file=@test.txt' \\"
echo "  -F 'category=test'"
echo ""

# Display container status
echo -e "${BLUE}📋 CONTAINER STATUS:${NC}"
docker-compose -f docker-compose.yml -f docker-compose.vps.yml ps

echo ""
echo -e "${YELLOW}⚠️  IMPORTANT NOTES:${NC}"
echo "1. Make sure your VPS firewall allows ports 3000 and 8000"
echo "2. Add your actual AI API keys to the .env file"
echo "3. Change the SECRET_KEY and JWT_SECRET_KEY in production"
echo "4. Consider setting up SSL certificates for HTTPS"
echo "5. Monitor logs with: docker-compose logs -f [service_name]"
echo ""

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Your application is now running on VPS ${VPS_IP}${NC}"
