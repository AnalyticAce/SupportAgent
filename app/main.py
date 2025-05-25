from fastapi import FastAPI
from app.api import agent_router, faq_router

# Comprehensive project description for API documentation
description = """
# SupportAgent 🤖 - Intelligent AI-Powered Customer Support

An advanced AI-powered SaaS support agent built with **OpenAI GPT-4** and **Pydantic-AI**, featuring cutting-edge **RAG (Retrieval-Augmented Generation)** capabilities for intelligent customer support automation.

## 🌟 Key Features

### AI-Powered Support
- **GPT-4 Integration**: Leverages OpenAI's most advanced language model for natural language understanding
- **Intelligent Responses**: Contextual, personalized support based on user account information
- **Smart Escalation**: AI-driven decision making for when to escalate to human agents
- **Risk Assessment**: Automatic risk scoring (0-10) for each support query

### RAG Implementation
- **Vector Embeddings**: Uses OpenAI's `text-embedding-3-small` model for semantic understanding
- **Semantic Search**: Intelligent FAQ search using vector similarity with PostgreSQL + pgvector
- **Context-Aware Responses**: Retrieves relevant documentation to provide accurate, up-to-date answers
- **Knowledge Base Integration**: Seamlessly integrates with FAQ database for enhanced response quality

### Database & Architecture
- **PostgreSQL + pgvector**: Advanced vector database for efficient similarity search
- **SQLAlchemy ORM**: Robust database interactions with automatic relationship management
- **FastAPI Framework**: Modern, high-performance API with automatic documentation
- **Pydantic Validation**: Type-safe request/response models with automatic validation

### Account Management
- **User Account Integration**: Real-time account status and subscription plan checking
- **Personalized Support**: Tailored responses based on user subscription tier and account status
- **Multi-tier Support**: Different support levels for free, basic, premium, and enterprise users

## 🛠️ Available Tools

The AI agent has access to several specialized tools:

1. **User Account Tools**:
   - User name lookup and personalization
   - Account status verification (active/inactive/suspended)
   - Subscription plan identification and feature access

2. **Knowledge Base Tools**:
   - FAQ semantic search using vector embeddings
   - Category-based content filtering
   - Real-time FAQ management (CRUD operations)

3. **Intelligence Tools**:
   - Smart escalation detection
   - Risk level assessment
   - Context-aware response generation

## 🔧 Technical Stack

- **AI Framework**: Pydantic-AI for structured AI agent development
- **Language Model**: OpenAI GPT-4 for natural language processing
- **Embeddings**: OpenAI text-embedding-3-small for vector operations
- **Database**: PostgreSQL 16+ with pgvector extension
- **Web Framework**: FastAPI with automatic OpenAPI documentation
- **Package Management**: UV for fast, reliable dependency management
- **Validation**: Pydantic v2 for type safety and data validation

## 📊 Use Cases

- **Customer Support Automation**: Handle common queries automatically with high accuracy
- **FAQ Management**: Dynamically manage and search knowledge base content
- **Escalation Management**: Intelligently route complex issues to human agents
- **Multi-tenant Support**: Support different subscription tiers with appropriate service levels
- **Analytics Ready**: Risk scoring and escalation tracking for support metrics

## 🚀 Getting Started

1. Set up PostgreSQL with pgvector extension
2. Configure environment variables (OpenAI API key, database credentials)
3. Run database seeding to populate FAQ embeddings
4. Start the API server and explore the interactive documentation

## 📖 API Documentation

This interactive documentation provides:
- **Try It Out**: Test all endpoints directly from the browser
- **Request/Response Examples**: See exactly what data to send and expect
- **Schema Validation**: Automatic validation of all request and response data
- **Error Handling**: Comprehensive error responses with helpful messages

---

*Built with ❤️ using modern AI and web technologies for intelligent customer support automation.*
"""

app = FastAPI(
    title="SupportAgent API",
    description=description,
    version="2.0.0",
    contact={
        "name": "SupportAgent Team",
        "email": "support@supportagent.ai",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Support Agent",
            "description": "AI-powered support agent with RAG capabilities for intelligent customer assistance.",
        },
        {
            "name": "FAQ",
            "description": "FAQ management system with vector embeddings for semantic search and content management.",
        },
        {
            "name": "System",
            "description": "System health checks and general information endpoints.",
        },
    ]
)

@app.get("/", tags=["System"])
async def root():
    return {
        "message": "SupportAgent API is running",
        "version": "2.0.0",
        "features": [
            "AI-Powered Support with GPT-4",
            "RAG Implementation with Vector Embeddings",
            "PostgreSQL + pgvector Integration",
            "Intelligent FAQ Search",
            "Smart Escalation System",
            "Risk Assessment Scoring"
        ],
        "documentation": "/docs",
        "health_check": "/health"
    }


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy", 
        "service": "supportagent-api",
        "version": "2.0.0",
        "ai_model": "gpt-4-turbo",
        "embedding_model": "text-embedding-3-small",
        "database": "postgresql+pgvector"
    }


app.include_router(agent_router)
app.include_router(faq_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
