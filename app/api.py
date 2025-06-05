from fastapi import APIRouter, HTTPException
from app.agent import support_agent, SupportDependencies, generate_embedding
from app.database import DataconnectionFaq, DataconnectionUser
from app.models import (
    QueryRequest,
    QueryResponse,
    FaqCreateRequest
)


faq_router = APIRouter(
    prefix="/faq",
    tags=["FAQ"],
    responses={404: {"description": "FAQ not found"}}
)


agent_router = APIRouter(
    prefix="/agent",
    tags=["Support Agent"],
    responses={500: {"description": "Internal server error"}}
)


@agent_router.post(
    "/query", 
    response_model=QueryResponse,
    summary="Process Customer Support Query",
    description="Submit a customer support query to the AI agent for intelligent response generation",
    responses={
        200: {"description": "Successful query processing with AI response"},
        500: {"description": "Error processing query"}
    }
)
async def query_support_agent(request: QueryRequest):
    """
Process a customer support query using AI agent with RAG capabilities.
    """
    try:
        deps = SupportDependencies(
            user_id=request.user_id,
            db=DataconnectionUser(),
            faqdb=DataconnectionFaq()
        )

        result = await support_agent.run(request.query, deps=deps)
        
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


@faq_router.get(
    "/", 
    response_model=dict,
    summary="Get All FAQs",
    description="Retrieve all FAQ entries from the database with questions, answers, and categories",
    responses={
        200: {"description": "List of all FAQs retrieved successfully"},
        404: {"description": "No FAQs found in database"}
    }
)
async def get_faqs():
    """
Retrieve all FAQ entries from the database.
    """
    try:
        faqs = await DataconnectionFaq.get_faqs()
        
        if not faqs:
            raise HTTPException(status_code=404, detail="No FAQs found")
        
        return {"faqs": faqs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving FAQs: {str(e)}")


@faq_router.get(
    "/{category}", 
    response_model=dict,
    summary="Get FAQs by Category",
    description="Retrieve FAQ entries filtered by specific category",
    responses={
        200: {"description": "FAQs for category retrieved successfully"},
        404: {"description": "No FAQs found for the specified category"}
    }
)
async def get_faq_by_category(category: str):
    """
Retrieve FAQ entries filtered by category.
    """
    try:
        faqs = await DataconnectionFaq.get_faq_by_category(category)
        
        if not faqs:
            raise HTTPException(status_code=404, detail=f"No FAQs found for category '{category}'")
        
        return {"faqs": faqs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving FAQs for category '{category}': {str(e)}")


@faq_router.post(
    "/", 
    response_model=FaqCreateRequest,
    summary="Create New FAQ",
    description="Add a new FAQ entry with automatic vector embedding generation",
    responses={
        200: {"description": "FAQ created successfully"},
        500: {"description": "Error creating FAQ entry"}
    }
)
async def create_faq(faq: FaqCreateRequest):
    """
Create a new FAQ entry in the database.
    """
    try:
        embedding = await generate_embedding(f"{faq.question}\n{faq.answer}")
        await DataconnectionFaq.add_faq(faq.question, faq.answer, faq.category, embedding)
        return FaqCreateRequest(
            question=faq.question,
            answer=faq.answer,
            category=faq.category
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating FAQ: {str(e)}")


@faq_router.put(
    "/{faq_id}", 
    response_model=FaqCreateRequest,
    summary="Update FAQ Entry",
    description="Update an existing FAQ entry by ID with new content",
    responses={
        200: {"description": "FAQ updated successfully"},
        404: {"description": "FAQ with specified ID not found"},
        500: {"description": "Error updating FAQ entry"}
    }
)
async def update_faq(faq_id: int, faq: FaqCreateRequest):
    """
Update an existing FAQ entry by ID.
    """
    try:
        updated_faq = await DataconnectionFaq.update_faq(faq_id, faq.question, faq.answer, faq.category)
        if not updated_faq:
            raise HTTPException(status_code=404, detail=f"FAQ with id {faq_id} not found")
        return updated_faq
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating FAQ: {str(e)}")


@faq_router.delete(
    "/{faq_id}", 
    response_model=dict,
    summary="Delete FAQ Entry", 
    description="Remove an FAQ entry from the database by ID",
    responses={
        200: {"description": "FAQ deleted successfully"},
        404: {"description": "FAQ with specified ID not found"},
        500: {"description": "Error deleting FAQ entry"}
    }
)
async def delete_faq(faq_id: int):
    """
Delete an FAQ entry by ID.
    """
    try:
        result = await DataconnectionFaq.delete_faq(faq_id)
        if "message" in result:
            return {"message": result["message"]}
        else:
            raise HTTPException(status_code=404, detail=f"FAQ with id {faq_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting FAQ: {str(e)}")

