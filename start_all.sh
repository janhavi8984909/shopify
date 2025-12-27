#!/bin/bash

echo "🚀 Shopify AI Analytics Platform - Unified Deployment"
echo "====================================================="
echo ""
echo "Starting Unified Gateway (all services combined)..."
echo ""
echo "📡 Endpoints:"
echo "   • Main URL: http://localhost:8000"
echo "   • API: POST http://localhost:8000/api/v1/questions"
echo "   • Health: http://localhost:8000/health"
echo ""
echo "⚙️  Services included:"
echo "   • Rails-Compatible API Gateway"
echo "   • AI Agent with OpenAI GPT"
echo "   • Mock Shopify API"
echo ""
echo "Starting server..."

# Start the unified gateway
python unified_gateway.py
