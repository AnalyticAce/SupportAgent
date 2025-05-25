from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.config import settings
from app.database import DataconnectionUser, DataconnectionFaq
from openai import AsyncOpenAI

embedding_client = AsyncOpenAI(api_key=settings.openai_api_key)

@dataclass
class SupportDependencies:
   user_id: int
   db: DataconnectionUser
   faqdb: DataconnectionFaq = None


class SupportResult(BaseModel):
   support_advice: str = Field(description="Advice returned to the user")
   escalation_required: bool = Field(default=False, description="Indicates if we need to escalate the query to an admin")
   risk_level: int = Field(description="Risk level of the query", ge=0, le=10)


model = OpenAIModel(
   model_name=settings.openai_model,
   provider=OpenAIProvider(api_key=settings.openai_api_key),
)


support_agent = Agent(
   model=model,
   deps_type=SupportDependencies,
   result_type=SupportResult,
   system_prompt=(
      "You are a friendly and professional customer support agent for a SaaS platform. "
      "Your job is to help users with account issues, subscription plans, billing, and technical questions. "
      "When a question can be answered using internal documentation or FAQ articles, use the `faq_search` tool "
      "to retrieve relevant content. Then, based on what you find, respond to the user in your own words. "
      "Do not copy-paste content directly from the documents—always rephrase and present the answer clearly, "
      "politely, and in a helpful tone. "
      "If the question cannot be answered using the tools, escalate only when necessary. "
      "Keep your answers concise, conversational, and easy to understand, like a real customer service agent would."
   ),
   retries=2
)


async def generate_embedding(text: str) -> list[float]:
   response = await embedding_client.embeddings.create(
      model=settings.openai_embedding_model_name, input=text
   )
   return response.data[0].embedding


@support_agent.system_prompt
async def add_user_name(ctx: RunContext[SupportDependencies]) -> str:
   user_name = await ctx.deps.db.user_name(ctx.deps.user_id)
   return f"User name is {user_name!r}.\n\n"


@support_agent.system_prompt
async def example_faq_usage(_: RunContext[SupportDependencies]) -> str:
   return (
      "Example: If the user asks about refunds, you can use `faq_search('refund policy')` "
      "to retrieve relevant documentation from the FAQ database.\n"
   )


@support_agent.tool
async def check_account_status(ctx: RunContext[SupportDependencies]) -> str:
   account_status = await ctx.deps.db.account_status(ctx.deps.user_id)
   return f"User account status is {account_status!r}.\n\n"


@support_agent.tool
async def check_subscription_plan(ctx: RunContext[SupportDependencies]) -> str:
   subscription_plan = await ctx.deps.db.subscription_plan(ctx.deps.user_id)
   return f"User subscription plan is {subscription_plan!r}.\n\n"


def format_faq_results(rows) -> str:
   return "\n\n".join(
      f"## {row['question']}\nCategory: {row['category']}\n\n{row['answer']}"
      for row in rows
   )


@support_agent.tool
async def faq_search(ctx: RunContext[SupportDependencies], query: str, top_k=3) -> str:
   print(f"Calling FAQ search with query: {query}")
   embedding = await generate_embedding(query)
   rows = await ctx.deps.faqdb.search_by_embedding(embedding, limit=top_k)
   print(format_faq_results(rows))
   return format_faq_results(rows)
