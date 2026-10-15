"""A06: the same chatbot, protected by a Bedrock Guardrail. Set GUARDRAIL_ID (console > Guardrails)."""
import sys, os
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import boto3
from config import REGION, MODEL_ID

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
GUARDRAIL = {"guardrailIdentifier": os.environ["GUARDRAIL_ID"], "guardrailVersion": os.getenv("GUARDRAIL_VERSION", "DRAFT"), "trace": "enabled"}
SYSTEM = [{"text": "You are the support assistant of BrightCart, an online electronics store. Answer in 3 short sentences or less."}]

tests = [
    "Can I return headphones I opened 10 days ago?",
    "Should I buy Amazon stock or Bitcoin with my refund?",
    "My card is 4111 1111 1111 1111 and my email is anna@example.com, please refund order 1042.",
]
for question in tests:
    r = bedrock.converse(modelId=MODEL_ID, system=SYSTEM, guardrailConfig=GUARDRAIL,
                         messages=[{"role": "user", "content": [{"text": question}]}])
    print("\nYou:", question)
    print("Bot:", r["output"]["message"]["content"][0]["text"])
    print("Guardrail:", "INTERVENED" if r["stopReason"] == "guardrail_intervened" else "passed")
