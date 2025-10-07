#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#           Switch All Endpoints from Localhost to VPS
#           I PROACTIVE BRICK Orchestration Intelligence
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

VPS_IP="64.227.99.111"
BACKEND_PORT="8000"
FRONTEND_PORT="3000"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}        Switching to VPS Endpoints${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}VPS Configuration:${NC}"
echo -e "  ${CYAN}VPS IP:${NC}           ${VPS_IP}"
echo -e "  ${CYAN}Backend Port:${NC}     ${BACKEND_PORT}"
echo -e "  ${CYAN}Frontend Port:${NC}    ${FRONTEND_PORT}"
echo ""
echo -e "${YELLOW}This will update:${NC}"
echo -e "  - All localhost:8000 → ${VPS_IP}:${BACKEND_PORT}"
echo -e "  - All localhost:3000 → ${VPS_IP}:${FRONTEND_PORT}"
echo -e "  - CORS configuration for VPS"
echo -e "  - Environment files"
echo ""
echo -e "${YELLOW}Continue? [Y/n]:${NC}"
read -r CONFIRM
CONFIRM=${CONFIRM:-Y}

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo -e "${RED}✗ Cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Updating Endpoints...${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Update env.unified
echo -e "${CYAN}→ Updating env.unified...${NC}"
if [ -f "env.unified" ]; then
    # Update frontend API URL
    sed -i "s|REACT_APP_API_URL=http://localhost:${BACKEND_PORT}|REACT_APP_API_URL=http://${VPS_IP}:${BACKEND_PORT}|g" env.unified
    sed -i "s|REACT_APP_API_URL=http://127.0.0.1:${BACKEND_PORT}|REACT_APP_API_URL=http://${VPS_IP}:${BACKEND_PORT}|g" env.unified
    
    # Update CORS origins
    sed -i "s|CORS_ORIGINS=.*|CORS_ORIGINS=http://${VPS_IP}:${FRONTEND_PORT},http://${VPS_IP}:${BACKEND_PORT},http://localhost:${FRONTEND_PORT},http://localhost:${BACKEND_PORT}|g" env.unified
    
    echo -e "${GREEN}  ✓ env.unified updated${NC}"
else
    echo -e "${YELLOW}  ! env.unified not found${NC}"
fi

# Update .env if exists
if [ -f ".env" ]; then
    echo -e "${CYAN}→ Updating .env...${NC}"
    sed -i "s|REACT_APP_API_URL=http://localhost:${BACKEND_PORT}|REACT_APP_API_URL=http://${VPS_IP}:${BACKEND_PORT}|g" .env
    sed -i "s|REACT_APP_API_URL=http://127.0.0.1:${BACKEND_PORT}|REACT_APP_API_URL=http://${VPS_IP}:${BACKEND_PORT}|g" .env
    sed -i "s|CORS_ORIGINS=.*|CORS_ORIGINS=http://${VPS_IP}:${FRONTEND_PORT},http://${VPS_IP}:${BACKEND_PORT},http://localhost:${FRONTEND_PORT},http://localhost:${BACKEND_PORT}|g" .env
    echo -e "${GREEN}  ✓ .env updated${NC}"
fi

# Create .env from env.unified if it doesn't exist
if [ ! -f ".env" ] && [ -f "env.unified" ]; then
    echo -e "${CYAN}→ Creating .env from env.unified...${NC}"
    cp env.unified .env
    echo -e "${GREEN}  ✓ .env created${NC}"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Endpoints Updated Successfully!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Show updated configuration
echo -e "${BLUE}Updated Configuration:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if [ -f ".env" ]; then
    echo -e "${CYAN}Frontend API URL:${NC}"
    grep "REACT_APP_API_URL" .env | head -1
    echo -e "${CYAN}CORS Origins:${NC}"
    grep "CORS_ORIGINS" .env | head -1
fi
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Ask to restart services
echo -e "${YELLOW}Restart Docker services to apply changes? [Y/n]:${NC}"
read -r RESTART
RESTART=${RESTART:-Y}

if [[ "$RESTART" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${CYAN}→ Stopping services...${NC}"
    docker compose down
    
    echo -e "${CYAN}→ Rebuilding and starting services...${NC}"
    docker compose up -d --build
    
    echo ""
    echo -e "${GREEN}✓ Services restarted${NC}"
    echo ""
    echo -e "${CYAN}Waiting for services to be ready...${NC}"
    sleep 15
    
    # Check service health
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Service Status:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Check backend
    if curl -s -f "http://localhost:${BACKEND_PORT}/health" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓ Backend:${NC}  http://${VPS_IP}:${BACKEND_PORT} (Running)"
    else
        echo -e "  ${RED}✗ Backend:${NC}  http://${VPS_IP}:${BACKEND_PORT} (Not responding)"
    fi
    
    # Check frontend
    if curl -s -f "http://localhost:${FRONTEND_PORT}" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓ Frontend:${NC} http://${VPS_IP}:${FRONTEND_PORT} (Running)"
    else
        echo -e "  ${YELLOW}⚠ Frontend:${NC} http://${VPS_IP}:${FRONTEND_PORT} (Still starting...)"
    fi
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 VPS Endpoints Configuration Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${CYAN}Access URLs:${NC}"
echo -e "  ${BLUE}→ Frontend:${NC}     http://${VPS_IP}:${FRONTEND_PORT}"
echo -e "  ${BLUE}→ Backend API:${NC}  http://${VPS_IP}:${BACKEND_PORT}"
echo -e "  ${BLUE}→ API Docs:${NC}     http://${VPS_IP}:${BACKEND_PORT}/docs"
echo -e "  ${BLUE}→ VPS Database:${NC} postgresql://user:password@${VPS_IP}:5432/brick_orchestration"
echo ""
echo -e "${CYAN}CORS Configuration:${NC}"
echo -e "  ${GREEN}✓ VPS endpoints added to CORS origins${NC}"
echo -e "  ${GREEN}✓ All requests from VPS frontend will be allowed${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

