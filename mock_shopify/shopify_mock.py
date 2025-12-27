"""
Shopify AI Analytics - Mock Shopify API
Deployment-ready for Render.com
"""
import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from flask import Flask, jsonify, request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Environment variables
PORT = int(os.environ.get("PORT", 8002))
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

# CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Sample data
PRODUCTS = [
    {"id": 1, "title": "Premium Cotton T-Shirt", "price": 29.99, "inventory": 50, "vendor": "Demo Brand", "type": "Clothing"},
    {"id": 2, "title": "Ceramic Coffee Mug", "price": 14.99, "inventory": 25, "vendor": "Demo Brand", "type": "Drinkware"},
    {"id": 3, "title": "Leather Notebook", "price": 24.99, "inventory": 15, "vendor": "Demo Brand", "type": "Stationery"},
    {"id": 4, "title": "Stainless Steel Water Bottle", "price": 34.99, "inventory": 30, "vendor": "Demo Brand", "type": "Drinkware"},
    {"id": 5, "title": "Wireless Earbuds", "price": 89.99, "inventory": 20, "vendor": "Tech Co", "type": "Electronics"},
    {"id": 6, "title": "Organic Soap Set", "price": 19.99, "inventory": 40, "vendor": "Natural Goods", "type": "Personal Care"},
    {"id": 7, "title": "Yoga Mat", "price": 39.99, "inventory": 18, "vendor": "Fitness Pro", "type": "Fitness"},
    {"id": 8, "title": "Phone Case", "price": 24.99, "inventory": 60, "vendor": "Tech Co", "type": "Accessories"},
    {"id": 9, "title": "Desk Organizer", "price": 29.99, "inventory": 22, "vendor": "Office Plus", "type": "Office"},
    {"id": 10, "title": "LED Desk Lamp", "price": 49.99, "inventory": 15, "vendor": "Home Goods", "type": "Home"},
]

# Generate sample orders
def generate_orders(count: int = 50) -> List[Dict[str, Any]]:
    orders = []
    customers = ["alice@example.com", "bob@example.com", "charlie@example.com", 
                 "diana@example.com", "evan@example.com", "fiona@example.com"]
    
    for i in range(1, count + 1):
        order_date = datetime.now() - timedelta(days=random.randint(0, 60))
        customer = random.choice(customers)
        product = random.choice(PRODUCTS)
        quantity = random.randint(1, 3)
        
        orders.append({
            "id": 1000 + i,
            "order_number": f"#{2000 + i}",
            "created_at": order_date.isoformat(),
            "customer_email": customer,
            "financial_status": "paid",
            "total_price": round(product["price"] * quantity, 2),
            "line_items": [
                {
                    "title": product["title"],
                    "quantity": quantity,
                    "price": str(product["price"]),
                    "product_id": product["id"]
                }
            ]
        })
    
    return orders

