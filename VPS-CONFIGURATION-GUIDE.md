# VPS Endpoints & CORS Configuration Guide

## 🎯 Overview

This guide explains how to configure VPS endpoints and CORS settings for **I PROACTIVE BRICK Orchestration Intelligence**.

---

## 📋 Current Configuration

### VPS Database Connection
```
Host: 64.227.99.111
Port: 5432
Database: brick_orchestration
Username: user
Password: password
Connection String: postgresql://user:password@64.227.99.111:5432/brick_orchestration
```

### Service Endpoints
```
Frontend:    http://64.227.99.111:3000
Backend API: http://64.227.99.111:8000
API Docs:    http://64.227.99.111:8000/docs
Health:      http://64.227.99.111:8000/health
```

### CORS Configuration
- **Mode**: Allow all origins (development)
- **Status**: ✅ Enabled for VPS IP and localhost
- **Origins**: All origins (`*`) currently allowed

---

## 🔧 Configuration Methods

### Method 1: Automatic Configuration Script (Recommended)

Run the interactive configuration script:

```bash
./configure-vps-endpoints.sh
```

The script will:
1. Prompt for VPS IP address (default: 64.227.99.111)
2. Prompt for service ports (Frontend: 3000, Backend: 8000)
3. Ask for CORS mode (allow all or restricted)
4. Update configuration files automatically
5. Optionally restart Docker services

### Method 2: Manual Configuration

#### Step 1: Update `env.unified`

Edit the file and update:

```bash
# VPS Configuration
VPS_IP=64.227.99.111
VPS_FRONTEND_PORT=3000
VPS_BACKEND_PORT=8000
VPS_DOMAIN=64.227.99.111

# Database Configuration
DATABASE_URL=postgresql://user:password@64.227.99.111:5432/brick_orchestration

# Frontend API URL
REACT_APP_API_URL=http://64.227.99.111:8000

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS=true
CORS_ORIGINS=http://64.227.99.111:3000,http://64.227.99.111:8000,http://localhost:3000,http://localhost:8000
```

#### Step 2: Copy to .env

```bash
cp env.unified .env
```

#### Step 3: Restart Services

```bash
docker compose down
docker compose up -d --build
```

---

## 🔐 CORS Security Modes

### Development Mode (Current)
```bash
CORS_ALLOW_ALL_ORIGINS=true
```
- ✅ Allows all origins
- ✅ Easy testing and development
- ⚠️ **Not recommended for production**

### Production Mode (Recommended for deployment)
```bash
CORS_ALLOW_ALL_ORIGINS=false
CORS_ORIGINS=http://64.227.99.111:3000,http://64.227.99.111:8000,https://yourdomain.com
```
- ✅ Only specified origins allowed
- ✅ Better security
- ✅ Protects against CSRF attacks

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     VPS Architecture                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend (Port 3000)                                       │
│  http://64.227.99.111:3000                                  │
│           ↓                                                 │
│  Backend API (Port 8000)                                    │
│  http://64.227.99.111:8000                                  │
│           ↓                                                 │
│  VPS PostgreSQL Database (Port 5432)                        │
│  64.227.99.111:5432/brick_orchestration                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Persistence
- ✅ **All data** is saved to VPS database
- ✅ **All data** is loaded from VPS database
- ✅ No local database required

### Supported Operations
- ✅ Chat messages → `chat_messages` table
- ✅ Chat sessions → `chat_sessions` table
- ✅ Orchestration sessions → `orchestration_sessions` table
- ✅ Memory records → `memories` table
- ✅ BRICK proposals → `brick_proposals` table
- ✅ Revenue data → `income_streams`, `brick_ecosystem` tables
- ✅ Strategic data → `brick_ecosystem`, `revenue_opportunities`, `strategic_gaps` tables

---

## 🚀 Deployment Scenarios

