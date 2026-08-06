import os
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

client = MongoClient(os.environ["MONGODB_URL"])
db = client["ecommerce"]
products_collection = db["products"]


def product_helper(product):
    return {
        "id": str(product["_id"]),
        "name": product.get("name", ""),
        "description": product.get("description", ""),
        "price": product.get("price", 0.0),
        "category": product.get("category", ""),
        "brand": product.get("brand", "Unknown"),
        "sku": product.get("sku", ""),
        "in_stock": product.get("in_stock", True),
        "stock_count": product.get("stock_count", 0),
        "rating": product.get("rating", 0.0),
        "tags": product.get("tags", []),
    }


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
            "body": {"error": f"'{product_id}' is not a valid product ID."}
        }

    ignored_keys = {
        "id",
        "__ow_method",
        "__ow_path",
        "__ow_headers",
        "__ow_body",
        "__ow_query",
        "http"
    }

    update_data = {
        key: value
        for key, value in event.items()
        if key not in ignored_keys and value is not None
    }

    if not update_data:
        return {
            "statusCode": 400,
            "body": {"error": "No fields to update."}
        }

    result = products_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return {
            "statusCode": 404,
            "body": {"error": f"Product {product_id} not found"}
        }

    updated_product = products_collection.find_one({"_id": object_id})

    return {"body": product_helper(updated_product)}