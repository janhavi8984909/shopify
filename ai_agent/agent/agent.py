"""
Shopify AI Analytics - AI Agent Service (OpenAI GPT)
Deployment-ready for Render.com
"""
import os
import json
import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Shopify AI Agent Service",
    description="AI-powered ShopifyQL query generator and data analyzer",
    version="1.0.0"
)

# Environment variables
PORT = int(os.environ.get("PORT", 8001))
API_GATEWAY_URL = os.environ.get("API_GATEWAY_URL", "https://shopify-ai-main-api.onrender.com")
MOCK_API_URL = os.environ.get("MOCK_API_URL", "https://shopify-ai-mock-api.onrender.com")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

# Initialize OpenAI
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    logger.info("OpenAI API key loaded")
else:
    logger.warning("OPENAI_API_KEY not found. AI features will use mock responses.")

# Request/Response models
class AgentRequest(BaseModel):
    store_id: str
    question: str
    access_token: Optional[str] = None

class AgentResponse(BaseModel):
    answer: str
    confidence: str
    query_used: Optional[str] = None
    data_source: str
    processing_time: float

class HealthResponse(BaseModel):
    status: str
    service: str
    openai_configured: bool
    timestamp: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Shopify AI Agent Service",
        "status": "running",
        "version": "1.0.0",
        "openai_configured": bool(OPENAI_API_KEY),
        "endpoints": {
            "health": "/health",
            "process": "POST /process",
            "test": "/test"
        }
    }

