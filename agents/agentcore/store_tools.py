"""BrightCart tools for the deployed agent (copy this file + the data/ folder into app/StoreAgent/)."""
import json, os
from strands import tool

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


@tool
def get_order_status(order_id: str) -> str:
    """Look up a BrightCart order by its id. Returns the item, status and delivery date."""
    orders = json.load(open(os.path.join(DATA, "orders.json")))
    order = orders.get(order_id.strip("# "))
    return json.dumps(order) if order else f"Order {order_id} not found"


@tool
def read_return_policy() -> str:
    """Read BrightCart's return policy: return windows, late-order discounts and refunds."""
    return open(os.path.join(DATA, "docs", "return-policy.md")).read()
