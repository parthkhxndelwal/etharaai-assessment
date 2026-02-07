#!/bin/bash

# Sutra HRMS - Quick Setup Script
# This script helps you get started with the application

set -e

echo "🕉️  Sutra HRMS - Setup Script"
echo "=============================="
echo ""

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configurations before continuing"
    echo "   Important: Change JWT_SECRET_KEY and ADMIN_PASSWORD"
    read -p "Press Enter to continue or Ctrl+C to exit..."
fi

echo "✅ .env file exists"
echo ""

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
RETRY_COUNT=0
MAX_RETRIES=30

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if docker-compose ps | grep -q "healthy"; then
        echo "✅ Services are running!"
        break
    fi
    echo "   Still waiting... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "❌ Services failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo ""
echo "🎉 Sutra HRMS is ready!"
echo ""
echo "Access the application:"
echo "  🌐 Frontend:     http://localhost:3000"
echo "  📡 Backend API:  http://localhost:8000"
echo "  📚 Swagger Docs: http://localhost:8000/docs"
echo "  📖 ReDoc:        http://localhost:8000/redoc"
echo ""
echo "Default login credentials (change in .env):"
echo "  Email:    admin@sutra.com"
echo "  Password: admin123"
echo ""
echo "Useful commands:"
echo "  View logs:       docker-compose logs -f"
echo "  Stop services:   docker-compose down"
echo "  Restart:         docker-compose restart"
echo ""
echo "🙏 Om Namah Shivaya | Jai Shree Ram! 🚩"
