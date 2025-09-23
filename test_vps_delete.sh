#!/bin/bash

# Test VPS Delete Memory Functionality
# Run this script locally to test the VPS delete endpoint

echo "🧪 Testing VPS Delete Memory Functionality"
echo "=========================================="

VPS_IP="64.227.99.111"
VPS_API_URL="http://$VPS_IP:8000"

echo "Testing VPS at: $VPS_API_URL"
echo ""

# Test 1: Check VPS health
echo "1. Testing VPS health..."
HEALTH_RESPONSE=$(curl -s "$VPS_API_URL/health")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ VPS health check passed"
else
    echo "❌ VPS health check failed"
    echo "Response: $HEALTH_RESPONSE"
    exit 1
fi

# Test 2: Get memories list
echo ""
echo "2. Getting memories list..."
MEMORY_RESPONSE=$(curl -s "$VPS_API_URL/api/v1/memory/")
echo "Memory list response:"
echo "$MEMORY_RESPONSE" | head -3

# Extract first memory ID for testing
FIRST_MEMORY_ID=$(echo "$MEMORY_RESPONSE" | grep -o '"memory_id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$FIRST_MEMORY_ID" ]; then
    echo ""
    echo "3. Testing delete endpoint with memory ID: $FIRST_MEMORY_ID"
    
    # Test 3: Delete memory
    DELETE_RESPONSE=$(curl -s -X DELETE "$VPS_API_URL/api/v1/memory/$FIRST_MEMORY_ID")
    echo "Delete response:"
    echo "$DELETE_RESPONSE"
    
    # Check if delete was successful
    if echo "$DELETE_RESPONSE" | grep -q "deleted successfully"; then
        echo "✅ Delete memory endpoint is working correctly!"
        
        # Test 4: Verify deletion
        echo ""
        echo "4. Verifying memory was deleted..."
        sleep 2
        UPDATED_MEMORY_RESPONSE=$(curl -s "$VPS_API_URL/api/v1/memory/")
        UPDATED_COUNT=$(echo "$UPDATED_MEMORY_RESPONSE" | grep -o '"count":[0-9]*' | cut -d':' -f2)
        echo "Updated memory count: $UPDATED_COUNT"
        
        if [ "$UPDATED_COUNT" -lt "$(echo "$MEMORY_RESPONSE" | grep -o '"count":[0-9]*' | cut -d':' -f2)" ]; then
            echo "✅ Memory was successfully deleted!"
        else
            echo "⚠️  Memory count didn't decrease - may need to refresh"
        fi
        
    elif echo "$DELETE_RESPONSE" | grep -q "Not Found"; then
        echo "❌ Delete memory endpoint is still returning 'Not Found'"
        echo "The VPS needs to be updated with the latest backend code."
        echo ""
        echo "🔧 To fix this:"
        echo "1. SSH into the VPS: ssh root@64.227.99.111"
        echo "2. Run the update script: ./update_vps.sh"
        echo "3. Or manually redeploy: docker-compose down && docker-compose up -d --build"
        
    else
        echo "❌ Delete memory endpoint returned unexpected response:"
        echo "$DELETE_RESPONSE"
    fi
    
else
    echo "⚠️  No memories found to test delete functionality."
    echo "Try adding a memory first through the frontend."
fi

echo ""
echo "🎯 Test Summary"
echo "==============="
echo "VPS URL: $VPS_API_URL"
echo "Frontend: http://$VPS_IP:3000"
echo "Memory Page: http://$VPS_IP:3000/memory"
echo ""
echo "If delete still doesn't work, the VPS needs to be updated with the latest backend code."
