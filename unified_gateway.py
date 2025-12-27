"""
Unified Gateway for Shopify AI Analytics - Railway Deployment
============================================================
This file combines all services into a single application for Railway.
Railway requires a single service on a single port.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import requests
from pydantic import BaseModel
import threading
import time

# Get the root directory
ROOT_DIR = Path(__file__).parent

# Add project directories to Python path
sys.path.insert(0, str(ROOT_DIR / "main_api"))
sys.path.insert(0, str(ROOT_DIR / "ai_agent" / "agent"))
sys.path.insert(0, str(ROOT_DIR / "mock_shopify"))

app = FastAPI(
    title="Shopify AI Analytics Platform",
    description="AI-powered analytics for Shopify stores",
    version="2.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== IMPORT SERVICES ====================

def import_ai_agent():
    """Dynamically import AI agent functions"""
    try:
        # Add agent directory to path
        agent_dir = ROOT_DIR / "ai_agent" / "agent"
        sys.path.insert(0, str(agent_dir))
        
        # Import the agent module
        from agent import generate_shopifyql_with_ai, generate_business_answer
        
        # Mock OpenAI client for testing (will use real one from .env)
        class MockOpenAI:
            class chat:
                class completions:
                    @staticmethod
                    def create(**kwargs):
                        return type('obj', (object,), {
                            'choices': [type('obj', (object,), {
                                'message': type('obj', (object,), {
                                    'content': '{"query": "SELECT * FROM products LIMIT 5", "intent": "general", "explanation": "Test query"}'
                                })()
                            })()]
                        })()
        
        return {
            "generate_shopifyql": generate_shopifyql_with_ai,
            "generate_answer": generate_business_answer,
            "status": "loaded"
        }
    except Exception as e:
        print(f"⚠️ AI Agent import warning: {e}")
        return {
            "status": "fallback",
            "error": str(e)
        }

def import_mock_shopify():
    """Dynamically import mock shopify functions"""
    try:
        # Create a simple mock shopify handler
        def mock_shopify_handler(query: str):
            query_lower = query.lower()
            
            if "inventory" in query_lower or "stock" in query_lower:
                return {
                    "data_type": "inventory",
                    "low_stock_products": [
                        {"id": 1, "title": "Blue T-Shirt", "inventory_quantity": 5, "status": "low"},
                        {"id": 2, "title": "Red Cap", "inventory_quantity": 3, "status": "critical"},
                        {"id": 3, "title": "White Sneakers", "inventory_quantity": 8, "status": "low"}
                    ],
                    "message": "3 products need restocking",
                    "recommendation": "Order 50+ units"
                }
            elif "sales" in query_lower or "revenue" in query_lower:
                return {
                    "data_type": "sales",
                    "top_products": [
                        {"product": "Blue T-Shirt", "units_sold": 45, "revenue": 1345.55},
                        {"product": "Black Jeans", "units_sold": 32, "revenue": 1919.68}
                    ],
                    "total_revenue": 3965.00,
                    "period": "last_7_days"
                }
            elif "customer" in query_lower:
                return {
                    "data_type": "customers",
                    "repeat_customers": [101, 205, 308],
                    "total_repeat_orders": 15,
                    "repeat_rate": "24%"
                }
            else:
                return {
                    "data_type": "general",
                    "store_stats": {
                        "total_products": 15,
                        "total_orders": 42,
                        "total_revenue": 5250.00,
                        "average_order_value": 125.00
                    }
                }
        
        return {
            "get_data": mock_shopify_handler,
            "status": "loaded"
        }
    except Exception as e:
        print(f"⚠️ Mock Shopify import warning: {e}")
        return {
            "status": "fallback",
            "error": str(e)
        }

# ==================== LOAD SERVICES ====================

print("🔄 Loading services...")
ai_agent = import_ai_agent()
mock_shopify = import_mock_shopify()
print("✅ Services loaded")

# ==================== PYDANTIC MODELS ====================

class QuestionRequest(BaseModel):
    store_id: str = "demo-store.myshopify.com"
    question: str

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "application": "Shopify AI Analytics Platform",
        "version": "2.0.0",
        "status": "online",
        "services": {
            "ai_agent": ai_agent["status"],
            "mock_shopify": mock_shopify["status"]
        },
        "endpoints": {
            "ask_question": "POST /api/v1/questions",
            "health": "GET /health",
            "services": "GET /services"
        },
        "deployment": "Railway Unified Gateway",
        "documentation": "See README.md for usage"
    }

@app.get("/health")
async def health():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "ai_agent": ai_agent["status"],
            "mock_shopify": mock_shopify["status"],
            "gateway": "online"
        }
    }

@app.get("/services")
async def services():
    """Service status endpoint"""
    return {
        "ai_agent": ai_agent["status"],
        "mock_shopify": mock_shopify["status"],
        "gateway": "online"
    }

@app.post("/api/v1/questions")
async def ask_question(request: QuestionRequest):
    """
    Main endpoint: Ask a question about Shopify data
    This simulates Rails Api::V1::QuestionsController#create
    """
    try:
        print(f"📥 Question received: {request.question}")
        
        # Step 1: Generate ShopifyQL query using AI
        if ai_agent["status"] == "loaded":
            try:
                ai_result = ai_agent["generate_shopifyql"](request.question)
                query = ai_result.get("query", "SELECT * FROM products LIMIT 5")
                intent = ai_result.get("intent", "general")
                
                # Step 2: Generate business answer
                business_answer = ai_agent["generate_answer"](request.question, intent)
            except Exception as e:
                print(f"⚠️ AI Agent error, using fallback: {e}")
                query = f"MOCK_QUERY: SELECT * FROM data WHERE question LIKE '%{request.question[:20]}%'"
                business_answer = f"I analyzed: '{request.question}'. Based on your store data, I recommend reviewing inventory levels and customer purchase patterns."
                intent = "fallback"
        else:
            # Fallback mode
            query = f"MOCK_QUERY: SELECT * FROM products WHERE title LIKE '%{request.question[:10]}%'"
            business_answer = f"Fallback analysis: '{request.question}'. Your store shows healthy metrics. Consider checking inventory for popular items."
            intent = "fallback"
        
        # Step 3: Get mock data
        if mock_shopify["status"] == "loaded":
            raw_data = mock_shopify["get_data"](query)
        else:
            raw_data = {
                "mock_data": True,
                "store_stats": {
                    "total_products": 15,
                    "total_orders": 42,
                    "total_revenue": 5250.00,
                    "average_order_value": 125.00
                }
            }
        
        # Step 4: Return response
        return {
            "answer": business_answer,
            "confidence": "high",
            "query_used": query,
            "raw_data": raw_data,
            "rails_gateway": True,
            "unified_gateway": True,
            "ai_model": "gpt-3.5-turbo" if ai_agent["status"] == "loaded" else "fallback",
            "timestamp": time.time()
        }
        
    except Exception as e:
        print(f"❌ Error in ask_question: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "Error processing question",
                "fallback_answer": f"Sorry, I encountered an error analyzing: '{request.question}'. Please try again."
            }
        )

@app.post("/analyze")
async def analyze_direct(request: Request):
    """Direct AI analysis endpoint (compatible with agent.py)"""
    try:
        data = await request.json()
        question = data.get("question", "")
        store_domain = data.get("store_domain", "demo.myshopify.com")
        
        if not question:
            raise HTTPException(status_code=400, detail="Missing question")
        
        print(f"🤖 Direct analysis: {question}")
        
        # Use AI agent if available
        if ai_agent["status"] == "loaded":
            try:
                ai_result = ai_agent["generate_shopifyql"](question)
                business_answer = ai_agent["generate_answer"](question, ai_result.get("intent", "general"))
                
                return {
                    "answer": business_answer,
                    "confidence": "high",
                    "query": ai_result.get("query", "SELECT * FROM products LIMIT 5"),
                    "intent": ai_result.get("intent", "general"),
                    "explanation": ai_result.get("explanation", "AI-generated query"),
                    "ai_model": "gpt-3.5-turbo"
                }
            except Exception as e:
                print(f"⚠️ AI error in direct analysis: {e}")
        
        # Fallback response
        return {
            "answer": f"Direct analysis of: '{question}'. This would normally use OpenAI GPT for deep insights.",
            "confidence": "medium",
            "query": f"SELECT * FROM products WHERE title LIKE '%{question[:10]}%'",
            "intent": "general",
            "explanation": "Fallback query for demonstration",
            "ai_model": "simulated"
        }
        
    except Exception as e:
        return {"error": str(e), "message": "Analysis failed"}

@app.get("/mock-data")
async def get_mock_data(query: str = ""):
    """Mock Shopify API endpoint (compatible with shopify_mock.py)"""
    if mock_shopify["status"] == "loaded":
        return mock_shopify["get_data"](query)
    else:
        return {
            "data_type": "general",
            "store_stats": {
                "total_products": 15,
                "total_orders": 42,
                "total_revenue": 5250.00
            },
            "message": "Using unified gateway mock data"
        }

# ==================== FRONTEND COMPATIBILITY ====================

@app.get("/api/v1/health")
async def api_health():
    """Health endpoint for frontend compatibility"""
    return {"status": "healthy", "service": "shopify_analytics_api_gateway"}

# ==================== STARTUP ====================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("=" * 50)
    print("🚀 Shopify AI Analytics - Unified Gateway")
    print("=" * 50)
    print(f"📁 Root Directory: {ROOT_DIR}")
    print(f"🔧 AI Agent Status: {ai_agent['status']}")
    print(f"🛍️ Mock Shopify Status: {mock_shopify['status']}")
    print(f"🌐 Port: {os.getenv('PORT', 8000)}")
    print("=" * 50)

# ==================== MAIN ====================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting Unified Gateway on port {port}...")
    print(f"📡 URL: http://0.0.0.0:{port}")
    print(f"📊 Health: http://0.0.0.0:{port}/health")
    print(f"🎯 API: POST http://0.0.0.0:{port}/api/v1/questions")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
    