"""
Shopify AI Analytics - Main API Gateway (Rails-Compatible)
Deployment-ready for Render.com
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Shopify AI Analytics API Gateway",
    description="Rails-compatible gateway for Shopify AI Analytics",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class QuestionRequest(BaseModel):
    store_id: str
    question: str
    access_token: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    dependencies: dict

# Get environment variables with defaults
AGENT_SERVICE_URL = os.environ.get("AGENT_SERVICE_URL", "https://shopify-ai-agent.onrender.com")
MOCK_SERVICE_URL = os.environ.get("MOCK_SERVICE_URL", "https://shopify-ai-mock-api.onrender.com")
PORT = int(os.environ.get("PORT", 8000))

@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "service": "Shopify AI Analytics API Gateway",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "ask_question": "POST /api/v1/questions"
        },
        "dependencies": {
            "ai_agent": AGENT_SERVICE_URL,
            "mock_api": MOCK_SERVICE_URL
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    dependencies = {}
    
    # Check AI Agent service
    try:
        agent_response = requests.get(f"{AGENT_SERVICE_URL}/health", timeout=5)
        dependencies["ai_agent"] = "healthy" if agent_response.status_code == 200 else "unhealthy"
    except:
        dependencies["ai_agent"] = "unreachable"
    
    # Check Mock API service
    try:
        mock_response = requests.get(f"{MOCK_SERVICE_URL}/health", timeout=5)
        dependencies["mock_api"] = "healthy" if mock_response.status_code == 200 else "unhealthy"
    except:
        dependencies["mock_api"] = "unreachable"
    
    return HealthResponse(
        status="healthy",
        service="api-gateway",
        dependencies=dependencies
    )

@app.get("/docs")
async def custom_docs():
    """Redirect to Swagger docs"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

@app.post("/api/v1/questions")
async def ask_question(request: QuestionRequest):
    """
    Accept natural language questions and return AI-powered insights
    """
    logger.info(f"Received question: {request.question} for store: {request.store_id}")
    
    try:
        # Forward to AI agent service
        ai_agent_endpoint = f"{AGENT_SERVICE_URL}/process"
        
        logger.info(f"Forwarding to AI agent: {ai_agent_endpoint}")
        
        response = requests.post(
            ai_agent_endpoint,
            json={
                "store_id": request.store_id,
                "question": request.question,
                "access_token": request.access_token
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"AI agent response received: {result.get('answer', '')[:50]}...")
            return result
        else:
            logger.error(f"AI Agent error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=500,
                detail=f"AI Agent service error: {response.status_code}"
            )
            
    except requests.exceptions.Timeout:
        logger.error("Request to AI agent timed out")
        raise HTTPException(
            status_code=504,
            detail="AI Agent service timeout. Please try again."
        )
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to AI agent service")
        raise HTTPException(
            status_code=503,
            detail="AI Agent service is unavailable. Please check if it's running."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/v1/status")
async def service_status():
    """Check status of all microservices"""
    services = {
        "api_gateway": {
            "status": "running",
            "url": f"https://shopify-ai-main-api.onrender.com",
            "port": PORT
        },
        "ai_agent": {
            "url": AGENT_SERVICE_URL,
            "status": "unknown"
        },
        "mock_shopify": {
            "url": MOCK_SERVICE_URL,
            "status": "unknown"
        }
    }
    
    # Check each service
    for service_name in ["ai_agent", "mock_shopify"]:
        url = AGENT_SERVICE_URL if service_name == "ai_agent" else MOCK_SERVICE_URL
        try:
            health_url = f"{url}/health"
            resp = requests.get(health_url, timeout=5)
            services[service_name]["status"] = "healthy" if resp.status_code == 200 else "unhealthy"
        except:
            services[service_name]["status"] = "unreachable"
    
    return services

if __name__ == "__main__":
    logger.info(f"Starting API Gateway on port {PORT}")
    logger.info(f"AI Agent URL: {AGENT_SERVICE_URL}")
    logger.info(f"Mock API URL: {MOCK_SERVICE_URL}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
    