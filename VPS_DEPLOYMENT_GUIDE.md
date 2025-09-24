# 🚀 VPS Deployment Guide

## Ubuntu VPS Deployment for I PROACTIVE BRICK Orchestration Intelligence

### Prerequisites
- Ubuntu VPS with IP: `64.227.99.111`
- Docker and Docker Compose installed
- Ports 3000, 8000, 80, 443 open in firewall

### Quick Deployment

1. **Clone/Upload the project to your VPS**
```bash
# If using git
git clone <your-repo-url>
cd orchestration

# Or upload the project files via SCP/SFTP
```

2. **Run the deployment script**
```bash
chmod +x vps-deploy.sh
./vps-deploy.sh
```

### Manual Deployment

1. **Set environment variables**
```bash
export VPS_API_URL="http://64.227.99.111:8000"
export ENVIRONMENT="production"
```

2. **Create .env file**
```bash
cat > .env << EOF
VPS_API_URL=http://64.227.99.111:8000
ENVIRONMENT=production
DATABASE_URL=postgresql://brick_user:brick_password@postgres:5432/brick_orchestration
POSTGRES_USER=brick_user
POSTGRES_PASSWORD=brick_password
POSTGRES_DB=brick_orchestration
REDIS_URL=redis://redis:6379
DEBUG=false
LOG_LEVEL=INFO
EOF
```

3. **Deploy with Docker Compose**
```bash
# Stop existing containers
docker-compose down --remove-orphans

# Build and start services
docker-compose up --build -d

# Or use VPS-specific compose file
docker-compose -f docker-compose.vps.yml up --build -d
```

### Service URLs

After deployment, your services will be available at:

- **Frontend**: http://64.227.99.111:3000
- **Backend API**: http://64.227.99.111:8000
- **API Documentation**: http://64.227.99.111:8000/docs
- **Health Check**: http://64.227.99.111:8000/health

### Testing the Deployment

1. **Test API health**
```bash
curl http://64.227.99.111:8000/health
```

2. **Test strategic analysis**
```bash
curl -X POST http://64.227.99.111:8000/api/v1/orchestration/strategic-analysis \
  -H 'Content-Type: application/json' \
  -d '{"task_type": "strategic_analysis", "goal": "Test VPS deployment"}'
```

3. **Test file upload**
```bash
curl -X POST http://64.227.99.111:8000/api/v1/memory/upload \
  -F 'file=@test.txt' \
  -F 'category=test'
```

4. **Test frontend**
```bash
curl http://64.227.99.111:3000
```

### Configuration Updates

The system has been updated with:

✅ **VPS API Endpoints**
- Frontend configured to use VPS API URL
- Backend CORS configured for VPS IP
- Environment variables set for production

✅ **Docker Configuration**
- VPS-specific docker-compose file
- Production environment settings
- Health checks and restart policies

✅ **Nginx Configuration**
- Reverse proxy setup
- CORS handling
- Rate limiting
- SSL support (optional)

### Environment Variables

Key environment variables for VPS deployment:

```bash
VPS_API_URL=http://64.227.99.111:8000
ENVIRONMENT=production
DATABASE_URL=postgresql://brick_user:brick_password@postgres:5432/brick_orchestration
REDIS_URL=redis://redis:6379
DEBUG=false
LOG_LEVEL=INFO
```

### AI API Keys (Optional)

To enable real AI processing, add your API keys:

```bash
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_GEMINI_API_KEY=your-google-gemini-api-key
```

### Monitoring

Check service status:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Troubleshooting

1. **Port conflicts**
```bash
# Check if ports are in use
sudo netstat -tlnp | grep :3000
sudo netstat -tlnp | grep :8000
```

2. **Container issues**
```bash
# Restart specific service
docker-compose restart backend

# Rebuild specific service
docker-compose up --build -d backend
```

3. **Database issues**
```bash
# Check database logs
docker-compose logs postgres

# Connect to database
docker-compose exec postgres psql -U brick_user -d brick_orchestration
```

### Security Considerations

1. **Change default passwords**
2. **Add SSL certificates for HTTPS**
3. **Configure firewall rules**
4. **Set up monitoring and logging**
5. **Regular security updates**

### Next Steps

1. **Add SSL certificates** for HTTPS
2. **Configure domain name** instead of IP
3. **Set up monitoring** (Prometheus, Grafana)
4. **Add backup strategy** for database
5. **Configure log rotation**

---

## 🎯 Quick Start Commands

```bash
# Deploy to VPS
chmod +x vps-deploy.sh
./vps-deploy.sh

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Test deployment
curl http://64.227.99.111:8000/health
```

Your I PROACTIVE BRICK Orchestration Intelligence system is now deployed on Ubuntu VPS! 🚀
