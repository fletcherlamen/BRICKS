#!/bin/bash

# I PROACTIVE BRICK Orchestration Intelligence - AI Services Setup
# This script helps configure real AI services for the orchestration system

echo "🤖 I PROACTIVE BRICK Orchestration Intelligence - AI Services Setup"
echo "=================================================================="
echo ""

# Check if env.local exists
if [ ! -f "env.local" ]; then
    echo "❌ env.local file not found. Please run this script from the project root."
    exit 1
fi

echo "📋 Current AI Service Configuration:"
echo "-----------------------------------"

# Check current API keys
if grep -q "OPENAI_API_KEY=your_openai_api_key_here" env.local; then
    echo "❌ OpenAI API Key: Not configured"
else
    echo "✅ OpenAI API Key: Configured"
fi

if grep -q "ANTHROPIC_API_KEY=your_anthropic_api_key_here" env.local; then
    echo "❌ Anthropic API Key: Not configured"
else
    echo "✅ Anthropic API Key: Configured"
fi

if grep -q "GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here" env.local; then
    echo "❌ Google Gemini API Key: Not configured"
else
    echo "✅ Google Gemini API Key: Configured"
fi

echo ""
echo "🔧 To enable real AI services, you need to:"
echo "1. Get API keys from the respective providers:"
echo "   - OpenAI: https://platform.openai.com/api-keys"
echo "   - Anthropic: https://console.anthropic.com/"
echo "   - Google AI: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Update env.local with your actual API keys:"
echo "   OPENAI_API_KEY=sk-your-actual-openai-key"
echo "   ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key"
echo "   GOOGLE_GEMINI_API_KEY=your-actual-google-key"
echo ""
echo "3. Restart the Docker containers:"
echo "   docker compose restart backend"
echo ""

# Interactive setup
read -p "Would you like to configure API keys now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔑 API Key Configuration:"
    echo "========================"
    
    # OpenAI API Key
    read -p "Enter your OpenAI API Key (or press Enter to skip): " openai_key
    if [ ! -z "$openai_key" ]; then
        sed -i "s/OPENAI_API_KEY=your_openai_api_key_here/OPENAI_API_KEY=$openai_key/" env.local
        echo "✅ OpenAI API Key configured"
    fi
    
    # Anthropic API Key
    read -p "Enter your Anthropic API Key (or press Enter to skip): " anthropic_key
    if [ ! -z "$anthropic_key" ]; then
        sed -i "s/ANTHROPIC_API_KEY=your_anthropic_api_key_here/ANTHROPIC_API_KEY=$anthropic_key/" env.local
        echo "✅ Anthropic API Key configured"
    fi
    
    # Google Gemini API Key
    read -p "Enter your Google Gemini API Key (or press Enter to skip): " google_key
    if [ ! -z "$google_key" ]; then
        sed -i "s/GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here/GOOGLE_GEMINI_API_KEY=$google_key/" env.local
        echo "✅ Google Gemini API Key configured"
    fi
    
    echo ""
    echo "🔄 Restarting backend to apply changes..."
    docker compose restart backend
    
    echo ""
    echo "✅ AI Services setup complete!"
    echo "The system will now use real AI services for orchestration."
    echo "Check the backend logs to verify AI services are working:"
    echo "docker compose logs backend --tail=20"
else
    echo ""
    echo "ℹ️  AI services setup skipped."
    echo "The system will continue using intelligent templates."
    echo "You can run this script again anytime to configure real AI services."
fi

echo ""
echo "📊 Current Status:"
echo "=================="
echo "The orchestration system is currently using:"
if grep -q "OPENAI_API_KEY=your_openai_api_key_here" env.local && \
   grep -q "ANTHROPIC_API_KEY=your_anthropic_api_key_here" env.local && \
   grep -q "GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here" env.local; then
    echo "🔄 Intelligent Templates (fallback mode)"
    echo "   - High-quality, context-aware responses"
    echo "   - No API costs"
    echo "   - Reliable and consistent"
else
    echo "🤖 Real AI Services (configured)"
    echo "   - Live AI responses from configured providers"
    echo "   - Dynamic and contextual analysis"
    echo "   - API costs apply"
fi

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Test the orchestration system at: http://localhost:3000"
echo "2. Check system status at: http://localhost:8000/api/v1/orchestration/status"
echo "3. View API documentation at: http://localhost:8000/docs"
echo ""
echo "Happy orchestrating! 🚀"
