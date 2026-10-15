"""Shared settings for the BrightCart examples. Region: us-east-1."""
import os

REGION = "us-east-1"

# Model IDs (copy the newest ones from Bedrock console > Model catalog > model card > "Inference profile ID")
NOVA = "us.amazon.nova-2-lite-v1:0"
CLAUDE = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"

MODEL_ID = os.getenv("MODEL_ID", NOVA)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
