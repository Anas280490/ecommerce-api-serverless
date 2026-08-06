def main(event):
    return {
        "body": {
            "message": "E-Commerce Products API (Serverless) is running",
            "docs": "Use /api/products-list, /api/products-create, etc.",
            "version": "2.0.0",
            "runtime": "DigitalOcean Functions"
        }
    }