### Scenario 1: Local Development with VPS Database (Current)
```
Frontend:  http://localhost:3000 → http://localhost:8000 → VPS DB (64.227.99.111:5432)
Backend:   http://localhost:8000 → VPS DB (64.227.99.111:5432)
Database:  VPS PostgreSQL @ 64.227.99.111:5432
```

**Configuration:**
- `REACT_APP_API_URL=http://localhost:8000`
- `DATABASE_URL=postgresql://user:password@64.227.99.111:5432/brick_orchestration`
- `CORS_ALLOW_ALL_ORIGINS=true`

### Scenario 2: Full VPS Deployment
```
Frontend:  http://64.227.99.111:3000 → http://64.227.99.111:8000 → VPS DB (localhost:5432)
Backend:   http://64.227.99.111:8000 → VPS DB (localhost:5432)
Database:  Local PostgreSQL @ localhost:5432
```

**Configuration:**
- `REACT_APP_API_URL=http://64.227.99.111:8000`
- `DATABASE_URL=postgresql://user:password@localhost:5432/brick_orchestration`
- `CORS_ALLOW_ALL_ORIGINS=false`
- `CORS_ORIGINS=http://64.227.99.111:3000,http://64.227.99.111:8000`

### Scenario 3: Production with Domain
```
Frontend:  https://yourdomain.com → https://api.yourdomain.com → VPS DB
Backend:   https://api.yourdomain.com → VPS DB
Database:  VPS PostgreSQL @ localhost:5432
```

**Configuration:**
- `REACT_APP_API_URL=https://api.yourdomain.com`
- `DATABASE_URL=postgresql://user:password@localhost:5432/brick_orchestration`
- `CORS_ALLOW_ALL_ORIGINS=false`
- `CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`
- `VPS_DOMAIN=yourdomain.com`

---

## 🔍 Testing Configuration

### Test Backend Health
```bash
curl http://64.227.99.111:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Service is running",
  "timestamp": "2025-10-07T..."
}
```

### Test Database Connection
```bash
curl http://64.227.99.111:8000/api/v1/database/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "vps_database": "64.227.99.111:5432"
}
```

### Test CORS Configuration
```bash
curl -H "Origin: http://64.227.99.111:3000" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     http://64.227.99.111:8000/api/v1/health
```

Should return CORS headers if configured correctly.

### Test Frontend API Connection
Open browser console at `http://64.227.99.111:3000` and run:
```javascript
fetch('http://64.227.99.111:8000/api/v1/health')
  .then(r => r.json())
  .then(d => console.log('Backend connected:', d))
```

---

## 🐛 Troubleshooting

### Issue 1: CORS Error in Browser Console

**Symptoms:**
```
Access to fetch at 'http://64.227.99.111:8000/api/v1/...' from origin 
'http://64.227.99.111:3000' has been blocked by CORS policy
```

**Solutions:**
1. **Check CORS_ALLOW_ALL_ORIGINS setting:**
   ```bash
   # In env.unified or .env
   CORS_ALLOW_ALL_ORIGINS=true
   ```

2. **Add origin to CORS_ORIGINS:**
   ```bash
   CORS_ORIGINS=http://64.227.99.111:3000,http://64.227.99.111:8000
   ```

3. **Restart backend:**
   ```bash
   docker compose restart backend
   ```

### Issue 2: Frontend Can't Connect to Backend

**Symptoms:**
- API calls fail with network errors
- Backend health check fails from frontend

**Solutions:**
1. **Check REACT_APP_API_URL:**
   ```bash
   # Should match backend URL
   REACT_APP_API_URL=http://64.227.99.111:8000
   ```

2. **Rebuild frontend to pick up new env vars:**
   ```bash
   docker compose up -d --build frontend
   ```

3. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

### Issue 3: Database Connection Failed

**Symptoms:**
- Backend logs show database connection errors
- Data not loading from VPS database

**Solutions:**
1. **Check DATABASE_URL:**
   ```bash
   DATABASE_URL=postgresql://user:password@64.227.99.111:5432/brick_orchestration
   ```

