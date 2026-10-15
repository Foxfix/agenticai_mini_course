"""B06: the store agent gets a real business action (create_refund on AWS Lambda) through AgentCore Gateway.
   export GATEWAY_URL=...   (from: agentcore fetch access)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client
from config import REGION, CLAUDE
from agents.store_tools import get_order_status, read_return_policy

gateway = MCPClient(lambda: aws_iam_streamablehttp_client(endpoint=os.environ["GATEWAY_URL"],
                                                          aws_service="bedrock-agentcore", aws_region=REGION))
with gateway:
    gateway_tools = gateway.list_tools_sync()
    print("tools from the gateway:", [t.tool_name for t in gateway_tools])
    agent = Agent(
        model=BedrockModel(model_id=CLAUDE, region_name=REGION),
        system_prompt=("You are BrightCart's support agent. Check the order and the return policy before any refund. "
                       "You may refund up to 300 USD; above that, say a human will confirm."),
        tools=[get_order_status, read_return_policy, *gateway_tools],
    )
    agent(" ".join(sys.argv[1:]) or "Order 1044: my smart watch stopped charging after 3 days. I want my money back.")
