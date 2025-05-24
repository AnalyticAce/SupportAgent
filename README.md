# SupportAgent 🤖

An intelligent AI-powered SaaS support agent built with OpenAI GPT-4 and Pydantic-AI. This project demonstrates how to create an automated customer support system that can handle user queries, check account statuses, manage subscriptions, and determine when to escalate issues to human administrators.

> [!NOTE]
> This is a simple implementation designed to serve as a foundation that can evolve >with multiple features. The current version provides basic functionality for AI-powered >support, with an extensible architecture that allows for easy addition of new capabilities, >tools, and integrations as your support requirements grow.

## 🌟 Features

- **AI-Powered Support**: Uses OpenAI's GPT-4 model for natural language understanding and response generation
- **Account Management**: Automatically checks user account status and subscription plans
- **Smart Escalation**: Determines when issues need to be escalated to human administrators
- **Risk Assessment**: Provides risk level scoring (0-10) for support queries
- **Database Integration**: SQLAlchemy-based user data management with SQLite
- **Structured Responses**: Uses Pydantic models for consistent, validated outputs
- **FastAPI Server**: Built-in web server with interactive API documentation
- **REST API**: HTTP endpoints for integration with external applications

## 🏗️ Architecture

The support agent is built using several key components:

- **Agent (`app/agent.py`)**: Core AI agent using Pydantic-AI framework
- **Database (`app/database.py`)**: SQLAlchemy setup for user data persistence
- **Models (`app/models.py`)**: User data model definitions
- **Main (`app/main.py`)**: Example usage and entry point
- **Config (`app/config.py`)**: Configuration settings and environment management
- **Seed (`scripts/seed.py`)**: Database seeding with sample users

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- OpenAI API key
- [UV package manager](https://docs.astral.sh/uv/) (fast Python package installer and resolver)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SupportAgent
   ```

2. **Install dependencies**
   ```bash
   # Install dependencies with UV (main package manager)
   uv sync
   
   # Alternative: using pip (if UV is not available)
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY='your-openai-api-key-here'" > .env
   ```

4. **Initialize the database**
   ```bash
   uv run python scripts/seed.py
   ```

5. **Start the FastAPI server**
   ```bash
   # Run the FastAPI server
   uv run python app/main.py
   ```

   The server will start and be available at:
   - **Main API**: http://localhost:8000
   - **Interactive API Documentation**: http://localhost:8000/docs
   - **Alternative API Documentation**: http://localhost:8000/redoc

6. **Test the API**
   ```bash
   # Test a support query via API
   curl -X POST "http://localhost:8000/support" \
        -H "Content-Type: application/json" \
        -d '{
          "user_id": 3,
          "message": "My account is not working properly, please help me!"
        }'
   ```

## 🌐 API Documentation

When you run the application, a FastAPI server starts automatically on `http://localhost:8000`. You can interact with the API in several ways:

### Interactive Documentation
- **Swagger UI**: Visit `http://localhost:8000/docs` for an interactive API interface
- **ReDoc**: Visit `http://localhost:8000/redoc` for alternative documentation

### Available Endpoints
- `POST /support`: Submit a support query and get AI-powered assistance
- `GET /health`: Check if the server is running
- `GET /`: Basic server information

### API Usage Example

```bash
# Test the support endpoint
curl -X POST "http://localhost:8000/support" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 1,
       "message": "I need help with my subscription"
     }'
```

### Response Format

```json
{
  "support_advice": "I can help you with your subscription...",
  "escalation_required": false,
  "risk_level": 3,
  "user_name": "Alice"
}
```

## 📋 Usage Examples

### Basic Support Query

```python
from app.agent import Dataconnection, SupportDependencies, support_agent

# Create dependencies
deps = SupportDependencies(
    user_id=3,
    db=Dataconnection()
)

# Run the support agent
result = support_agent.run_sync(
    "My account is not working properly, please help me!",
    deps=deps,
)

print(f"Support Advice: {result.output.support_advice}")
print(f"Escalation Required: {result.output.escalation_required}")
print(f"Risk Level: {result.output.risk_level}")
```

### Sample Output

```
Support Advice: I can see that your account (Shalom) is currently inactive. This is likely why you're experiencing issues. I recommend contacting our billing team to reactivate your Enterprise subscription. You can also check your payment method or reach out to support for immediate assistance.

Escalation Required: True
Risk Level: 7
```

## 🗃️ Database Schema

The system uses a simple SQLite database with the following user structure:

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    account_status VARCHAR NOT NULL,  -- 'active', 'inactive', 'suspended'
    subscription_plan VARCHAR NOT NULL  -- 'free', 'basic', 'premium', 'enterprise'
);
```

### Sample Data

The database comes pre-seeded with test users:

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

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Model Configuration

The agent is configured to use GPT-4o by default. You can modify the model in `app/agent.py`:

```python
model = OpenAIModel(
    'gpt-4o',  # Change to 'gpt-3.5-turbo' for faster/cheaper responses
    provider=OpenAIProvider(api_key=api_key)
)
```

## 🛠️ Available Tools

The support agent has access to several tools:

1. **User Name Lookup**: Automatically retrieves the user's name
2. **Account Status Check**: Checks if account is active, inactive, or suspended
3. **Subscription Plan Check**: Retrieves current subscription tier

## 📁 Project Structure

```
SupportAgent/
├── app/                   # Main application package
│   ├── __init__.py       # Package initialization
│   ├── agent.py          # Main AI agent implementation
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database configuration
│   ├── main.py           # Example usage and entry point
│   └── models.py         # SQLAlchemy models
├── data/                  # Data storage
│   └── support.db        # SQLite database
├── scripts/               # Utility scripts
│   └── seed.py           # Database seeding script
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock               # UV lockfile for reproducible builds
├── .env                  # Environment variables (create this file)
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

You can test different support scenarios by modifying the query in `app/main.py`:

```python
# Billing inquiry
result = support_agent.run_sync(
    "I want to upgrade my subscription plan",
    deps=deps,
)

# Technical issue
result = support_agent.run_sync(
    "The application keeps crashing when I try to login",
    deps=deps,
)

# Account access issue
result = support_agent.run_sync(
    "I can't access my account anymore",
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

2. **Extend the database model** in `app/models.py`:
```python
class User(Base):
    # ...existing fields...
    last_login = Column(DateTime)
    billing_history = Column(Text)
```

3. **Update the system prompt** to include new capabilities

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
- [OpenAI](https://openai.com/) for the powerful language models
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM capabilities

## 📧 Support

If you have questions or need help:
- Open an issue on GitHub
- Check the existing documentation
- Review the example usage in `app/main.py`

---

**Note**: Remember to keep your OpenAI API key secure and never commit it to version control. The `.env` file is included in `.gitignore` for this reason.