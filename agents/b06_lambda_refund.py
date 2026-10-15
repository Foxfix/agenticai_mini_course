# B06: AWS Lambda function "brightcart-create-refund" (paste into the Lambda console, runtime Python 3.13+).
# AgentCore Gateway calls it with the tool arguments as the event.
import json, uuid

APPROVAL_LIMIT = 300  # USD, above this a human must approve (store playbook)


def lambda_handler(event, context):
    order_id = str(event.get("order_id", ""))
    amount = float(event.get("amount", 0))
    reason = event.get("reason", "")

    if amount > APPROVAL_LIMIT:
        result = {"status": "needs_human_approval", "order_id": order_id, "amount": amount,
                  "message": "A support agent will confirm this refund by email within 1 business day."}
    else:
        result = {"status": "refund_created", "refund_id": "RF-" + uuid.uuid4().hex[:8].upper(),
                  "order_id": order_id, "amount": amount, "reason": reason,
                  "message": "Refund goes back to the original payment method in 5 to 7 business days."}

    print(json.dumps(result))  # visible in CloudWatch Logs
    return result
