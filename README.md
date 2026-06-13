# AI News Summarizer

> 🛠️ Practice Project — Built to solidify ReAct agent loop, streaming, and sentiment analysis concepts.

AI-powered news summarizer with ReAct agent loop, real-time streaming, and sentiment analysis built with FastAPI and Gemini API.

## Features
- ReAct agent loop built from scratch using Gemini API
- Real-time streaming responses via SSE
- Sentiment analysis via prompt chaining
- Stateless design — no database, no session storage

## Tech Stack
- FastAPI
- Gemini API (gemini-2.5-flash-lite)
- NewsAPI
- Pydantic
- Python

## Architecture
Stateless design — each request is fully independent. ReAct agent loop runs fresh per query. No authentication layer in this project.

> 🔐 For JWT authentication and role-based access control (RBAC) implementation, refer to [Hospital Appointment Management System](https://github.com/prem-ai-dev/hospital-appointment-system)

## Setup
1. Clone the repo
2. Create .env file with your API keys
3. pip install -r requirements.txt
4. uvicorn main:app --reload

## Environment Variables
NEWS_API_KEY=
GEMINI_API_KEY=
