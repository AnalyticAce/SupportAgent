from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.config import settings
from app.database import DataconnectionUser

@dataclass
class SupportDependencies:
   user_id: int
   db: DataconnectionUser


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
      "Your are a SaaS support agent. Help users with their account,"
      "check subscription plans, account status and user query to check if it needs to be escalated to an admin."
   ),
   retries=2
)


@support_agent.system_prompt
async def add_user_name(ctx: RunContext[SupportDependencies]) -> str:
   user_name = await ctx.deps.db.user_name(ctx.deps.user_id)
   return f"User name is {user_name!r}.\n\n"


@support_agent.tool
async def check_account_status(ctx: RunContext[SupportDependencies]) -> str:
   account_status = await ctx.deps.db.account_status(ctx.deps.user_id)
   return f"User account status is {account_status!r}.\n\n"


@support_agent.tool
async def check_subscription_plan(ctx: RunContext[SupportDependencies]) -> str:
   subscription_plan = await ctx.deps.db.subscription_plan(ctx.deps.user_id)
   return f"User subscription plan is {subscription_plan!r}.\n\n"