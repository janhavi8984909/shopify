from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="Mock Shopify API")

# ✅ ADDED: CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/mock-data")
def get_mock_data(query: str = Query("")):
    """Mock Shopify API endpoint"""
    
    if "inventory" in query.lower():
        return {
            "data_type": "inventory",
            "low_stock_products": [
                {"id": 1, "title": "Blue T-Shirt", "inventory_quantity": 5, "status": "low"},
                {"id": 3, "title": "Red Cap", "inventory_quantity": 3, "status": "critical"},
                {"id": 4, "title": "White Sneakers", "inventory_quantity": 8, "status": "low"}
            ],
            "message": "3 products have low inventory levels",
            "recommendation": "Reorder 50 units total"
        }
    
    elif "sales" in query.lower() or "top" in query.lower():
        return {
            "data_type": "sales",
            "top_products": [
                {"product": "Blue T-Shirt", "units_sold": 45, "revenue": 1345.55},
                {"product": "Black Jeans", "units_sold": 32, "revenue": 1919.68},
                {"product": "Red Cap", "units_sold": 28, "revenue": 699.72}
            ],
            "total_revenue": 3965.00,
            "period": "last_7_days"
        }
    
    elif "customer" in query.lower():
        return {
            "data_type": "customers",
            "repeat_customers": [101, 205, 308, 412, 519],
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
                "average_order_value": 125.00,
                "customers": 28
            }
        }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "mock_shopify"}

@app.get("/")
def home():
    return {
        "message": "Mock Shopify API",
        "endpoints": ["GET /mock-data?query=inventory", "GET /health"],
        "port": 8002
    }

if __name__ == "__main__":
    import uvicorn
    print("🛍️ Mock Shopify API starting on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
    