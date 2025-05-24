import asyncio
from agent import Dataconnection, SupportDependencies, support_agent


def main():
    deps = SupportDependencies(
        user_id=3,
        db=Dataconnection()
    )

    result = support_agent.run_sync(
        "What is my is not longer working I dont know why, please help me ?",
        deps=deps,
    )

    print(f"Support Advice: {result.output.support_advice}")
    print(f"Escalation Required: {result.output.escalation_required}")
    print(f"Risk Level: {result.output.risk_level}")

if __name__ == "__main__":  
    main()
