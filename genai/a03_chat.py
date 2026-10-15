"""A03: a support chatbot in the terminal: system prompt, memory of the conversation, streaming."""
import sys
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import boto3
from config import REGION, MODEL_ID

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
SYSTEM = [{"text": "You are the friendly support assistant of BrightCart, an online electronics store. Answer in 3 short sentences or less."}]
history = []

print("BrightCart support (type 'quit' to exit)")
while True:
    question = input("\nYou: ").strip()
    if question.lower() in ("quit", "exit"):
        break
    history.append({"role": "user", "content": [{"text": question}]})

    stream = bedrock.converse_stream(modelId=MODEL_ID, system=SYSTEM, messages=history,
                                     inferenceConfig={"maxTokens": 400, "temperature": 0.3})
    print("Bot: ", end="", flush=True)
    answer = ""
    for event in stream["stream"]:
        if "contentBlockDelta" in event:
            piece = event["contentBlockDelta"]["delta"].get("text", "")
            answer += piece
            print(piece, end="", flush=True)
    print()
    history.append({"role": "assistant", "content": [{"text": answer}]})
