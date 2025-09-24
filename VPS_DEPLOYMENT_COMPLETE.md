# 🚀 VPS Deployment Guide - Complete Setup

## VPS Configuration Summary
- **VPS IP**: `64.227.99.111`
- **Frontend URL**: `http://64.227.99.111:3000`
- **Backend API URL**: `http://64.227.99.111:8000`
- **Nginx Proxy**: `http://64.227.99.111:80` (HTTP) / `https://64.227.99.111:443` (HTTPS)

## ✅ Configuration Updates Completed

### 1. **Backend CORS Configuration** ✅
- Updated `backend/app/core/config.py` with VPS-specific CORS origins
- Added all necessary VPS endpoints and ports
- Configured for both HTTP and HTTPS access

### 2. **Docker Compose Configuration** ✅
- Updated `docker-compose.yml` with VPS environment variables
- Enhanced `docker-compose.vps.yml` for production deployment
- Configured proper environment variables and ports

### 3. **Nginx Configuration** ✅
- Created `nginx/nginx.conf` for HTTPS deployment
- Created `nginx/nginx-http-only.conf` for HTTP-only testing
- Configured reverse proxy for frontend and backend
- Added CORS headers and rate limiting

### 4. **Environment Variables** ✅
- Created `env.vps.template` with all VPS-specific settings
- Configured database, Redis, and API endpoints
- Set production environment settings

### 5. **VPS Deployment Script** ✅
- Updated `vps-deploy.sh` with VPS-specific Docker Compose commands
- Added HTTP-only Nginx configuration for initial deployment
- Included comprehensive health checks and testing

## 🚀 Deployment Instructions

### Step 1: Upload Project to VPS
```bash
# From your local machine
scp -r /path/to/orchestration/ user@64.227.99.111:/home/user/
```

### Step 2: SSH into VPS
```bash
ssh user@64.227.99.111
cd /home/user/orchestration
```

### Step 3: Install Docker (if not already installed)
```bash
# Update system
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Log out and back in for group changes
exit
ssh user@64.227.99.111
```

### Step 4: Configure Environment
```bash
# Copy VPS environment template
cp env.vps.template .env

# Edit the .env file with your actual API keys
nano .env
```

### Step 5: Deploy Application
```bash
# Make deployment script executable
chmod +x vps-deploy.sh

# Run deployment
./vps-deploy.sh
```

### Step 6: Configure Firewall
```bash
# Allow necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3000/tcp  # Frontend (direct access)
sudo ufw allow 8000/tcp  # Backend API (direct access)

# Enable firewall
sudo ufw enable
```

## 🧪 Testing Your Deployment

### 1. Health Checks
```bash
# Backend health
curl http://64.227.99.111:8000/health

# Frontend (via Nginx)
curl http://64.227.99.111/

# Direct frontend access
curl http://64.227.99.111:3000
```

### 2. API Testing
```bash
# Strategic analysis
curl -X POST http://64.227.99.111:8000/api/v1/orchestration/strategic-analysis \
  -H "Content-Type: application/json" \
  -d '{"task_type": "strategic_analysis", "goal": "Test VPS deployment"}'

# Memory upload
curl -X POST http://64.227.99.111:8000/api/v1/memory/upload \
  -F "file=@test.txt" \
  -F "category=test"
```

### 3. Frontend Access
- Open browser and navigate to: `http://64.227.99.111:3000`
- Or via Nginx: `http://64.227.99.111`

## 📊 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend (Direct) | http://64.227.99.111:3000 | React application |
| Backend API (Direct) | http://64.227.99.111:8000 | FastAPI backend |
| Frontend (Nginx) | http://64.227.99.111 | Via reverse proxy |
| API Docs | http://64.227.99.111:8000/docs | Swagger documentation |
| Health Check | http://64.227.99.111:8000/health | Service health status |

## 🔧 Management Commands

### Container Management
```bash
# View container status
docker-compose -f docker-compose.yml -f docker-compose.vps.yml ps

# View logs
docker-compose -f docker-compose.yml -f docker-compose.vps.yml logs -f [service_name]

# Restart services
docker-compose -f docker-compose.yml -f docker-compose.vps.yml restart [service_name]

# Stop all services
docker-compose -f docker-compose.yml -f docker-compose.vps.yml down

# Rebuild and start
docker-compose -f docker-compose.yml -f docker-compose.vps.yml up --build -d
```

### Database Management
```bash
# Access PostgreSQL
docker-compose -f docker-compose.yml -f docker-compose.vps.yml exec postgres psql -U brick_user -d brick_orchestration

# Access Redis
docker-compose -f docker-compose.yml -f docker-compose.vps.yml exec redis redis-cli
```

## 🔒 Security Considerations

### 1. **Update API Keys**
- Replace placeholder API keys in `.env` file
- Add your actual OpenAI, Anthropic, and Google API keys

### 2. **Change Default Secrets**
```bash
# Generate secure secrets
openssl rand -hex 32  # For SECRET_KEY
openssl rand -hex 32  # For JWT_SECRET_KEY
```

### 3. **SSL Configuration** (Optional)
- Obtain SSL certificates (Let's Encrypt recommended)
- Update `nginx/nginx.conf` with your certificates
- Enable HTTPS redirect

### 4. **Firewall Rules**
- Only open necessary ports
- Consider using fail2ban for additional security
- Regularly update system packages

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS_ORIGINS in backend configuration
   - Verify frontend is connecting to correct API URL

2. **Container Won't Start**
   - Check logs: `docker-compose logs [service_name]`
   - Verify environment variables in `.env`
   - Ensure ports are not already in use

3. **Database Connection Issues**
   - Verify DATABASE_URL in environment
   - Check if PostgreSQL container is healthy
   - Ensure database credentials match

4. **Frontend Not Loading**
   - Check if REACT_APP_API_URL is correct
   - Verify Nginx configuration
   - Check browser console for errors

### Log Locations
```bash
# Application logs
docker-compose -f docker-compose.yml -f docker-compose.vps.yml logs backend
docker-compose -f docker-compose.yml -f docker-compose.vps.yml logs frontend

# Nginx logs
docker-compose -f docker-compose.yml -f docker-compose.vps.yml logs nginx

# System logs
sudo journalctl -u docker
```

## 📈 Monitoring

### Health Monitoring
- Backend health: `http://64.227.99.111:8000/health`
- Container health: Docker health checks
- System resources: `htop`, `docker stats`

### Performance Monitoring
- Enable metrics: Set `ENABLE_METRICS=true` in `.env`
- Access metrics: `http://64.227.99.111:9090/metrics`
- Monitor logs: `docker-compose logs -f`

## 🎉 Success!

Your I PROACTIVE BRICK Orchestration Intelligence system is now deployed on your Ubuntu VPS!

### Next Steps
1. ✅ Test all endpoints and functionality
2. ✅ Configure your AI API keys for real functionality
3. ✅ Set up SSL certificates for HTTPS
4. ✅ Configure monitoring and alerting
5. ✅ Set up automated backups
6. ✅ Document your deployment for team members

### Support
- Check logs for any issues
- Review the troubleshooting section above
- Ensure all ports are properly configured in firewall
- Verify environment variables are correctly set

**Your VPS deployment is complete and ready for production use! 🚀**
