## SHOPIFY AI ANALYTICS APP

---

## 🎯 Project Overview
A fully functional AI-powered analytics application that connects natural language questions to Shopify data insights. This project demonstrates a complete 3-tier architecture with real OpenAI GPT integration, ready for production deployment.

---

## 🏗️ System Architecture

<img width="547" height="346" alt="image" src="https://github.com/user-attachments/assets/730ddd89-f584-4c43-ac57-e5c30c87b39a" />

---

## 📊 Architecture Diagram

<img width="572" height="380" alt="image" src="https://github.com/user-attachments/assets/78edc462-219d-4355-a9af-63844bad200f" />

---

## ✅ Components

### 1. Rails-Compatible API Gateway (main_api/main.py)
   
a) REST endpoint: POST /api/v1/questions (simulates Rails controller)

b) Request validation & routing

c) Authentication-ready structure (OAuth slots prepared)

d) Production migration path to Rails controllers

e) Rails design patterns implemented in Python

f) Port: 8000


### 2. Python AI Service with Real LLM (ai_agent/agent/agent.py)
   
a) Real OpenAI GPT-3.5 Turbo integration (not simulated)

b) Dynamic ShopifyQL query generation from natural language

c) Business-friendly answer generation

d) Full agentic workflow: Question → Intent → Query → Insight

e) Error handling & fallback mechanisms

f) Port: 8001


### 3. Shopify Mock API (mock_shopify/shopify_mock.py)

a) Simulates Shopify Admin API responses

b) Structured inventory, sales, customer data

c) Ready for real Shopify API integration

d) CORS configured for frontend access

e) Port: 8002


### 4. Frontend UI (frontend/index.html)

a) Clean, responsive interface

b) Example questions with one-click prompts

c) Real-time system status monitoring

d) Confidence indicators (High/Medium/Low)

e) Technical details view (ShopifyQL queries, raw data)

---

## 🚀 Quick Start

### Prerequisites

1. Python 3.8+

2. OpenAI API key

3. Git Bash (Windows) or Terminal (Mac/Linux)

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

1. System design & API architecture - 3-tier microservices architecture

2. Python + LLM orchestration - Real OpenAI GPT-3.5 Turbo integration

3. Agentic workflows - Question → AI → Query → Answer pipeline

4. ShopifyQL understanding - AI generates valid ShopifyQL syntax

5. Practical problem-solving - Working prototype with clear migration path

6. Rails API design - Rails-compatible gateway with production migration path

---

## 🗺️ Production Roadmap

1. Convert gateway to Rails (Api::V1::QuestionsController)

2. Implement Shopify OAuth flow with real authentication

3. Connect to real Shopify Admin API

4. Deploy to production environment

---

## 🛠️ Technical Implementation

### 1. AI Agent Features:

a) Two-step AI processing: Query generation + business answer

b) Fallback mechanisms: Graceful degradation on API errors

c) Confidence scoring: High/Medium/Low confidence indicators

d) Query validation: Ensures valid ShopifyQL syntax


### 2. API Gateway Features:

a)Rails-compatible endpoints: /api/v1/questions

b) Error handling: Consistent error responses

c) Service orchestration: Coordinates between AI and data layers

d) CORS enabled: Frontend compatibility


### 3. Frontend Features:

a) Real-time monitoring: Service health checks

b) User-friendly interface: Clean, intuitive design

c) Example prompts: Quick-start questions

d) Detailed views: Show/hide technical details

---

## 🔮 Future Enhancements

### 1. Production Implementation

a) Full Rails API - Convert Python gateway to Ruby on Rails

b) Shopify OAuth - Real store authentication with OAuth 2.0

c) Real Shopify API - Live data integration with GraphQL

d) Advanced Analytics - Predictive insights, trend analysis


#### 2. Advanced Features

a) Multi-store support - Manage multiple Shopify stores

b) Custom reporting - Save and schedule reports

c) Team collaboration - Share insights with team members

d) Mobile app - iOS/Android companion apps


### 3. Enterprise Features

a) Data warehouse integration - BigQuery, Snowflake, Redshift

b) Custom AI models - Fine-tuned for specific industries

c) API marketplace - Third-party integrations

d) White-label solution - Brandable for agencies

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

a) Create new Web Service

b) Connect GitHub repository

c) Set build command: pip install -r requirements.txt

d) Set start command: cd main_api && python main.py


### Option C: Docker Deployment

"# Build and run
docker build -t shopify-ai-analytics .
docker run -p 8000:8000 shopify-ai-analytics"

---

## Working Model

### Shopify Test Dashboards

#### 1.
<img width="1047" height="792" alt="image" src="https://github.com/user-attachments/assets/9a7ada89-a2b1-41a1-9d64-a220d764ee46" />

---

### 2.
<img width="979" height="830" alt="image" src="https://github.com/user-attachments/assets/4fb1a42c-6aeb-431a-b244-6ad1c2dc13f1" />

---

### 3.
<img width="958" height="838" alt="image" src="https://github.com/user-attachments/assets/81ce8004-3989-4da7-956a-39928bc1ecab" />

---

### 4.
<img width="954" height="841" alt="image" src="https://github.com/user-attachments/assets/424fc6e8-5e2f-4c31-9303-75021dd683cc" />

---

### 5.
<img width="955" height="848" alt="image" src="https://github.com/user-attachments/assets/eab07215-57f5-4ef5-b1f7-3c00e8229bb8" />

---

## Shopify Dashboard

<img width="1777" height="844" alt="image" src="https://github.com/user-attachments/assets/870f6f00-0503-47ad-8829-7a7d373aa8d6" />

---

## Shopify Open AI Platform

<img width="1780" height="838" alt="image" src="https://github.com/user-attachments/assets/34874f73-d119-46c2-b43c-641a61753d14" />

---

## 🎯 Learning Objectives Achieved

### 1. Technical Skills Demonstrated:

a)  Microservices Architecture: 3 independent services communicating via HTTP

b) AI Integration: Real OpenAI API usage with proper error handling

c) API Design: RESTful endpoints with proper validation

d) Frontend Development: Responsive UI with real-time updates

e) System Integration: Coordinating multiple services

f) Deployment Readiness: Production configuration files included


### 2. Business Understanding Demonstrated:

a) Shopify Ecosystem: Understanding of Shopify data structure

b) Business Intelligence: Translating data into actionable insights

c) User Experience: Intuitive interface for non-technical users

d) Scalability Planning: Clear path from prototype to production

---

## 📝 License & Attribution

### This project is developed as a demonstration of AI-powered analytics integration with Shopify. It uses:

1. OpenAI GPT-3.5 Turbo for natural language processing

2. FastAPI for Python web framework

3. Mock data for demonstration purposes


### For production use, replace mock layers with:

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





