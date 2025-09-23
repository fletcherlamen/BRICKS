#!/bin/bash

# Deploy Chat Fixes to VPS
# This script deploys the latest chat system improvements to the VPS

echo "🚀 Deploying Chat Fixes to VPS (64.227.99.111)"
echo "=============================================="

VPS_IP="64.227.99.111"
VPS_USER="root"

echo "📋 Files to update on VPS:"
echo "• backend/app/api/v1/endpoints/chat.py (improved keyword routing)"
echo "• frontend/src/pages/Chat.js (chat UI)"
echo "• frontend/src/App.js (chat route)"
echo "• frontend/src/components/Layout.js (chat navigation)"
echo ""

# Test VPS connectivity
echo "🔍 Testing VPS connectivity..."
if ! ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_IP} "echo 'VPS connection successful'"; then
    echo "❌ Cannot connect to VPS. Please check:"
    echo "   • SSH key is set up correctly"
    echo "   • VPS is running and accessible"
    echo "   • Firewall allows SSH connections"
    exit 1
fi

echo "✅ VPS connection successful"
echo ""

# Create a temporary directory for the files
TEMP_DIR="/tmp/chat_fixes_$(date +%s)"
mkdir -p "$TEMP_DIR"

echo "📁 Preparing files for deployment..."

# Copy the updated chat endpoint
cp backend/app/api/v1/endpoints/chat.py "$TEMP_DIR/chat.py"
echo "✅ Copied chat.py"

# Copy the chat UI files
cp frontend/src/pages/Chat.js "$TEMP_DIR/Chat.js"
cp frontend/src/App.js "$TEMP_DIR/App.js"
cp frontend/src/components/Layout.js "$TEMP_DIR/Layout.js"
echo "✅ Copied frontend files"

# Create deployment script for VPS
cat > "$TEMP_DIR/deploy_on_vps.sh" << 'EOF'
#!/bin/bash

echo "🔄 Deploying Chat Fixes on VPS..."

# Navigate to project directory
cd ~/orchestration || { echo "❌ Project directory not found"; exit 1; }

# Backup existing files
echo "💾 Creating backups..."
mkdir -p backups/$(date +%Y%m%d_%H%M%S)
cp backend/app/api/v1/endpoints/chat.py backups/$(date +%Y%m%d_%H%M%S)/chat.py.backup 2>/dev/null || true
cp frontend/src/pages/Chat.js backups/$(date +%Y%m%d_%H%M%S)/Chat.js.backup 2>/dev/null || true
cp frontend/src/App.js backups/$(date +%Y%m%d_%H%M%S)/App.js.backup 2>/dev/null || true
cp frontend/src/components/Layout.js backups/$(date +%Y%m%d_%H%M%S)/Layout.js.backup 2>/dev/null || true

# Stop services
echo "🛑 Stopping services..."
docker-compose down

# Update files
echo "📝 Updating files..."
cp /tmp/chat_fixes/chat.py backend/app/api/v1/endpoints/chat.py
cp /tmp/chat_fixes/Chat.js frontend/src/pages/Chat.js
cp /tmp/chat_fixes/App.js frontend/src/App.js
cp /tmp/chat_fixes/Layout.js frontend/src/components/Layout.js

# Rebuild and start services
echo "🔨 Rebuilding and starting services..."
docker-compose up -d --build --force-recreate

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 30

# Test the chat endpoint
echo "🧪 Testing chat endpoint..."
sleep 10

CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat/message \
    -H "Content-Type: application/json" \
    -d '{"message":"Should campaign orchestration use real-time streaming or batch processing?","session_id":"test_vps_deploy"}' \
    --max-time 10)

if echo "$CHAT_RESPONSE" | grep -q "BRICK Development Plan"; then
    echo "✅ Chat endpoint is working correctly with improved routing!"
    echo "Response includes: BRICK Development Plan"
else
    echo "⚠️ Chat endpoint response:"
    echo "$CHAT_RESPONSE" | head -3
fi

# Check service status
echo "📊 Service status:"
docker-compose ps

echo ""
echo "🎉 Chat fixes deployment completed!"
echo "=================================="
echo "✅ Frontend: http://64.227.99.111:3000/chat"
echo "✅ Backend API: http://64.227.99.111:8000/api/v1/chat/message"
echo ""
echo "🔧 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
EOF

chmod +x "$TEMP_DIR/deploy_on_vps.sh"
echo "✅ Created VPS deployment script"

echo ""
echo "🚀 Deploying to VPS..."

# Copy files to VPS
echo "📤 Uploading files to VPS..."
scp -o StrictHostKeyChecking=no "$TEMP_DIR"/* ${VPS_USER}@${VPS_IP}:/tmp/chat_fixes/

# Create directory on VPS and run deployment
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_IP} << 'ENDSSH'
mkdir -p /tmp/chat_fixes
chmod +x /tmp/chat_fixes/deploy_on_vps.sh
/tmp/chat_fixes/deploy_on_vps.sh
ENDSSH

# Clean up temporary files
rm -rf "$TEMP_DIR"
echo "🧹 Cleaned up temporary files"

echo ""
echo "🎯 Testing VPS Chat Endpoint..."
echo "==============================="

# Test the VPS chat endpoint
sleep 10
echo "Testing campaign orchestration message on VPS:"
VPS_CHAT_RESPONSE=$(curl -s -X POST http://${VPS_IP}:8000/api/v1/chat/message \
    -H "Content-Type: application/json" \
    -d '{"message":"Should campaign orchestration use real-time streaming or batch processing?","session_id":"test_vps_final"}' \
    --max-time 15)

if echo "$VPS_CHAT_RESPONSE" | grep -q "BRICK Development Plan"; then
    echo "✅ VPS Chat endpoint is working correctly!"
    echo "✅ Campaign orchestration message now routes to BRICK development"
    echo ""
    echo "Response preview:"
    echo "$VPS_CHAT_RESPONSE" | head -3
else
    echo "⚠️ VPS Chat endpoint response:"
    echo "$VPS_CHAT_RESPONSE" | head -3
    echo ""
    echo "🔧 If there are issues, check VPS logs:"
    echo "   ssh ${VPS_USER}@${VPS_IP}"
    echo "   cd ~/orchestration"
    echo "   docker-compose logs backend | tail -20"
fi

echo ""
echo "🎉 VPS Chat Fixes Deployment Complete!"
echo "====================================="
echo "✅ VPS Chat Interface: http://${VPS_IP}:3000/chat"
echo "✅ VPS Backend API: http://${VPS_IP}:8000/api/v1/chat/message"
echo ""
echo "🧪 Test the chat system with messages like:"
echo "   • 'Should campaign orchestration use real-time streaming or batch processing?'"
echo "   • 'What are the key insights for business growth?'"
echo "   • 'Help me develop a mobile app'"
echo ""
echo "The chat system should now properly route messages to the correct orchestration type!"
