#!/bin/bash

echo "🔄 Updating VPS Chat System"
echo "=========================="

VPS_IP="64.227.99.111"

echo "📤 Copying updated chat.py to VPS..."
scp -o StrictHostKeyChecking=no backend/app/api/v1/endpoints/chat.py root@${VPS_IP}:/tmp/chat_updated.py

echo "📤 Copying updated frontend files to VPS..."
scp -o StrictHostKeyChecking=no frontend/src/pages/Chat.js root@${VPS_IP}:/tmp/Chat_updated.js
scp -o StrictHostKeyChecking=no frontend/src/App.js root@${VPS_IP}:/tmp/App_updated.js
scp -o StrictHostKeyChecking=no frontend/src/components/Layout.js root@${VPS_IP}:/tmp/Layout_updated.js

echo "🚀 Deploying on VPS..."
ssh -o StrictHostKeyChecking=no root@${VPS_IP} << 'ENDSSH'
cd ~/orchestration || { echo "❌ Project directory not found"; exit 1; }

echo "🛑 Stopping services..."
docker-compose down

echo "📝 Updating files..."
cp /tmp/chat_updated.py backend/app/api/v1/endpoints/chat.py
cp /tmp/Chat_updated.js frontend/src/pages/Chat.js
cp /tmp/App_updated.js frontend/src/App.js
cp /tmp/Layout_updated.js frontend/src/components/Layout.js

echo "🔨 Rebuilding services..."
docker-compose up -d --build --force-recreate

echo "⏳ Waiting for services..."
sleep 30

echo "🧪 Testing chat endpoint..."
sleep 10
curl -s -X POST http://localhost:8000/api/v1/chat/message \
    -H "Content-Type: application/json" \
    -d '{"message":"Should campaign orchestration use real-time streaming or batch processing?","session_id":"test_vps_update"}' \
    --max-time 10 | head -3

echo "📊 Service status:"
docker-compose ps

echo "✅ VPS chat system updated!"
ENDSSH

echo ""
echo "🎯 Final VPS Test..."
sleep 10
curl -s -X POST http://${VPS_IP}:8000/api/v1/chat/message \
    -H "Content-Type: application/json" \
    -d '{"message":"Should campaign orchestration use real-time streaming or batch processing?","session_id":"test_final"}' \
    --max-time 15 | head -3

echo ""
echo "🎉 VPS Chat System Update Complete!"
echo "Frontend: http://${VPS_IP}:3000/chat"
echo "Backend: http://${VPS_IP}:8000/api/v1/chat/message"
