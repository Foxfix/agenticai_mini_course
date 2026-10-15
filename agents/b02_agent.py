"""B02: your first AI agent: Strands Agents + a model on Amazon Bedrock + two Python tools."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from strands import Agent
from strands.models import BedrockModel
from config import REGION, CLAUDE
from agents.store_tools import get_order_status, read_return_policy

agent = Agent(
    model=BedrockModel(model_id=CLAUDE, region_name=REGION),
    system_prompt="You are BrightCart's support agent. Always look up an order before answering about it. Be short and warm.",
    tools=[get_order_status, read_return_policy],
)

question = " ".join(sys.argv[1:]) or "My order 1042 is late. What can you do for me?"
result = agent(question)

print("\n\n--- what happened ---")
print("tools used:", list(result.metrics.tool_metrics))
print("loop cycles:", result.metrics.cycle_count)
