#!/bin/bash

# I PROACTIVE BRICK Orchestration Intelligence - Development Setup Script

set -e

echo "🛠️  Setting up I PROACTIVE BRICK for development..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Please run this script from the project root directory."
    exit 1
fi

# Create Python virtual environment for backend
echo "🐍 Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Install Node.js dependencies for frontend
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create development environment file
echo "📝 Creating development environment file..."
if [ ! -f backend/.env ]; then
    cp backend/env.example backend/.env
    echo "⚠️  Please update backend/.env with your API keys"
fi

# Create development directories
echo "📁 Creating development directories..."
mkdir -p logs/backend
mkdir -p logs/frontend
mkdir -p data/postgres-dev
mkdir -p data/redis-dev

# Set up pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
cd backend
pip install pre-commit
pre-commit install
cd ..

cd frontend
npm install --save-dev husky lint-staged
npx husky install
npx husky add .husky/pre-commit "npm run lint"
cd ..

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "🚀 To start development:"
echo "   Backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "   Frontend: cd frontend && npm start"
echo ""
echo "🐳 To start with Docker:"
echo "   ./scripts/start.sh"
echo ""
echo "📚 Available commands:"
echo "   Backend tests:  cd backend && pytest"
echo "   Frontend tests: cd frontend && npm test"
echo "   Lint backend:   cd backend && flake8 ."
echo "   Lint frontend:  cd frontend && npm run lint"
echo ""
