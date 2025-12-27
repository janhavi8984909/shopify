## Shopify AI Analytics App

---

## 🎯 Project Overview
A fully functional AI-powered analytics application that connects natural language questions to Shopify data insights. This project demonstrates a complete 3-tier architecture with real OpenAI GPT integration, ready for production deployment.

---

## 🏗️ System Architecture

---

## 📊 Architecture Diagram

---

## ✅ Components

### 1. Rails-Compatible API Gateway (main_api/main.py)
   
✅ REST endpoint: POST /api/v1/questions (simulates Rails controller)

✅ Request validation & routing

✅ Authentication-ready structure (OAuth slots prepared)

✅ Production migration path to Rails controllers

✅ Rails design patterns implemented in Python

✅ Port: 8000


### 2. Python AI Service with Real LLM (ai_agent/agent/agent.py)
   
✅ Real OpenAI GPT-3.5 Turbo integration (not simulated)

✅ Dynamic ShopifyQL query generation from natural language

✅ Business-friendly answer generation

✅ Full agentic workflow: Question → Intent → Query → Insight

✅ Error handling & fallback mechanisms

✅ Port: 8001


### 3. Shopify Mock API (mock_shopify/shopify_mock.py)

✅ Simulates Shopify Admin API responses

✅ Structured inventory, sales, customer data

✅ Ready for real Shopify API integration

✅ CORS configured for frontend access

✅ Port: 8002


### 4. Frontend UI (frontend/index.html)

✅ Clean, responsive interface

✅ Example questions with one-click prompts

✅ Real-time system status monitoring

✅ Confidence indicators (High/Medium/Low)

✅ Technical details view (ShopifyQL queries, raw data)

---

## 🚀 Quick Start

### Prerequisites

Python 3.8+

OpenAI API key

Git Bash (Windows) or Terminal (Mac/Linux)

---

## Installation & Setup

### 1. Clone and navigate to project

"git clone <your-repo-url>
cd shopify-ai-project"

### 2. Set up OpenAI API key

"#Navigate to AI agent directory
cd ai_agent/agent

#Create .env file
echo "OPENAI_API_KEY=your_actual_openai_key_here" > .env

#Install dependencies
pip install -r requirements.txt"

### 3. Start all services

"#Terminal 1: Rails-Compatible Gateway
cd main_api
python main.py

#Terminal 2: AI Agent  
cd ai_agent/agent
python agent.py

#Terminal 3: Mock Shopify API
cd mock_shopify
python shopify_mock.py"

### 4. Open the frontend

Open "frontend/index.html" in your browser

Or use Live Server extension in VS Code

### One-Command Startup (Alternative)

"#Run from root directory
chmod +x start_all.sh
./start_all.sh"

---

## 📞 API Examples

### 1. Direct API Request

"curl -X POST http://localhost:8000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{"store_id": "demo-store.myshopify.com", "question": "What were my sales last Tuesday?"}'"

### 2. AI Agent Direct Call

"curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "Which products need restocking?", "store_domain": "test.myshopify.com"}'"

### 3. Mock Data Endpoint

"curl "http://localhost:8002/mock-data?query=SELECT+title,+inventory_quantity+FROM+products""

---

## 🔄 Data Flow (Step-by-Step)

1. User asks: "What were sales last Tuesday?"
   ↓
2. Frontend sends to API Gateway (port 8000)
   ↓
3. Gateway validates → Forwards to AI Agent (port 8001)
   ↓
4. AI Agent uses OpenAI GPT to:
   - Understand natural language
   - Generate ShopifyQL query
   ↓
5. AI requests data from Mock API (port 8002)
   ↓
6. Mock API returns structured inventory/sales data
   ↓
7. AI creates business explanation
   ↓
8. Gateway formats Rails-compatible response
   ↓
9. Frontend displays beautiful answer to user

---

## ✅ Core Concepts Demonstrated

System design & API architecture - 3-tier microservices architecture

Python + LLM orchestration - Real OpenAI GPT-3.5 Turbo integration

Agentic workflows - Question → AI → Query → Answer pipeline

