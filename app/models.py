from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_id: int
    query: str

class QueryResponse(BaseModel):
    user_id: int
    query: str
    support_advice: str
    escalation_required: bool
    risk_level: int
    

class FaqCreateRequest(BaseModel):
    question: str
    answer: str
    category: str
