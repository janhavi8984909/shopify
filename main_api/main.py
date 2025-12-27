"""
Rails-Compatible API Gateway
=============================
This service acts as the Rails API layer specified in requirements.
It handles:
- Request validation
- Authentication (would be OAuth in production)
- Routing to Python AI service
- Response formatting

In a full Rails implementation, this would be a Rails controller
(Api::V1::QuestionsController) but uses FastAPI for prototyping speed.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI(title="Shopify Analytics API (Rails-Compatible Gateway)")

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Shopify Analytics API Gateway",
        "rails_compatible": True,
        "endpoint": "POST /api/v1/questions",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "shopify_analytics_api_gateway"}

@app.post("/api/v1/questions")
async def ask_question(data: dict):
    """
    Rails-compatible endpoint: POST /api/v1/questions
    Mirrors what would be in Api::V1::QuestionsController#create
    
    Request format (matches Rails params):
    {
        "store_id": "example-store.myshopify.com",
        "question": "How much inventory should I reorder?"
    }
    """
    try:
        question = data.get("question", "")
        store_id = data.get("store_id", "")
        
        if not question or not store_id:
            raise HTTPException(status_code=400, detail="Missing question or store_id")
        
        print(f"📥 Rails Gateway Received: {question}")
        
        # 1. Call AI Agent (port 8001) - This would be a service object in Rails
        agent_response = call_ai_agent(question, store_id)
        
        # 2. Get mock data (port 8002) - This would call Shopify API in production
        shopify_data = call_mock_shopify(agent_response.get("query", ""))
        
        # 3. Create final answer - This would be a Rails serializer/view
        final_answer = {
            "answer": agent_response.get("answer", ""),
            "confidence": agent_response.get("confidence", "medium"),
            "query_used": agent_response.get("query", "No query"),
            "raw_data": shopify_data,
            "rails_gateway": True,
            "ai_model": agent_response.get("ai_model", "unknown")
        }
        
        return final_answer
        
    except Exception as e:
        # Rails would have rescue_from in ApplicationController
        return {
            "error": str(e),
            "answer": "Service error occurred",
            "rails_gateway_error": True
        }

def call_ai_agent(question, store_id):
    """
    Service object method: Calls the Python AI agent
    In Rails, this would be AiAgentService.new.call(question, store_id)
    """
    try:
        response = requests.post(
            "http://localhost:8001/analyze",
            json={"question": question, "store_domain": store_id},
            timeout=5
        )
        return response.json()
    except:
        # Fallback for demo purposes
        return {
            "answer": f"Analyzed: '{question}'. Based on mock data, consider reviewing inventory.",
            "confidence": "low",
            "query": f"MOCK_QUERY: SELECT * FROM data WHERE question LIKE '%{question[:10]}%'",
            "ai_model": "fallback"
        }

def call_mock_shopify(query):
    """
    Service object method: Calls Shopify API
    In production, this would use Shopify OAuth tokens and real API
    """
    try:
        response = requests.get(
            "http://localhost:8002/mock-data",
            params={"query": query},
            timeout=5
        )
        return response.json()
    except:
        # Mock response for prototyping
        return {
            "mock_data": True,
            "store_stats": {
                "total_products": 15,
                "total_orders": 42,
                "total_revenue": 5250.00,
                "average_order_value": 125.00,
                "customers": 28
            },
            "note": "Using mock data for prototyping. In production, connects to real Shopify API."
        }

if __name__ == "__main__":
    import uvicorn
    print("🚂 Rails-Compatible API Gateway starting on port 8000...")
    print("   Endpoint: POST /api/v1/questions")
    print("   (Simulating Rails Api::V1::QuestionsController)")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    