#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#           VPS Endpoints & CORS Configuration Script
#           I PROACTIVE BRICK Orchestration Intelligence
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}        VPS Endpoints & CORS Configuration${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Default VPS IP
DEFAULT_VPS_IP="64.227.99.111"
DEFAULT_FRONTEND_PORT="3000"
DEFAULT_BACKEND_PORT="8000"

# Prompt for VPS IP
echo -e "${YELLOW}Enter VPS IP address [default: ${DEFAULT_VPS_IP}]:${NC}"
read -r VPS_IP
VPS_IP=${VPS_IP:-$DEFAULT_VPS_IP}

# Prompt for ports
echo -e "${YELLOW}Enter Frontend port [default: ${DEFAULT_FRONTEND_PORT}]:${NC}"
read -r FRONTEND_PORT
FRONTEND_PORT=${FRONTEND_PORT:-$DEFAULT_FRONTEND_PORT}

echo -e "${YELLOW}Enter Backend port [default: ${DEFAULT_BACKEND_PORT}]:${NC}"
read -r BACKEND_PORT
BACKEND_PORT=${BACKEND_PORT:-$DEFAULT_BACKEND_PORT}

# Prompt for CORS mode
echo ""
echo -e "${YELLOW}CORS Configuration:${NC}"
echo -e "  ${CYAN}1)${NC} Allow all origins (development mode)"
echo -e "  ${CYAN}2)${NC} Restrict to specific origins (production mode)"
echo -e "${YELLOW}Select CORS mode [1]:${NC}"
read -r CORS_MODE
CORS_MODE=${CORS_MODE:-1}

if [ "$CORS_MODE" = "1" ]; then
    CORS_ALLOW_ALL="true"
    echo -e "${GREEN}✓ CORS: Allow all origins${NC}"
else
    CORS_ALLOW_ALL="false"
    echo -e "${GREEN}✓ CORS: Restricted to specific origins${NC}"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Configuration Summary:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${CYAN}VPS IP:${NC}              ${VPS_IP}"
echo -e "  ${CYAN}Frontend Port:${NC}       ${FRONTEND_PORT}"
echo -e "  ${CYAN}Backend Port:${NC}        ${BACKEND_PORT}"
echo -e "  ${CYAN}CORS Mode:${NC}           $([ "$CORS_ALLOW_ALL" = "true" ] && echo "Allow all" || echo "Restricted")"
echo -e "  ${CYAN}Frontend URL:${NC}        http://${VPS_IP}:${FRONTEND_PORT}"
echo -e "  ${CYAN}Backend API URL:${NC}     http://${VPS_IP}:${BACKEND_PORT}"
echo -e "  ${CYAN}VPS Database:${NC}        postgresql://user:password@${VPS_IP}:5432/brick_orchestration"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Confirm
echo -e "${YELLOW}Apply this configuration? [Y/n]:${NC}"
read -r CONFIRM
CONFIRM=${CONFIRM:-Y}

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo -e "${RED}✗ Configuration cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Applying Configuration...${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Update env.unified
echo -e "${CYAN}→ Updating env.unified...${NC}"
if [ -f "env.unified" ]; then
    sed -i "s/^VPS_IP=.*/VPS_IP=${VPS_IP}/" env.unified
    sed -i "s/^VPS_FRONTEND_PORT=.*/VPS_FRONTEND_PORT=${FRONTEND_PORT}/" env.unified
    sed -i "s/^VPS_BACKEND_PORT=.*/VPS_BACKEND_PORT=${BACKEND_PORT}/" env.unified
    sed -i "s/^VPS_DOMAIN=.*/VPS_DOMAIN=${VPS_IP}/" env.unified
    sed -i "s/^CORS_ALLOW_ALL_ORIGINS=.*/CORS_ALLOW_ALL_ORIGINS=${CORS_ALLOW_ALL}/" env.unified
    sed -i "s|^REACT_APP_API_URL=.*|REACT_APP_API_URL=http://${VPS_IP}:${BACKEND_PORT}|" env.unified
    sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql://user:password@${VPS_IP}:5432/brick_orchestration|" env.unified
    echo -e "${GREEN}  ✓ env.unified updated${NC}"
else
    echo -e "${YELLOW}  ! env.unified not found, skipping${NC}"
fi

# Update .env if it exists
if [ -f ".env" ]; then
    echo -e "${CYAN}→ Updating .env...${NC}"
    sed -i "s/^VPS_IP=.*/VPS_IP=${VPS_IP}/" .env
    sed -i "s/^VPS_FRONTEND_PORT=.*/VPS_FRONTEND_PORT=${FRONTEND_PORT}/" .env
    sed -i "s/^VPS_BACKEND_PORT=.*/VPS_BACKEND_PORT=${BACKEND_PORT}/" .env
    sed -i "s/^VPS_DOMAIN=.*/VPS_DOMAIN=${VPS_IP}/" .env
    sed -i "s/^CORS_ALLOW_ALL_ORIGINS=.*/CORS_ALLOW_ALL_ORIGINS=${CORS_ALLOW_ALL}/" .env
    sed -i "s|^REACT_APP_API_URL=.*|REACT_APP_API_URL=http://${VPS_IP}:${BACKEND_PORT}|" .env
    sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql://user:password@${VPS_IP}:5432/brick_orchestration|" .env
    echo -e "${GREEN}  ✓ .env updated${NC}"
fi

# Create/update .env from env.unified if .env doesn't exist
if [ ! -f ".env" ] && [ -f "env.unified" ]; then
    echo -e "${CYAN}→ Creating .env from env.unified...${NC}"
    cp env.unified .env
    echo -e "${GREEN}  ✓ .env created${NC}"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Configuration Applied Successfully!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Ask if user wants to restart services
echo -e "${YELLOW}Restart Docker services to apply changes? [Y/n]:${NC}"
read -r RESTART
RESTART=${RESTART:-Y}

if [[ "$RESTART" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${CYAN}→ Restarting Docker services...${NC}"
    docker compose down
    docker compose up -d --build
    echo ""
    echo -e "${GREEN}✓ Services restarted${NC}"
    echo ""
    echo -e "${CYAN}Waiting for services to be ready...${NC}"
    sleep 10
    
    # Check service health
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Service Status:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Check backend
    if curl -s -f "http://localhost:${BACKEND_PORT}/health" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓ Backend:${NC}  http://localhost:${BACKEND_PORT} (Running)"
    else
        echo -e "  ${RED}✗ Backend:${NC}  http://localhost:${BACKEND_PORT} (Not responding)"
    fi
    
    # Check frontend
    if curl -s -f "http://localhost:${FRONTEND_PORT}" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓ Frontend:${NC} http://localhost:${FRONTEND_PORT} (Running)"
    else
        echo -e "  ${YELLOW}⚠ Frontend:${NC} http://localhost:${FRONTEND_PORT} (Still starting...)"
    fi
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 VPS Configuration Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${CYAN}Access URLs:${NC}"
echo -e "  ${BLUE}→ Frontend:${NC}     http://${VPS_IP}:${FRONTEND_PORT}"
echo -e "  ${BLUE}→ Backend API:${NC}  http://${VPS_IP}:${BACKEND_PORT}"
echo -e "  ${BLUE}→ API Docs:${NC}     http://${VPS_IP}:${BACKEND_PORT}/docs"
echo -e "  ${BLUE}→ VPS Database:${NC} postgresql://user:password@${VPS_IP}:5432/brick_orchestration"
echo ""
echo -e "${CYAN}CORS Configuration:${NC}"
if [ "$CORS_ALLOW_ALL" = "true" ]; then
    echo -e "  ${GREEN}✓ All origins allowed (Development mode)${NC}"
else
    echo -e "  ${YELLOW}⚠ Restricted origins only (Production mode)${NC}"
    echo -e "  ${CYAN}  Allowed origins:${NC}"
    echo -e "    - http://${VPS_IP}:${FRONTEND_PORT}"
    echo -e "    - http://${VPS_IP}:${BACKEND_PORT}"
    echo -e "    - http://localhost:3000"
    echo -e "    - http://localhost:8000"
fi
echo ""
echo -e "${CYAN}VPS Database:${NC}"
echo -e "  ${GREEN}✓ All data persisted to VPS PostgreSQL @ ${VPS_IP}:5432${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

