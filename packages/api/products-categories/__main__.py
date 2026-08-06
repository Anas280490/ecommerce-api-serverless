import os
from pymongo import MongoClient

client = MongoClient(os.environ["MONGODB_URL"])
db = client["ecommerce"]
products_collection = db["products"]


def main(event):
    categories = products_collection.distinct("category")

    return {
        "body": {
            "count": len(categories),
            "categories": sorted(categories)
        }
    }