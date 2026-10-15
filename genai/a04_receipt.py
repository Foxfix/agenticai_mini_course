"""A04: image in, JSON out: read a receipt photo and return structured data."""
import sys, json
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import boto3
from config import REGION, CLAUDE, DATA

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
image = open(f"{DATA}/receipt.png", "rb").read()

schema = {
    "type": "object",
    "properties": {
        "store": {"type": "string"},
        "date": {"type": "string", "description": "YYYY-MM-DD"},
        "items": {"type": "array", "items": {"type": "object", "properties": {
            "name": {"type": "string"}, "quantity": {"type": "integer"}, "price": {"type": "number"}},
            "required": ["name", "quantity", "price"], "additionalProperties": False}},
        "total": {"type": "number"},
    },
    "required": ["store", "date", "items", "total"],
    "additionalProperties": False,
}

response = bedrock.converse(
    modelId=CLAUDE,
    messages=[{"role": "user", "content": [
        {"image": {"format": "png", "source": {"bytes": image}}},
        {"text": "Read this receipt and extract the data."},
    ]}],
    outputConfig={"textFormat": {"type": "json_schema", "structure": {"jsonSchema": {
        "name": "receipt", "schema": json.dumps(schema)}}}},
)

data = json.loads(response["output"]["message"]["content"][0]["text"])
print(json.dumps(data, indent=2))
print("Items:", len(data["items"]), "· total:", data["total"])
