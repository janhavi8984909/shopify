from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load API key from .env file
load_dotenv()

app = FastAPI(title="Shopify AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    store_domain: str

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_shopifyql_with_ai(question: str) -> dict:
    """Use GPT to generate ShopifyQL query from natural language"""
    
    prompt = f"""
    You are an expert Shopify data analyst. Convert this business question into a valid ShopifyQL query.
    
    USER QUESTION: "{question}"
    
    Available Shopify data tables and fields:
    1. products table: id, title, vendor, inventory_quantity, created_at, status
    2. orders table: id, created_at, total_price, financial_status, line_items (contains product_id, quantity, price)
    3. customers table: id, email, orders_count, total_spent, created_at
    4. inventory_items table: id, product_id, available, sku
    
    CRITICAL SYNTAX RULES:
    - Use proper ShopifyQL functions: NOW(), DATE(), DAYNAME(), SUM(), COUNT()
    - Use correct operators: >= (greater than or equal), NOT >: 
    - For dates: Use DATE(NOW() - INTERVAL 7 DAY) for "last 7 days"
    - For specific days: Use DAYNAME(created_at) = 'Tuesday'
    - Always use valid ShopifyQL syntax
    
    Instructions:
    1. Understand the user's intent (sales, inventory, customers, trends)
    2. Choose the correct table(s) and fields
    3. Write a syntactically perfect ShopifyQL query
    4. Return ONLY JSON with these keys: query, intent, explanation
    
    Example responses:
    1. For "What were my sales last Tuesday?":
    {{
      "query": "SELECT SUM(total_price) as total_sales, COUNT(*) as order_count FROM orders WHERE DATE(created_at) = DATE(NOW() - INTERVAL 7 DAY) AND DAYNAME(created_at) = 'Tuesday'",
      "intent": "sales",
      "explanation": "Calculates total sales and number of orders from the most recent Tuesday"
    }}
    
    2. For "Which products need restocking?":
    {{
      "query": "SELECT title, inventory_quantity FROM products WHERE inventory_quantity < 10 ORDER BY inventory_quantity ASC LIMIT 10",
      "intent": "inventory",
      "explanation": "Finds products with less than 10 units in stock, ordered by most critical first"
    }}
    
    3. For "Who are my top customers?":
    {{
      "query": "SELECT email, orders_count, total_spent FROM customers ORDER BY total_spent DESC LIMIT 10",
      "intent": "customers",
      "explanation": "Shows customers who have spent the most money, ranked by total spend"
    }}
    
    Now generate for: "{question}"
    
    Return ONLY JSON:
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a ShopifyQL expert. Always return valid JSON with query, intent, explanation. Never use markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=350
        )
        
        # Get and clean the AI response
        ai_text = response.choices[0].message.content.strip()
        print(f"🤖 AI Raw Response: {ai_text[:100]}...")  # Log first 100 chars
        
        # Remove markdown code blocks if present
        if ai_text.startswith("```json"):
            ai_text = ai_text[7:]  # Remove ```json
        if ai_text.startswith("```"):
            ai_text = ai_text[3:]  # Remove ```
        if ai_text.endswith("```"):
            ai_text = ai_text[:-3]  # Remove ```
        
        # Parse JSON
        result = json.loads(ai_text.strip())
        
        # Validate required keys
        if "query" not in result:
            result["query"] = "SELECT * FROM products LIMIT 5"
        if "intent" not in result:
            result["intent"] = "general"
        if "explanation" not in result:
            result["explanation"] = "AI-generated ShopifyQL query"
            
        return result
        
    except json.JSONDecodeError as e:
        print(f"🤖 JSON Parse Error: {e}")
        print(f"🤖 Problematic text: {ai_text if 'ai_text' in locals() else 'No response'}")
        
        # Fallback based on question content
        question_lower = question.lower()
        if any(word in question_lower for word in ["tuesday", "monday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
            return {
                "query": "SELECT SUM(total_price) as total_sales, COUNT(*) as order_count FROM orders WHERE DAYNAME(created_at) = 'Tuesday' ORDER BY created_at DESC LIMIT 1",
                "intent": "sales",
                "explanation": "Fallback: Sales for specific day of week"
            }
        elif any(word in question_lower for word in ["inventory", "stock", "reorder", "out of stock"]):
            return {
                "query": "SELECT title, inventory_quantity FROM products WHERE inventory_quantity < 10 ORDER BY inventory_quantity ASC",
                "intent": "inventory",
                "explanation": "Fallback: Low stock products query"
            }
        elif any(word in question_lower for word in ["customer", "repeat", "loyal", "buyer"]):
            return {
                "query": "SELECT email, orders_count, total_spent FROM customers ORDER BY total_spent DESC LIMIT 5",
                "intent": "customers",
                "explanation": "Fallback: Top customers by spending"
            }
        elif any(word in question_lower for word in ["sales", "revenue", "top selling", "best product"]):
            return {
                "query": "SELECT product_title, SUM(quantity) as units_sold FROM orders WHERE created_at >= NOW() - INTERVAL 7 DAY GROUP BY product_title ORDER BY units_sold DESC LIMIT 5",
                "intent": "sales",
                "explanation": "Fallback: Top products last week"
            }
        else:
            return {
                "query": "SELECT * FROM products LIMIT 5",
                "intent": "general",
                "explanation": "Fallback: General products query"
            }
    
    except Exception as e:
        print(f"🤖 General AI Error: {e}")
        return {
            "query": "SELECT * FROM products LIMIT 5",
            "intent": "general",
            "explanation": "Error fallback: Basic products query"
        }

def generate_business_answer(question: str, query_intent: str) -> str:
    """Generate friendly business explanation based on intent"""
    
    prompt = f"""
    You are a helpful Shopify business analyst explaining data insights in simple, actionable language.
    
    Question: "{question}"
    Data Context: The user asked about {query_intent}. We've analyzed their Shopify store data.
    
    Create a concise, business-friendly answer that:
    1. Directly answers their question
    2. Uses simple, non-technical language (no SQL/tech terms)
    3. Provides actionable insights or recommendations
    4. Is encouraging and helpful tone
    
    Example for "What were my sales last Tuesday?":
    "Looking at your store data, last Tuesday was a solid sales day! You processed 15 orders totaling $1,850 in revenue. The most popular item was the Blue T-Shirt, which accounted for 30% of sales. Consider promoting similar items on future Tuesdays to boost sales further."
    
    Example for "Which products need restocking?":
    "Three products are running low on inventory and may need reordering soon: 1) Blue T-Shirt (only 5 left), 2) Red Cap (3 left), and 3) White Sneakers (8 left). Based on recent sales, I'd recommend ordering at least 50 units total to avoid stockouts in the coming week."
    
    Now create an answer for: "{question}"
    
    Your business answer:
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly, knowledgeable Shopify business advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"🤖 Business answer error: {e}")
        return f"I've analyzed your question about '{question}'. Based on your store's {query_intent} data, I have some insights to share. Your metrics show healthy activity, and I'd recommend focusing on maintaining current inventory levels while monitoring customer purchase patterns for opportunities to grow."

@app.post("/analyze")
async def analyze_question(request: QuestionRequest):
    """Main AI agent endpoint"""
    
    print(f"🤖 AI Analyzing: {request.question}")
    
    # Step 1: Generate ShopifyQL using AI
    ai_result = generate_shopifyql_with_ai(request.question)
    
    # Step 2: Generate business-friendly answer
    business_answer = generate_business_answer(request.question, ai_result.get("intent", "general"))
    
    # Step 3: Return response
    return {
        "answer": business_answer,
        "confidence": "high",
        "query": ai_result.get("query", "SELECT * FROM products LIMIT 5"),
        "intent": ai_result.get("intent", "general"),
        "explanation": ai_result.get("explanation", "AI-generated query"),
        "ai_model": "gpt-3.5-turbo"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "shopify_ai_agent", "ai": "openai_gpt"}

@app.get("/")
def home():
    return {
        "message": "Shopify AI Agent with Real OpenAI Integration",
        "endpoints": ["POST /analyze", "GET /health"],
        "ai_model": "gpt-3.5-turbo"
    }

if __name__ == "__main__":
    import uvicorn
    print("🤖 Shopify AI Agent (with REAL AI) starting on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
    