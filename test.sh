#!/bin/bash

echo "🧪 Testing AI Knowledge Application..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check for docker compose (v2) or docker-compose (v1)
if docker compose version &> /dev/null; then
    echo "✅ Docker Compose v2 is installed"
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose v1 is installed"
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo ""

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found. Please run this script from the project root."
    exit 1
fi

echo "✅ docker-compose.yml found"
echo ""

# Test building the Docker image
echo "🏗️  Testing Docker build..."
if $COMPOSE_CMD build --no-cache webui; then
    echo "✅ Docker build successful"
else
    echo "❌ Docker build failed"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
echo ""
echo "To start the application, run: ./setup.sh or $COMPOSE_CMD up -d"