2. **Test database connection:**
   ```bash
   psql postgresql://user:password@64.227.99.111:5432/brick_orchestration
   ```

3. **Check VPS PostgreSQL is accepting remote connections:**
   - Edit `/etc/postgresql/.../postgresql.conf`: `listen_addresses = '*'`
   - Edit `/etc/postgresql/.../pg_hba.conf`: Add `host all all 0.0.0.0/0 md5`
   - Restart PostgreSQL: `sudo systemctl restart postgresql`

### Issue 4: Environment Variables Not Loading

**Symptoms:**
- Configuration changes not taking effect
- Using old endpoints

**Solutions:**
1. **Ensure .env file exists:**
   ```bash
   cp env.unified .env
   ```

2. **Restart all services:**
   ```bash
   docker compose down
   docker compose up -d --build
   ```

3. **Check environment variables in container:**
   ```bash
   docker compose exec backend env | grep VPS
   docker compose exec frontend env | grep REACT_APP
   ```

---

## 📝 Configuration Files Reference

### Files to Update for VPS Configuration

1. **`env.unified`** - Primary configuration file
   - VPS_IP, VPS_FRONTEND_PORT, VPS_BACKEND_PORT
   - DATABASE_URL
   - REACT_APP_API_URL
   - CORS_ALLOW_ALL_ORIGINS
   - CORS_ORIGINS

2. **`.env`** - Active environment file (copy from env.unified)

3. **`docker-compose.yml`** - Already configured to use .env file

4. **`backend/app/core/config.py`** - Already configured with:
   - Dynamic CORS origins via `get_cors_origins()`
   - VPS configuration support
   - CORS_ORIGINS string parsing

5. **`backend/main.py`** - Already configured with:
   - Dynamic CORS middleware
   - TrustedHostMiddleware with VPS IP
   - Health check endpoint

---

## ✅ Configuration Checklist

Before deploying to VPS, ensure:

- [ ] VPS_IP is set to your VPS IP address
- [ ] DATABASE_URL points to your VPS database
- [ ] REACT_APP_API_URL points to your backend API
- [ ] CORS configuration is appropriate for your deployment
- [ ] Security keys are changed from defaults
- [ ] PostgreSQL is configured to accept connections
- [ ] Firewall allows ports 3000, 8000, and 5432
- [ ] All services restart successfully
- [ ] Health checks pass
- [ ] Frontend can connect to backend
- [ ] Backend can connect to database
- [ ] Data is being saved to VPS database

---

## 🎯 Quick Commands

### View Current Configuration
```bash
cat env.unified | grep -E "(VPS_|CORS_|DATABASE_|REACT_APP_)"
```

### Test All Endpoints
```bash
# Backend health
curl -s http://64.227.99.111:8000/health | jq

# Database health
curl -s http://64.227.99.111:8000/api/v1/database/health | jq

# Frontend (check if serving)
curl -s -o /dev/null -w "%{http_code}" http://64.227.99.111:3000
```

### View Service Logs
```bash
# Backend logs
docker compose logs backend --tail=50

# Frontend logs
docker compose logs frontend --tail=50

# All logs
docker compose logs --tail=50
```

### Restart Services
```bash
# Restart all
docker compose restart

# Restart backend only
docker compose restart backend

# Restart frontend only
docker compose restart frontend

# Full rebuild
docker compose down && docker compose up -d --build
```

---

## 📞 Support

If you encounter issues not covered in this guide:

1. Check Docker logs: `docker compose logs`
2. Verify network connectivity to VPS
3. Ensure PostgreSQL is running on VPS
4. Check firewall rules on VPS
5. Verify environment variables are loaded correctly

---

**Last Updated:** 2025-10-07  
**VPS IP:** 64.227.99.111  
**Database:** PostgreSQL @ 64.227.99.111:5432  
**All Data:** ✅ Persisted to VPS Database

