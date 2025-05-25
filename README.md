# SupportAgent 🤖

An intelligent AI-powered SaaS support agent built with OpenAI GPT-4 and Pydantic-AI. This project demonstrates how to create an automated customer support system that can handle user queries, check account statuses, manage subscriptions, and determine when to escalate issues to human administrators using advanced RAG (Retrieval-Augmented Generation) capabilities.

> [!NOTE]
> This is a comprehensive implementation featuring advanced AI capabilities including vector embeddings, semantic search, and PostgreSQL integration. The current version provides enterprise-grade functionality for AI-powered support, with an extensible architecture that allows for easy addition of new capabilities, tools, and integrations as your support requirements grow.

## 🌟 Features

- **AI-Powered Support**: Uses OpenAI's GPT-4 model for natural language understanding and response generation
- **RAG Implementation**: Advanced Retrieval-Augmented Generation using vector embeddings for intelligent FAQ search
- **Vector Database**: PostgreSQL with pgvector extension for efficient similarity search
- **Semantic Search**: Uses OpenAI embeddings (text-embedding-3-small) for finding relevant documentation
- **Account Management**: Automatically checks user account status and subscription plans
- **Smart Escalation**: Determines when issues need to be escalated to human administrators
- **Risk Assessment**: Provides risk level scoring (0-10) for support queries
- **Database Integration**: SQLAlchemy-based data management with PostgreSQL and pgvector
- **Structured Responses**: Uses Pydantic models for consistent, validated outputs
- **FastAPI Server**: Built-in web server with interactive API documentation
- **REST API**: Comprehensive HTTP endpoints for agent queries and FAQ management

## 🏗️ Architecture

The support agent is built using several key components with advanced RAG capabilities:

