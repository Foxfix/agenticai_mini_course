"""B03: give the agent tools through MCP: the public AWS Knowledge MCP Server (no account, no key)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamable_http_client
from config import REGION, CLAUDE

aws_docs = MCPClient(lambda: streamable_http_client("https://knowledge-mcp.global.api.aws"),
                     tool_filters={"allowed": ["aws___search_documentation", "aws___read_documentation", "aws___get_regional_availability"]})

with aws_docs:
    tools = aws_docs.list_tools_sync()
    print("MCP tools the agent can use:", [t.tool_name for t in tools])
    agent = Agent(model=BedrockModel(model_id=CLAUDE, region_name=REGION), tools=tools,
                  system_prompt="You help BrightCart's developers with AWS. Use the AWS documentation tools and keep answers short.")
    agent(" ".join(sys.argv[1:]) or "Is Amazon Bedrock AgentCore available in us-east-1? Answer in 2 sentences with a doc link.")
