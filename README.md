# BrightCart: AWS AI examples

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    aws login

- `config.py`: region and model IDs (one place to change them)
- `data/`: orders, company docs (RAG, caching), receipt.png
- `genai/`: A02-A07 (Amazon Bedrock)
- `agents/`: B02-B07 (Strands Agents, AgentCore)
- `kiro/brightcart-api`: B08-B09 (Kiro)
