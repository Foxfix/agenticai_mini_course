"""A05: ask questions about company documents (Managed Knowledge Base + RAG).
   Set KB_ID to your knowledge base ID (AgentCore console > Knowledge Base)."""
import sys, os
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import boto3
from config import REGION, MODEL_ID

KB_ID = os.environ["KB_ID"]
kb = boto3.client("bedrock-agent-runtime", region_name=REGION)
bedrock = boto3.client("bedrock-runtime", region_name=REGION)

question = " ".join(sys.argv[1:]) or "I opened my headphones 20 days ago. Can I still return them?"

# 1. Retrieve: find the most relevant pieces of our documents
found = kb.retrieve(knowledgeBaseId=KB_ID, retrievalQuery={"text": question},
                    retrievalConfiguration={"managedSearchConfiguration": {"numberOfResults": 3}})
chunks = found["retrievalResults"]
for i, c in enumerate(chunks, 1):
    print(f"[{i}] {c['location'].get('s3Location', {}).get('uri', '?')}")

# 2. Augment + generate: give the model ONLY those pieces and ask it to answer from them
context = "\n\n".join(f"[{i}] {c['content']['text']}" for i, c in enumerate(chunks, 1))
response = bedrock.converse(
    modelId=MODEL_ID,
    system=[{"text": "Answer only from the provided BrightCart documents. Cite sources like [1]. If the answer is not there, say you don't know."}],
    messages=[{"role": "user", "content": [{"text": f"Documents:\n{context}\n\nQuestion: {question}"}]}],
)
print("\nAnswer:", response["output"]["message"]["content"][0]["text"])
