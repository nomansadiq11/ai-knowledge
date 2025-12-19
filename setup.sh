#!/bin/bash

echo "🚀 Starting AI Knowledge Application..."
echo ""

# Start docker compose
echo "📦 Starting Docker containers..."
if ! docker compose up -d; then
    echo "❌ Failed to start Docker containers"
    echo "Please check Docker is running and try again"
    exit 1
fi

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if Ollama is running
echo ""
echo "🔍 Checking Ollama service..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not responding yet, it may still be starting..."
fi

# Pull the LLM model if not already present
echo ""
echo "🤖 Pulling gpt-oss:20b model (this may take a while on first run)..."
ollama pull gpt-oss:20b

echo ""
echo "✅ Setup complete!"
echo ""
echo "📱 Access the application at: http://localhost:8501"
echo ""
echo "To stop the application, run: docker compose down"
echo "To view logs, run: docker compose logs -f"
