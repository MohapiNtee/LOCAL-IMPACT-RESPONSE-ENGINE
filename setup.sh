#!/bin/bash

# LIRE Setup Script for Linux/Mac
# This script initializes the LIRE project

set -e

echo "🚀 Starting LIRE setup..."

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
fi

echo "🐳 Starting Docker containers..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

echo "🗄️  Running database migrations..."
docker-compose exec -T backend python manage.py migrate

echo "👤 Creating superuser..."
docker-compose exec -T backend python manage.py createsuperuser --noinput --username admin --email admin@lire.local 2>/dev/null || true

echo ""
echo "✅ LIRE setup completed!"
echo ""
echo "📍 Application URLs:"
echo "   Frontend:    http://localhost:3000"
echo "   Backend API: http://localhost:8000/api/"
echo "   Admin Panel: http://localhost:8000/admin/"
echo ""
echo "📚 Docker commands:"
echo "   View logs:   docker-compose logs -f"
echo "   Stop:        docker-compose stop"
echo "   Start:       docker-compose start"
echo "   Restart:     docker-compose restart"
echo ""
