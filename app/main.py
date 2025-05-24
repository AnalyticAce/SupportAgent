from fastapi import FastAPI
from app.api import agent_router, faq_router

app = FastAPI(
    title="Support Agent API",
    description="A simple API to query the AI support agent",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Support Agent API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "support-agent-api"}


app.include_router(agent_router)
app.include_router(faq_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
