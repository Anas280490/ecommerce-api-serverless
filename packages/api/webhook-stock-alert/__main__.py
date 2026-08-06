from datetime import datetime, timezone


def main(event):
    full_document = event.get("fullDocument", {})
    product_name = full_document.get("name", "Unknown")
    stock_count = full_document.get("stock_count", "N/A")

    timestamp = datetime.now(timezone.utc).isoformat()

    print(
        f"🚨 [{timestamp}] STOCK ALERT: "
        f"'{product_name}' — stock = {stock_count}"
    )

    return {
        "body": {
            "received": True,
            "timestamp": timestamp,
            "product": product_name,
            "stock_count": stock_count,
            "action": "Alert logged to DO Functions console"
        }
    }