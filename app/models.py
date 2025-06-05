from pydantic import BaseModel

class QueryRequest(BaseModel):
    """Request model for submitting a support query to the AI agent."""
    user_id: int
    query: str

class QueryResponse(BaseModel):
    """Response model for the AI agent's support query response."""
    user_id: int
    query: str
    support_advice: str
    escalation_required: bool
    risk_level: int
    

class FaqCreateRequest(BaseModel):
    """Request model for creating a new FAQ entry."""
    question: str
    answer: str
    category: str