"""A07: same question, several models: answer, speed, tokens and cost.
   Fill PRICES (USD per 1 million tokens) from https://aws.amazon.com/bedrock/pricing/ for us-east-1."""
import sys, time
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import boto3
from config import REGION, NOVA, CLAUDE

MODELS = {"Amazon Nova 2 Lite": NOVA, "Claude Sonnet": CLAUDE, "OpenAI gpt-oss-120b": "openai.gpt-oss-120b-1:0"}
PRICES = {  # (input, output) per 1M tokens, copy from the pricing page
    "Amazon Nova 2 Lite": (None, None),
    "Claude Sonnet": (None, None),
    "OpenAI gpt-oss-120b": (None, None),
}
QUESTION = "A customer's order #1042 is 3 days late. Write a short, warm reply and offer the code LATE10."

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
for name, model in MODELS.items():
    t = time.time()
    r = bedrock.converse(modelId=model, messages=[{"role": "user", "content": [{"text": QUESTION}]}],
                         inferenceConfig={"maxTokens": 300})
    s = time.time() - t
    u = r["usage"]
    text = next(b["text"] for b in r["output"]["message"]["content"] if "text" in b)
    pin, pout = PRICES[name]
    cost = f"${(u['inputTokens'] * pin + u['outputTokens'] * pout) / 1e6:.5f}" if pin else "fill PRICES"
    print(f"\n=== {name} · {s:.1f} s · {u['inputTokens']} in / {u['outputTokens']} out · {cost}")
    print(text.strip())
