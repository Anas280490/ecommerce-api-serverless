import os
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

client = MongoClient(os.environ["MONGODB_URL"])
db = client["ecommerce"]
products_collection = db["products"]


def main(event):
    product_id = event.get("id")

    if not product_id:
        return {
            "statusCode": 400,
            "body": {"error": "Missing required parameter: id"}
        }

    try:
        object_id = ObjectId(product_id)
    except (InvalidId, Exception):
        return {
            "statusCode": 400,
            "body": {
                "error": (
                    f"'{product_id}' is not a valid product ID. "
                    "IDs look like: 507f1f77bcf86cd799439011"
                )
            }
        }

    product = products_collection.find_one({"_id": object_id})

    if product is None:
        return {
            "statusCode": 404,
            "body": {"error": f"Product {product_id} not found"}
        }

    products_collection.delete_one({"_id": object_id})

    return {
        "body": {
            "message": f"Product '{product['name']}' deleted successfully."
        }
    }