from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import agent_router, faq_router


description = """
# SupportAgent 🤖 - AI-Powered Customer Support

An intelligent support agent built with **OpenAI GPT-4** and **RAG (Retrieval-Augmented Generation)** for automated customer support.

## 🌟 Key Features

- **GPT-4 Integration**: Advanced natural language understanding and contextual responses
- **RAG Implementation**: Vector embeddings with PostgreSQL + pgvector for semantic FAQ search
- **Smart Escalation**: AI-driven decision making with risk assessment (0-10 scoring)
- **Account Integration**: Personalized support based on user subscription and account status

## 🔧 Technical Stack

- **AI**: Pydantic-AI + OpenAI GPT-4 + text-embedding-3-small
- **Database**: PostgreSQL 16+ with pgvector extension
- **Framework**: FastAPI with automatic OpenAPI documentation
- **Validation**: Pydantic v2 for type safety

## 🛠️ Available Tools

1. **User Account**: Name lookup, status verification, subscription management
2. **Knowledge Base**: FAQ semantic search, category filtering, CRUD operations
3. **Intelligence**: Smart escalation detection, risk assessment, context-aware responses

## 📊 Use Cases

- Automated customer support with high accuracy
- Dynamic FAQ management and search
- Intelligent escalation routing
- Multi-tier subscription support
"""


app = FastAPI(
    title="SupportAgent API",
    description=description,
    version="1.0.0",
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

# Add CORS middleware to allow requests from the demo frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["System"])
async def root():
    """Root endpoint to verify API is running and provide basic information."""
    return {
        "message": "SupportAgent API is running",
        "version": "1.0.0",
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
    """Health check endpoint to verify API status and version information."""
    return {
        "status": "healthy", 
        "service": "supportagent-api",
        "version": "1.0.0",
        "ai_model": "gpt-4-turbo",
        "embedding_model": "text-embedding-3-small",
        "database": "postgresql+pgvector"
    }


app.include_router(agent_router)
app.include_router(faq_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
