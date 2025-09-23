#!/bin/bash

# Quick VPS Delete Memory Fix
# This script helps you quickly fix the VPS delete memory issue

echo "🔧 Quick VPS Delete Memory Fix"
echo "=============================="

VPS_IP="64.227.99.111"
VPS_USER="root"

echo "This script will help you fix the VPS delete memory issue."
echo "VPS: $VPS_IP"
echo ""

# Function to test VPS delete endpoint
test_vps_delete() {
    echo "🧪 Testing VPS delete endpoint..."
    
    # Get a memory ID
    MEMORY_RESPONSE=$(curl -s http://$VPS_IP:8000/api/v1/memory/)
    FIRST_MEMORY_ID=$(echo "$MEMORY_RESPONSE" | grep -o '"memory_id":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -n "$FIRST_MEMORY_ID" ]; then
        echo "Testing delete with memory ID: $FIRST_MEMORY_ID"
        DELETE_RESPONSE=$(curl -s -X DELETE "http://$VPS_IP:8000/api/v1/memory/$FIRST_MEMORY_ID")
        echo "Delete response: $DELETE_RESPONSE"
        
        if echo "$DELETE_RESPONSE" | grep -q "deleted successfully"; then
            echo "✅ Delete memory endpoint is working!"
            return 0
        else
            echo "❌ Delete memory endpoint is still broken"
            return 1
        fi
    else
        echo "⚠️  No memories found to test"
        return 1
    fi
}

# Test current VPS status
echo "1. Testing current VPS status..."
test_vps_delete

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 VPS delete memory is already working!"
    echo "No fix needed."
    exit 0
fi

echo ""
echo "2. VPS needs to be updated with the latest backend fixes."
echo ""
echo "📋 To fix this, you need to:"
echo ""
echo "Option A - SSH and run update script:"
echo "  ssh $VPS_USER@$VPS_IP"
echo "  cd ~/orchestration"
echo "  ./update_vps.sh"
echo ""
echo "Option B - SSH and manual update:"
echo "  ssh $VPS_USER@$VPS_IP"
echo "  cd ~/orchestration"
echo "  docker-compose down"
echo "  docker-compose up -d --build --force-recreate"
echo "  sleep 30"
echo ""
echo "Option C - Copy fixed files:"
echo "  # Copy these files to VPS:"
echo "  # - backend/app/api/v1/endpoints/memory.py"
echo "  # - backend/app/services/real_orchestrator.py"
echo "  # Then restart: docker-compose restart backend"
echo ""
echo "3. After updating, test again:"
echo "  ./test_vps_delete.sh"
echo ""
echo "📱 VPS URLs:"
echo "  Frontend: http://$VPS_IP:3000"
echo "  Memory Page: http://$VPS_IP:3000/memory"
echo "  Backend: http://$VPS_IP:8000"
echo ""
echo "🔍 The issue is that the VPS backend doesn't have the latest delete memory fixes."
echo "The fix involves updating the memory lookup logic in the delete endpoint."