ShopifyQL understanding - AI generates valid ShopifyQL syntax

Practical problem-solving - Working prototype with clear migration path

Rails API design - Rails-compatible gateway with production migration path

---

## 🔄 Migration to Production

This prototype demonstrates all architectural patterns required for production. The following mock layers are ready for production swap:

A PICTURE WILL BE HERE [SS]

---

## 🗺️ Production Roadmap

1: Convert gateway to Rails (Api::V1::QuestionsController)

2: Implement Shopify OAuth flow with real authentication

3: Connect to real Shopify Admin API

4: Deploy to production environment

---

## 🛠️ Technical Implementation

### 1. AI Agent Features:

Two-step AI processing: Query generation + business answer

Fallback mechanisms: Graceful degradation on API errors

Confidence scoring: High/Medium/Low confidence indicators

Query validation: Ensures valid ShopifyQL syntax


### 2. API Gateway Features:

Rails-compatible endpoints: /api/v1/questions

Error handling: Consistent error responses

Service orchestration: Coordinates between AI and data layers

CORS enabled: Frontend compatibility


### 3. Frontend Features:

Real-time monitoring: Service health checks

User-friendly interface: Clean, intuitive design

Example prompts: Quick-start questions

Detailed views: Show/hide technical details

---

## 🔮 Future Enhancements

### Production Implementation

Full Rails API - Convert Python gateway to Ruby on Rails

Shopify OAuth - Real store authentication with OAuth 2.0

Real Shopify API - Live data integration with GraphQL

Advanced Analytics - Predictive insights, trend analysis


#### Phase 3: Advanced Features

Multi-store support - Manage multiple Shopify stores

Custom reporting - Save and schedule reports

Team collaboration - Share insights with team members

Mobile app - iOS/Android companion apps


### Phase 4: Enterprise Features

Data warehouse integration - BigQuery, Snowflake, Redshift

Custom AI models - Fine-tuned for specific industries

API marketplace - Third-party integrations

White-label solution - Brandable for agencies

---

## 🚀 Deployment Options

### Option A: Railway.app

"# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway link
railway up"


### Option B: Render.com

Create new Web Service

Connect GitHub repository

Set build command: pip install -r requirements.txt

Set start command: cd main_api && python main.py


### Option C: Docker Deployment

"# Build and run
docker build -t shopify-ai-analytics .
docker run -p 8000:8000 shopify-ai-analytics"

---

## 🎯 Learning Objectives Achieved

### Technical Skills Demonstrated:

✅ Microservices Architecture: 3 independent services communicating via HTTP

✅ AI Integration: Real OpenAI API usage with proper error handling

✅ API Design: RESTful endpoints with proper validation

✅ Frontend Development: Responsive UI with real-time updates

✅ System Integration: Coordinating multiple services

✅ Deployment Readiness: Production configuration files included


### Business Understanding Demonstrated:

✅ Shopify Ecosystem: Understanding of Shopify data structure

✅ Business Intelligence: Translating data into actionable insights

✅ User Experience: Intuitive interface for non-technical users

✅ Scalability Planning: Clear path from prototype to production


### 📝 License & Attribution

#### This project is developed as a demonstration of AI-powered analytics integration with Shopify. It uses:

1. OpenAI GPT-3.5 Turbo for natural language processing

2. FastAPI for Python web framework

3. Mock data for demonstration purposes


#### For production use, replace mock layers with:

1. Real Shopify API with proper OAuth authentication

2. Ruby on Rails for the API gateway

3. Production database for data persistence

---

## 🤝 Contributing

This project welcomes contributions. To contribute:

1. Fork the repository

2. Create a feature branch

3. Implement changes with tests

4. Submit a pull request

---

## 🏆 Conclusion

This project successfully demonstrates a complete AI-powered analytics platform with:

✅ Working prototype with all core features

✅ Real AI integration (not simulated)

✅ Clear migration path to production

✅ Professional architecture with separation of concerns

✅ User-friendly interface with example questions

The system is production-ready with mock layers that can be directly swapped for real implementations, demonstrating both technical skill and strategic planning for scalability.

---