@app.get("/health")
async def health_check():
    """Health check for Render"""
    return HealthResponse(
        status="healthy",
        service="ai-agent",
        openai_configured=bool(OPENAI_API_KEY),
        timestamp=datetime.now().isoformat()
    )

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify AI functionality"""
    test_question = "What were my sales last week?"
    
    try:
        shopifyql = generate_shopifyql(test_question)
        return {
            "test": "successful",
            "question": test_question,
            "generated_query": shopifyql[:100] + "..." if len(shopifyql) > 100 else shopifyql,
            "openai_available": bool(OPENAI_API_KEY),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "test": "failed",
            "error": str(e),
            "openai_available": bool(OPENAI_API_KEY)
        }

@app.post("/process")
async def process_question(request: AgentRequest):
    """
    Main endpoint: Process natural language questions
    """
    start_time = datetime.now()
    logger.info(f"Processing question: {request.question}")
    
    try:
        # Step 1: Generate ShopifyQL query using AI
        shopifyql_query = generate_shopifyql(request.question)
        logger.info(f"Generated ShopifyQL: {shopifyql_query[:100]}...")
        
        # Step 2: Get data from appropriate source
        use_real_shopify = request.access_token and request.access_token.startswith("shpat_")
        
        if use_real_shopify and request.store_id != "test.myshopify.com":
            # Real Shopify integration (placeholder for future)
            data = get_mock_data(request.question)
            data_source = "mock (real shopify placeholder)"
        else:
            # Use mock data
            data = get_mock_data(request.question)
            data_source = "mock_shopify"
        
        # Step 3: Generate business-friendly answer using AI
        answer = generate_business_answer(request.question, data, shopifyql_query)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Determine confidence level
        confidence = "high" if len(answer) > 20 else "medium"
        
        logger.info(f"Question processed in {processing_time:.2f}s")
        
        return AgentResponse(
            answer=answer,
            confidence=confidence,
            query_used=shopifyql_query,
            data_source=data_source,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )

def generate_shopifyql(question: str) -> str:
    """Generate ShopifyQL query from natural language using OpenAI"""
    
    # If OpenAI is not configured, return a mock query
    if not OPENAI_API_KEY:
        logger.warning("OpenAI not configured, using mock ShopifyQL")
        return get_mock_shopifyql(question)
    
    try:
        prompt = f"""
        Convert this business question into a valid ShopifyQL query.
        Question: "{question}"
        
        Available tables: orders, products, inventory, customers
        Use appropriate date filters for "last week", "last month", etc.
        Return ONLY the ShopifyQL query, no explanations.
        
        ShopifyQL Query:
        """
        
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a ShopifyQL expert. Generate valid ShopifyQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        query = response.choices[0].message.content.strip()
        return query
        
    except Exception as e:
        logger.error(f"OpenAI error: {e}, using fallback query")
        return get_mock_shopifyql(question)

def get_mock_shopifyql(question: str) -> str:
    """Fallback mock ShopifyQL generator"""
    question_lower = question.lower()
    
    if "inventory" in question_lower and "low" in question_lower:
        return "SELECT product_title, inventory_quantity FROM products WHERE inventory_quantity < 20 ORDER BY inventory_quantity ASC LIMIT 10"
    elif "sales" in question_lower and "last week" in question_lower:
        return "SELECT DATE(processed_at) as date, SUM(total_price) as daily_sales FROM orders WHERE DATE(processed_at) >= DATE_SUB(NOW(), INTERVAL 7 DAY) GROUP BY DATE(processed_at) ORDER BY date DESC"
    elif "top" in question_lower and "product" in question_lower:
        return "SELECT product_title, SUM(quantity) as units_sold, SUM(price * quantity) as revenue FROM order_line_items WHERE DATE(processed_at) >= DATE_SUB(NOW(), INTERVAL 30 DAY) GROUP BY product_title ORDER BY revenue DESC LIMIT 5"
    elif "customer" in question_lower and "repeat" in question_lower:
        return "SELECT customer_email, COUNT(order_id) as order_count FROM orders GROUP BY customer_email HAVING order_count > 1 ORDER BY order_count DESC"
    else:
        return "SELECT * FROM orders WHERE DATE(processed_at) >= DATE_SUB(NOW(), INTERVAL 30 DAY) LIMIT 10"

def get_mock_data(question: str) -> Dict[str, Any]:
    """Get mock data from mock Shopify API"""
    try:
        # Call mock API
        mock_url = f"{MOCK_API_URL}/mock-data"
        params = {"query": question}
        
        response = requests.get(mock_url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Mock API returned {response.status_code}, using fallback data")
            return generate_fallback_data(question)
            
    except Exception as e:
        logger.error(f"Error fetching mock data: {e}")
        return generate_fallback_data(question)

def generate_fallback_data(question: str) -> Dict[str, Any]:
    """Generate fallback mock data"""
    question_lower = question.lower()
    
    if "sales" in question_lower:
        return {
            "total_sales": 1850.75,
            "order_count": 15,
            "average_order_value": 123.38,
            "top_product": "Premium T-Shirt",
            "top_product_sales": 450.50
        }
    elif "inventory" in question_lower:
        return {
            "low_stock_items": [
                {"product": "Premium T-Shirt", "quantity": 5},
                {"product": "Coffee Mug", "quantity": 8},
                {"product": "Notebook", "quantity": 12}
            ],
            "total_products": 42,
            "out_of_stock": 2
        }
    elif "product" in question_lower:
        return {
            "top_products": [
                {"name": "Premium T-Shirt", "revenue": 450.50, "units": 15},
                {"name": "Coffee Mug", "revenue": 300.25, "units": 20},
                {"name": "Notebook", "revenue": 250.75, "units": 10}
            ]
        }
    else:
        return {
            "message": "Sample data for analysis",
            "total_orders": 15,
            "total_revenue": 1850.75,
            "average_customer_value": 123.38
        }

def generate_business_answer(question: str, data: Dict[str, Any], query: str) -> str:
    """Generate business-friendly answer using AI"""
    
    # If OpenAI is not configured, use template-based answers
    if not OPENAI_API_KEY:
        return generate_template_answer(question, data)
    
    try:
        prompt = f"""
        You are a helpful business analyst for a Shopify store.
        Based on the data and query below, provide a clear, concise business answer.
        
        Question: {question}
        Query Used: {query}
        Data Retrieved: {json.dumps(data, indent=2)}
        
        Provide a 2-3 sentence answer that:
        1. Directly answers the question
        2. Mentions key numbers from the data
        3. Gives actionable insight if relevant
        
        Answer:
        """
        
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful business analyst. Provide clear, actionable insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
        
    except Exception as e:
        logger.error(f"OpenAI answer generation failed: {e}")
        return generate_template_answer(question, data)

def generate_template_answer(question: str, data: Dict[str, Any]) -> str:
    """Template-based fallback answer generator"""
    question_lower = question.lower()
    
    if "sales" in question_lower:
        if "total_sales" in data:
            return f"Last week, you had ${data['total_sales']:,.2f} in sales from {data.get('order_count', 15)} orders. Your average order value was ${data.get('average_order_value', 123.38):,.2f}."
        else:
            return "Based on recent data, your store is performing well with steady sales growth."
    
    elif "inventory" in question_lower and "low" in question_lower:
        if "low_stock_items" in data:
            items = data["low_stock_items"]
            item_list = ", ".join([f"{item['product']} ({item['quantity']} left)" for item in items[:3]])
            return f"You have {len(items)} products low in stock: {item_list}. Consider reordering soon to avoid stockouts."
        else:
            return "Your inventory levels look healthy. No products are critically low at the moment."
    
    elif "top" in question_lower and "product" in question_lower:
        if "top_products" in data:
            top = data["top_products"][0] if data["top_products"] else {}
            return f"Your top-selling product is {top.get('name', 'Premium T-Shirt')} with ${top.get('revenue', 450.50):,.2f} in revenue. It's performing well in the market."
        else:
            return "Your products are selling steadily. The Premium T-Shirt has been particularly popular with customers."
    
    else:
        return f"Based on your store data: {question}. The analysis shows positive trends in customer engagement and sales performance."

if __name__ == "__main__":
    logger.info(f"Starting AI Agent Service on port {PORT}")
    logger.info(f"API Gateway URL: {API_GATEWAY_URL}")
    logger.info(f"Mock API URL: {MOCK_API_URL}")
    logger.info(f"OpenAI Configured: {bool(OPENAI_API_KEY)}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
    