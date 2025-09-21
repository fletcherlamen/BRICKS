# I PROACTIVE BRICK Orchestration Intelligence - Deployment Guide

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git
- API keys for AI services (OpenAI, Anthropic, Google, Mem0.ai)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd orchestration
./scripts/start.sh
```

### 2. Configure API Keys
Edit `backend/.env` and add your API keys:
```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
MEM0_API_KEY=your_mem0_key_here
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Grafana Monitoring**: http://localhost:3001 (admin/admin)
- **Prometheus Metrics**: http://localhost:9090

## Development Setup

### Backend Development
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Full Development Setup
```bash
./scripts/dev-setup.sh
```

## Architecture Overview

### Services
- **Frontend**: React application with modern UI
- **Backend**: FastAPI with async support
- **Database**: PostgreSQL with async driver
- **Cache**: Redis for session management
- **Reverse Proxy**: Nginx with SSL termination
- **Monitoring**: Prometheus + Grafana

### AI Integration
- **CrewAI**: Multi-agent orchestration
- **Mem0.ai**: Persistent memory and context
- **Multi-model routing**: OpenAI, Anthropic, Google Gemini

## Production Deployment

### Environment Variables
```bash
# Application
DEBUG=false
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
MEM0_API_KEY=...

# Security
SECRET_KEY=your-secret-key
```

### Docker Compose Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
kubectl apply -f k8s/
```

## Monitoring and Observability

### Health Checks
- Backend: `GET /api/v1/health`
- Database: PostgreSQL health check
- Redis: Connection health check

### Metrics
- Prometheus metrics at `/metrics`
- Custom orchestration metrics
- AI collaboration tracking
- Performance monitoring

### Logging
- Structured JSON logging
- Centralized log aggregation
- Error tracking and alerting

## Security

### API Security
- Rate limiting with Nginx
- CORS configuration
- Request validation
- Authentication (JWT)

### Container Security
- Non-root user in containers
- Security scanning with Trivy
- Dependency vulnerability checks
- Secret management

## Backup and Recovery

### Database Backup
```bash
docker exec postgres pg_dump -U postgres brick_orchestration > backup.sql
```

### Restore Database
```bash
docker exec -i postgres psql -U postgres brick_orchestration < backup.sql
```

## Troubleshooting

### Common Issues

1. **Services won't start**
   ```bash
   docker-compose logs [service-name]
   ```

2. **Database connection issues**
   ```bash
   docker-compose exec postgres psql -U postgres -d brick_orchestration
   ```

3. **API not responding**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Reset Everything
```bash
docker-compose down -v
docker system prune -a
./scripts/start.sh
```

## Performance Tuning

### Database Optimization
- Connection pooling
- Query optimization
- Index management
- Memory configuration

### Application Optimization
- Async processing
- Caching strategies
- Load balancing
- Resource limits

## Scaling

### Horizontal Scaling
- Load balancer configuration
- Multiple backend instances
- Database read replicas
- Redis clustering

### Vertical Scaling
- Resource limits in Docker
- Memory and CPU allocation
- Storage optimization
- Network configuration

## Maintenance

### Updates
```bash
git pull origin main
docker-compose pull
docker-compose up -d --build
```

### Database Migrations
```bash
docker-compose exec backend alembic upgrade head
```

### Monitoring Alerts
- High error rates
- Response time degradation
- Resource utilization
- Service availability

## Support

For issues and questions:
1. Check the logs
2. Review the documentation
3. Create an issue in the repository
4. Contact the development team
