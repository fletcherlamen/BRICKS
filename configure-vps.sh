#!/bin/bash

# I PROACTIVE BRICK Orchestration Intelligence - VPS Configuration Script
# This script helps you easily configure VPS endpoints and CORS settings

echo "🌐 I PROACTIVE BRICK Orchestration Intelligence - VPS Configuration"
echo "=================================================================="
echo ""

# Function to update environment file
update_env_file() {
    local key=$1
    local value=$2
    local file="env.local"
    
    if grep -q "^${key}=" "$file"; then
        sed -i "s/^${key}=.*/${key}=${value}/" "$file"
        echo "✅ Updated ${key}=${value}"
    else
        echo "${key}=${value}" >> "$file"
        echo "✅ Added ${key}=${value}"
    fi
}

# Function to update docker-compose file
update_docker_compose() {
    local key=$1
    local value=$2
    local file="docker-compose.yml"
    
    if grep -q "${key}=\${${key}:-" "$file"; then
        sed -i "s/${key}=\${${key}:-[^}]*}/${key}=\${${key}:-${value}}/" "$file"
        echo "✅ Updated Docker Compose ${key} default to ${value}"
    fi
}

echo "📋 Current VPS Configuration:"
echo "----------------------------"
echo "VPS IP: $(grep '^VPS_IP=' env.local 2>/dev/null | cut -d'=' -f2 || echo '64.227.99.111')"
echo "Frontend Port: $(grep '^VPS_FRONTEND_PORT=' env.local 2>/dev/null | cut -d'=' -f2 || echo '3000')"
echo "Backend Port: $(grep '^VPS_BACKEND_PORT=' env.local 2>/dev/null | cut -d'=' -f2 || echo '8000')"
echo "HTTP Port: $(grep '^VPS_HTTP_PORT=' env.local 2>/dev/null | cut -d'=' -f2 || echo '80')"
echo "HTTPS Port: $(grep '^VPS_HTTPS_PORT=' env.local 2>/dev/null | cut -d'=' -f2 || echo '443')"
echo "Domain: $(grep '^VPS_DOMAIN=' env.local 2>/dev/null | cut -d'=' -f2 || echo 'your-domain.com')"
echo "CORS Allow All: $(grep '^CORS_ALLOW_ALL_ORIGINS=' env.local 2>/dev/null | cut -d'=' -f2 || echo 'true')"
echo ""

# Interactive configuration
read -p "Would you like to configure VPS settings? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔧 VPS Configuration:"
    echo "===================="
    
    # VPS IP
    read -p "Enter VPS IP address [64.227.99.111]: " vps_ip
    vps_ip=${vps_ip:-64.227.99.111}
    update_env_file "VPS_IP" "$vps_ip"
    
    # Frontend Port
    read -p "Enter VPS Frontend Port [3000]: " frontend_port
    frontend_port=${frontend_port:-3000}
    update_env_file "VPS_FRONTEND_PORT" "$frontend_port"
    
    # Backend Port
    read -p "Enter VPS Backend Port [8000]: " backend_port
    backend_port=${backend_port:-8000}
    update_env_file "VPS_BACKEND_PORT" "$backend_port"
    
    # HTTP Port
    read -p "Enter VPS HTTP Port [80]: " http_port
    http_port=${http_port:-80}
    update_env_file "VPS_HTTP_PORT" "$http_port"
    
    # HTTPS Port
    read -p "Enter VPS HTTPS Port [443]: " https_port
    https_port=${https_port:-443}
    update_env_file "VPS_HTTPS_PORT" "$https_port"
    
    # Domain
    read -p "Enter VPS Domain [your-domain.com]: " domain
    domain=${domain:-your-domain.com}
    update_env_file "VPS_DOMAIN" "$domain"
    
    # Database URL
    read -p "Update database URL with new VPS IP? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter database user [user]: " db_user
        db_user=${db_user:-user}
        read -p "Enter database password [password]: " db_password
        db_password=${db_password:-password}
        read -p "Enter database name [brick_orchestration]: " db_name
        db_name=${db_name:-brick_orchestration}
        read -p "Enter database port [5432]: " db_port
        db_port=${db_port:-5432}
        
        database_url="postgresql://${db_user}:${db_password}@${vps_ip}:${db_port}/${db_name}"
        update_env_file "DATABASE_URL" "$database_url"
        update_env_file "POSTGRES_USER" "$db_user"
        update_env_file "POSTGRES_PASSWORD" "$db_password"
        update_env_file "POSTGRES_DB" "$db_name"
    fi
    
    echo ""
    echo "🔒 CORS Configuration:"
    echo "====================="
    read -p "Allow all CORS origins? (y/n) [y]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        update_env_file "CORS_ALLOW_ALL_ORIGINS" "false"
        echo "✅ CORS restricted to configured origins only"
    else
        update_env_file "CORS_ALLOW_ALL_ORIGINS" "true"
        echo "✅ CORS allows all origins"
    fi
    
    echo ""
    echo "🔄 Frontend Configuration:"
    echo "========================="
    read -p "Update frontend API URL to use VPS? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        api_url="http://${vps_ip}:${backend_port}"
        update_env_file "REACT_APP_API_URL" "$api_url"
        echo "✅ Frontend will use VPS API: $api_url"
    else
        update_env_file "REACT_APP_API_URL" "http://localhost:8000"
        echo "✅ Frontend will use local API: http://localhost:8000"
    fi
    
    echo ""
    echo "✅ VPS Configuration Complete!"
    echo ""
    echo "📊 New Configuration Summary:"
    echo "============================"
    echo "VPS IP: $vps_ip"
    echo "Frontend Port: $frontend_port"
    echo "Backend Port: $backend_port"
    echo "HTTP Port: $http_port"
    echo "HTTPS Port: $https_port"
    echo "Domain: $domain"
    echo "CORS Allow All: $(grep '^CORS_ALLOW_ALL_ORIGINS=' env.local | cut -d'=' -f2)"
    echo "Frontend API URL: $(grep '^REACT_APP_API_URL=' env.local | cut -d'=' -f2)"
    echo ""
    
    read -p "Restart Docker containers to apply changes? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 Restarting Docker containers..."
        docker compose restart
        echo "✅ Docker containers restarted!"
    fi
    
else
    echo ""
    echo "ℹ️  VPS configuration skipped."
    echo "You can run this script again anytime to configure VPS settings."
fi

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Test the configuration:"
echo "   curl http://localhost:8000/api/v1/health"
echo ""
echo "2. Check CORS origins:"
echo "   curl http://localhost:8000/api/v1/database/health"
echo ""
echo "3. View API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "4. Access the frontend:"
echo "   http://localhost:3000"
echo ""
echo "Happy configuring! 🚀"
