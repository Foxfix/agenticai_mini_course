"""A02: your first call to Amazon Bedrock from Python (Converse API)."""
import sys, time
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import boto3
from config import REGION, MODEL_ID

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

start = time.time()
response = bedrock.converse(
    modelId=MODEL_ID,
    messages=[{"role": "user", "content": [{"text": "Write a one-line welcome message for BrightCart, an online electronics store."}]}],
    inferenceConfig={"maxTokens": 200, "temperature": 0.5},
)
seconds = time.time() - start

print("Model:", MODEL_ID)
print("Answer:", response["output"]["message"]["content"][0]["text"])
usage = response["usage"]
print(f"Tokens: {usage['inputTokens']} in, {usage['outputTokens']} out · {seconds:.1f} s")