- **Agent (`app/agent.py`)**: Core AI agent using Pydantic-AI framework with RAG implementation
- **Database (`app/database.py`)**: PostgreSQL setup with pgvector extension for vector operations
- **Models (`app/models.py`)**: Pydantic models for API requests and responses
- **API (`app/api.py`)**: FastAPI endpoints for agent queries and FAQ management
- **Config (`app/config.py`)**: Configuration settings and environment management
- **Seed (`scripts/seed.py`)**: Database seeding with sample users and vectorized FAQs

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL 16+ with pgvector extension
- OpenAI API key
- [UV package manager](https://docs.astral.sh/uv/) (fast Python package installer and resolver)

### Installation

1. **Set up PostgreSQL with pgvector**
   ```bash
   # Install PostgreSQL and pgvector (Ubuntu/Debian)
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   
   # Install pgvector extension
   sudo apt-get install postgresql-16-pgvector
   
   # Create database and user
   sudo -u postgres psql
   CREATE DATABASE supportagent;
   CREATE USER supportagent WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE supportagent TO supportagent;
   \c supportagent
   CREATE EXTENSION vector;
   \q
   ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SupportAgent
   ```

3. **Install dependencies**
   ```bash
   # Install dependencies with UV (main package manager)
   uv sync
   
   # Alternative: using pip (if UV is not available)
   pip install -e .
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file with your configuration
   cp .env.example .env
   # Edit .env with your OpenAI API key and PostgreSQL settings
   ```

5. **Initialize the database**
   ```bash
   # Seed database with sample data and generate embeddings
   uv run python scripts/seed.py
   ```

6. **Start the FastAPI server**
   ```bash
   # Run the FastAPI server
   uv run python app/main.py
   ```

   The server will start and be available at:
   - **Main API**: <http://localhost:8080>
   - **Interactive API Documentation**: <http://localhost:8080/docs>
   - **Alternative API Documentation**: <http://localhost:8080/redoc>

7. **Test the API**
   ```bash
   # Test a support query via API
   curl -X POST "http://localhost:8080/agent/query" \
        -H "Content-Type: application/json" \
        -d '{
          "user_id": 3,
          "query": "My account is not working properly, please help me!"
        }'
   ```

## 🌐 API Documentation

When you run the application, a FastAPI server starts automatically on `http://localhost:8080`. You can interact with the API in several ways:

### Interactive Documentation

- **Swagger UI**: Visit `http://localhost:8080/docs` for an interactive API interface
- **ReDoc**: Visit `http://localhost:8080/redoc` for alternative documentation

### Available Endpoints

#### Support Agent Endpoints
- `POST /agent/query`: Submit a support query and get AI-powered assistance

#### FAQ Management Endpoints
- `GET /faq/`: Get all FAQs
- `GET /faq/{category}`: Get FAQs by category
- `POST /faq/`: Create a new FAQ
- `PUT /faq/{faq_id}`: Update an existing FAQ
- `DELETE /faq/{faq_id}`: Delete an FAQ

#### System Endpoints
- `GET /health`: Check if the server is running
- `GET /`: Basic server information

### API Usage Examples

```bash
# Test the support endpoint with RAG
curl -X POST "http://localhost:8080/agent/query" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 1,
       "query": "What is your refund policy?"
     }'

# Get all FAQs
curl -X GET "http://localhost:8080/faq/"

# Get FAQs by category
curl -X GET "http://localhost:8080/faq/billing"

# Create a new FAQ
curl -X POST "http://localhost:8080/faq/" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "How do I change my email address?",
       "answer": "You can update your email in account settings.",
       "category": "general"
     }'
```

### Response Format

Support agent response:
```json
{
  "user_id": 1,
  "query": "What is your refund policy?",
  "support_advice": "We offer a 30-day money-back guarantee for all subscription plans. You can request a refund through your account settings or by contacting our support team.",
  "escalation_required": false,
  "risk_level": 2
}
```

## 📋 Usage Examples

### Basic Support Query with RAG

```python
from app.agent import support_agent, SupportDependencies
from app.database import DataconnectionUser, DataconnectionFaq

# Create dependencies
deps = SupportDependencies(
    user_id=3,
    db=DataconnectionUser(),
    faqdb=DataconnectionFaq()
)

# Run the support agent with RAG capabilities
result = await support_agent.run(
    "What is your refund policy?",
    deps=deps,
)

print(f"Support Advice: {result.output.support_advice}")
print(f"Escalation Required: {result.output.escalation_required}")
print(f"Risk Level: {result.output.risk_level}")
```

### Sample Output

```text
Support Advice: We offer a 30-day money-back guarantee for all subscription plans. You can request a refund through your account settings or by contacting our support team directly.

Escalation Required: False
Risk Level: 2
```

## 🗃️ Database Schema

The system uses PostgreSQL with pgvector extension for advanced vector operations:

### Tables Structure

1. **Users Table**
   ```sql
   CREATE TABLE users (
       user_id INTEGER PRIMARY KEY,
       name VARCHAR NOT NULL,
       email VARCHAR UNIQUE NOT NULL,
       account_status VARCHAR NOT NULL,  -- 'active', 'inactive', 'suspended'
       subscription_plan VARCHAR NOT NULL  -- 'free', 'basic', 'premium', 'enterprise'
   );
   ```

2. **FAQs Table with Vector Embeddings**
   ```sql
   CREATE TABLE faqs (
       id INTEGER PRIMARY KEY,
       question TEXT NOT NULL,
       answer TEXT NOT NULL,
       category VARCHAR NOT NULL,  -- 'billing', 'technical', 'general'
       embedding VECTOR(1536)  -- OpenAI embeddings for semantic search
   );
   ```

### Sample Data

The database comes pre-seeded with test users and vectorized FAQs:

| User ID | Name   | Email              | Status   | Plan       |
|---------|--------|--------------------|----------|------------|
| 1       | Alice  | alice@gmail.com    | active   | premium    |
| 2       | Bob    | bob@gmail.com      | active   | basic      |
| 3       | Shalom | shalom@gmail.com   | inactive | enterprise |

## 🔧 Configuration

### Package Management with UV

This project uses [UV](https://docs.astral.sh/uv/) as the primary package manager, which provides:

- **Fast dependency resolution**: UV is significantly faster than pip
- **Reproducible builds**: `uv.lock` ensures consistent dependency versions
- **Python version management**: UV can manage Python installations
- **Virtual environment handling**: Automatic virtual environment creation and management

Common UV commands for this project:
```bash
# Install all dependencies
uv sync

# Add a new dependency
uv add package-name

# Run Python scripts
uv run python script.py

# Install the project in development mode
uv pip install -e .
```

### Environment Variables

Required configuration in `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo
OPENAI_EMBEDDING_MODEL_NAME=text-embedding-3-small

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=supportagent
POSTGRES_PASSWORD=password
POSTGRES_DB=supportagent
```

### Model Configuration

The agent is configured to use GPT-4-turbo by default. You can modify the model in `app/config.py`:

```python
class Settings(BaseSettings):
    openai_model: str = 'gpt-4-turbo'  # Change to 'gpt-3.5-turbo' for faster/cheaper responses
    openai_embedding_model_name: str = 'text-embedding-3-small'  # For RAG embeddings
```

## 🛠️ Available Tools

The support agent has access to several advanced tools:

1. **User Name Lookup**: Automatically retrieves the user's name
2. **Account Status Check**: Checks if account is active, inactive, or suspended
3. **Subscription Plan Check**: Retrieves current subscription tier
4. **FAQ Search (RAG)**: Semantic search through vectorized FAQ database using embeddings
5. **Smart Escalation**: AI-driven decision making for human escalation

## 📁 Project Structure

```text
SupportAgent/
├── app/                   # Main application package
│   ├── __init__.py       # Package initialization
│   ├── agent.py          # Main AI agent with RAG implementation
│   ├── api.py            # FastAPI API endpoints for agent and FAQ management
│   ├── config.py         # Configuration settings and environment management
│   ├── database.py       # PostgreSQL configuration with pgvector integration
│   ├── main.py           # FastAPI application entry point
│   └── models.py         # Pydantic models for API requests and responses
├── data/                 # Data storage (if needed for local files)
├── scripts/              # Utility scripts
│   └── seed.py           # Database seeding with vectorized FAQs
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock               # UV lockfile for reproducible builds
├── .env                  # Environment variables (create from .env.example)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This documentation
```

## 🔍 Testing

### Run Support Agent

```bash
uv run python app/main.py
```

## 🚀 Advanced Usage

### Custom Support Scenarios

You can test different support scenarios using the RAG-enabled agent:

```python
# Billing inquiry with semantic search
result = await support_agent.run(
    "I want to know about refunds",
    deps=deps,
)

# Technical issue
result = await support_agent.run(
    "The application keeps crashing when I try to login",
    deps=deps,
)

# Account access issue with escalation
result = await support_agent.run(
    "I can't access my account and I'm losing business",
    deps=deps,
)
```

### Extending Functionality

To add new tools or capabilities:

1. **Add new tools** in `app/agent.py`:

   ```python
   @support_agent.tool
   async def check_billing_history(ctx: RunContext[SupportDependencies]) -> str:
       # Implementation here
       pass
   ```

2. **Extend the database model** in `app/database.py`:

   ```python
   class User(Base):
       # ...existing fields...
       last_login = Column(DateTime)
       billing_history = Column(Text)
   ```

3. **Update the system prompt** to include new capabilities

### Working with Vector Embeddings

The system automatically generates and stores embeddings for FAQ content:

```python
from app.agent import generate_embedding
from app.database import DataconnectionFaq

# Generate embedding for new content
embedding = await generate_embedding("How do I reset my password?")

# Search similar content using vector similarity
results = await DataconnectionFaq.search_by_embedding(embedding, limit=5)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Pydantic-AI](https://github.com/pydantic/pydantic-ai) for the excellent AI agent framework
- [OpenAI](https://openai.com/) for the powerful language models and embeddings
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM capabilities
- [pgvector](https://github.com/pgvector/pgvector) for PostgreSQL vector operations
- [FastAPI](https://fastapi.tiangolo.com/) for the modern API framework

## 📧 Support

If you have questions or need help:

- Open an issue on GitHub
- Check the existing documentation
- Review the example usage in the API documentation
- Test endpoints using the interactive docs at `/docs`

---

**Note**: Remember to keep your OpenAI API key secure and never commit it to version control. The `.env` file is included in `.gitignore` for this reason. Make sure to set up PostgreSQL with the pgvector extension before running the application.