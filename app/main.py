from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import support_agent, SupportDependencies, Dataconnection

app = FastAPI(
    title="Support Agent API",
    description="A simple API to query the AI support agent",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    user_id: int
    query: str

class QueryResponse(BaseModel):
    user_id: int
    query: str
    support_advice: str
    escalation_required: bool
    risk_level: int

@app.get("/")
async def root():
    return {"message": "Support Agent API is running"}

@app.post("/query", response_model=QueryResponse)
async def query_support_agent(request: QueryRequest):
    """
    Query the support agent with a user question and get structured response
    """
    try:
        # Create dependencies for the agent
        deps = SupportDependencies(
            user_id=request.user_id,
            db=Dataconnection()
        )
        
        # Run the agent with the user's query
        result = await support_agent.run(request.query, deps=deps)
        
        # Return structured response
        return QueryResponse(
            user_id=request.user_id,
            query=request.query,
            support_advice=result.output.support_advice,
            escalation_required=result.output.escalation_required,
            risk_level=result.output.risk_level
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "support-agent-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