ORDERS = generate_orders(50)

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        "service": "Mock Shopify API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "products": "/api/products",
            "orders": "/api/orders",
            "inventory": "/api/inventory",
            "mock_data": "GET /mock-data?query=your_question"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check for Render"""
    return jsonify({
        "status": "healthy",
        "service": "mock-shopify",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/products')
def get_products():
    """Get all products"""
    limit = request.args.get('limit', default=10, type=int)
    return jsonify({
        "products": PRODUCTS[:limit],
        "count": len(PRODUCTS[:limit]),
        "total": len(PRODUCTS)
    })

@app.route('/api/orders')
def get_orders():
    """Get orders with optional filtering"""
    limit = request.args.get('limit', default=20, type=int)
    days = request.args.get('days', default=30, type=int)
    
    # Filter by date if specified
    cutoff_date = datetime.now() - timedelta(days=days)
    
    filtered_orders = []
    for order in ORDERS:
        order_date = datetime.fromisoformat(order["created_at"].replace('Z', '+00:00'))
        if order_date >= cutoff_date:
            filtered_orders.append(order)
    
    filtered_orders = filtered_orders[:limit]
    
    # Calculate summary stats
    total_revenue = sum(order["total_price"] for order in filtered_orders)
    avg_order_value = total_revenue / len(filtered_orders) if filtered_orders else 0
    
    return jsonify({
        "orders": filtered_orders,
        "summary": {
            "count": len(filtered_orders),
            "total_revenue": round(total_revenue, 2),
            "average_order_value": round(avg_order_value, 2),
            "time_period_days": days
        }
    })

@app.route('/api/inventory')
def get_inventory():
    """Get inventory data"""
    low_stock_threshold = request.args.get('low_threshold', default=20, type=int)
    
    low_stock = [p for p in PRODUCTS if p["inventory"] < low_stock_threshold]
    out_of_stock = [p for p in PRODUCTS if p["inventory"] <= 0]
    
    total_value = sum(p["price"] * p["inventory"] for p in PRODUCTS)
    
    return jsonify({
        "products": PRODUCTS,
        "inventory_summary": {
            "total_products": len(PRODUCTS),
            "low_stock_items": len(low_stock),
            "out_of_stock_items": len(out_of_stock),
            "total_inventory_value": round(total_value, 2),
            "low_stock_threshold": low_stock_threshold
        },
        "low_stock_items": low_stock
    })

@app.route('/mock-data')
def get_mock_data():
    """Get mock data based on query type"""
    query = request.args.get('query', '').lower()
    
    if 'inventory' in query or 'stock' in query or 'reorder' in query:
        low_stock = [p for p in PRODUCTS if p["inventory"] < 20]
        return jsonify({
            "query_type": "inventory",
            "low_stock_items": low_stock,
            "total_products": len(PRODUCTS),
            "low_stock_count": len(low_stock),
            "message": f"Found {len(low_stock)} products with low inventory"
        })
    
    elif 'sales' in query or 'revenue' in query or 'order' in query:
        # Get recent orders (last 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        recent_orders = []
        for order in ORDERS:
            order_date = datetime.fromisoformat(order["created_at"].replace('Z', '+00:00'))
            if order_date >= cutoff_date:
                recent_orders.append(order)
        
        recent_orders = recent_orders[:20]  # Limit to 20
        
        total_revenue = sum(order["total_price"] for order in recent_orders)
        avg_order_value = total_revenue / len(recent_orders) if recent_orders else 0
        
        # Find top product
        product_sales = {}
        for order in recent_orders:
            for item in order["line_items"]:
                product_name = item["title"]
                revenue = float(item["price"]) * item["quantity"]
                product_sales[product_name] = product_sales.get(product_name, 0) + revenue
        
        top_product = max(product_sales.items(), key=lambda x: x[1]) if product_sales else ("Premium T-Shirt", 450.50)
        
        return jsonify({
            "query_type": "sales",
            "total_sales": round(total_revenue, 2),
            "order_count": len(recent_orders),
            "average_order_value": round(avg_order_value, 2),
            "top_product": top_product[0],
            "top_product_sales": round(top_product[1], 2),
            "time_period": "last 30 days"
        })
    
    elif 'product' in query or 'item' in query:
        # Sort products by inventory (low to high) or other criteria
        if 'top' in query or 'best' in query:
            # Mock best sellers
            sorted_products = sorted(PRODUCTS, key=lambda x: (100 - x["inventory"]), reverse=True)[:5]
            return jsonify({
                "query_type": "top_products",
                "top_products": [
                    {
                        "name": p["title"],
                        "revenue": round(p["price"] * (100 - p["inventory"]), 2),
                        "units": (100 - p["inventory"])
                    }
                    for p in sorted_products
                ]
            })
        else:
            return jsonify({
                "query_type": "products",
                "products": PRODUCTS[:10],
                "total_products": len(PRODUCTS)
            })
    
    elif 'customer' in query:
        # Mock customer data
        customer_orders = {}
        for order in ORDERS:
            email = order["customer_email"]
            customer_orders[email] = customer_orders.get(email, 0) + 1
        
        repeat_customers = {email: count for email, count in customer_orders.items() if count > 1}
        
        return jsonify({
            "query_type": "customers",
            "total_customers": len(customer_orders),
            "repeat_customers": len(repeat_customers),
            "top_customers": sorted(repeat_customers.items(), key=lambda x: x[1], reverse=True)[:5]
        })
    
    else:
        # Default response
        return jsonify({
            "query_type": "general",
            "message": "Mock Shopify API is running",
            "available_data": {
                "products": len(PRODUCTS),
                "orders": len(ORDERS),
                "total_revenue": sum(order["total_price"] for order in ORDERS[:30])
            },
            "timestamp": datetime.now().isoformat()
        })

@app.route('/api/shop')
def get_shop_info():
    """Get mock store information"""
    return jsonify({
        "shop": {
            "id": 123456789,
            "name": "AI Analytics Test Store",
            "email": "contact@ai-analytics-test.com",
            "domain": "test.myshopify.com",
            "created_at": "2024-01-15T00:00:00-05:00",
            "plan_name": "Development",
            "currency": "USD",
            "country": "US"
        }
    })

@app.route('/test')
def test_endpoint():
    """Test endpoint"""
    return jsonify({
        "status": "success",
        "message": "Mock Shopify API is working correctly",
        "endpoints_tested": ["/health", "/api/products", "/api/orders", "/mock-data"],
        "sample_data_available": {
            "products": len(PRODUCTS),
            "orders": len(ORDERS)
        }
    })

if __name__ == '__main__':
    logger.info(f"Starting Mock Shopify API on port {PORT}")
    logger.info(f"Allowed origins: {ALLOWED_ORIGINS}")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False  # Set to False in production
    )
    