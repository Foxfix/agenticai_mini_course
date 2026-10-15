"""A07: prompt caching: send the same long store handbook twice, the second time it's read from cache."""
import sys, glob, time
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import boto3
from config import REGION, CLAUDE, DATA

handbook = "\n\n".join(open(p).read() for p in sorted(glob.glob(f"{DATA}/docs/*.md")))
bedrock = boto3.client("bedrock-runtime", region_name=REGION)
SYSTEM = [{"text": "You are BrightCart's support assistant. Use this handbook:\n\n" + handbook},
          {"cachePoint": {"type": "default"}}]

for q in ["Can I return opened earbuds after 20 days?", "How long does a refund take?"]:
    t = time.time()
    r = bedrock.converse(modelId=CLAUDE, system=SYSTEM, messages=[{"role": "user", "content": [{"text": q}]}],
                         inferenceConfig={"maxTokens": 200})
    u = r["usage"]
    print(f"\nQ: {q}\n{time.time() - t:.1f} s · input {u['inputTokens']} · cache write {u.get('cacheWriteInputTokens', 0)} · cache read {u.get('cacheReadInputTokens', 0)}")
    print("A:", r["output"]["message"]["content"][0]["text"].strip())
