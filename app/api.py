import asyncio
from fastapi import APIRouter, HTTPException
from app.agent import support_agent, SupportDependencies
from app.database import DataconnectionFaq, DataconnectionUser
from app.models import (
    QueryRequest,
    QueryResponse,
    FaqCreateRequest
)


faq_router = APIRouter(
    prefix="/faq",
    tags=["FAQ"]
)


agent_router = APIRouter(
    prefix="/agent",
    tags=["Support Agent"]
)


@agent_router.post("/query", response_model=QueryResponse)
async def query_support_agent(request: QueryRequest):
    """
    Query the support agent with a user question and get structured response
    """
    try:
        deps = SupportDependencies(
            user_id=request.user_id,
            db=DataconnectionUser()
        )

        result = asyncio.run(support_agent.run(request.query, deps=deps))
        
        if not result or not result.output:
            raise HTTPException(status_code=500, detail="No response from support agent")
        
        return QueryResponse(
            user_id=request.user_id,
            query=request.query,
            support_advice=result.output.support_advice,
            escalation_required=result.output.escalation_required,
            risk_level=result.output.risk_level
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@faq_router.get("/", response_model=dict)
async def get_faqs():
    try:
        faqs = await DataconnectionFaq.get_faqs()
        
        if not faqs:
            raise HTTPException(status_code=404, detail="No FAQs found")
        
        return {"faqs": faqs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving FAQs: {str(e)}")


@faq_router.get("/{category}")
async def get_faq_by_category(category: str):
    try:
        faqs = await DataconnectionFaq.get_faq_by_category(category)
        
        if not faqs:
            raise HTTPException(status_code=404, detail=f"No FAQs found for category '{category}'")
        
        return {"faqs": faqs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving FAQs for category '{category}': {str(e)}")


@faq_router.post("/", response_model=FaqCreateRequest)
async def create_faq(faq: FaqCreateRequest):
    try:
        await DataconnectionFaq.add_faq(faq.question, faq.answer, faq.category)
        return FaqCreateRequest(
            question=faq.question,
            answer=faq.answer,
            category=faq.category
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating FAQ: {str(e)}")


@faq_router.put("/{faq_id}", response_model=FaqCreateRequest)
async def update_faq(faq_id: int, faq: FaqCreateRequest):
    try:
        updated_faq = await DataconnectionFaq.update_faq(faq_id, faq.question, faq.answer, faq.category)
        if not updated_faq:
            raise HTTPException(status_code=404, detail=f"FAQ with id {faq_id} not found")
        return updated_faq
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating FAQ: {str(e)}")


@faq_router.delete("/{faq_id}")
async def delete_faq(faq_id: int):
    try:
        result = await DataconnectionFaq.delete_faq(faq_id)
        if "message" in result:
            return {"message": result["message"]}
        else:
            raise HTTPException(status_code=404, detail=f"FAQ with id {faq_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting FAQ: {str(e)}")

