from pymongo import MongoClient


def customer_revenue(db_client, db_name, src_collection, dst_collection):
    db = db_client[db_name]
    db_collection = db[src_collection]
    db_collection.aggregate([
        {
            "$project": {
                "customer": { "$concat": ["$customer.first_name", " ", "$customer.last_name"] },
                "revenue": {
                    "$map": {
                        "input": "$items",
                        "as": "item",
                        "in": {
                            "item_product": "$$item.product.name",
                            "item_revenue": {
                                "$multiply": ["$$item.product.price", "$$item.quantity"]
                            }
                        }
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$customer",
                "revenue": {
                    "$sum": { "$sum": "$revenue.item_revenue" }
                }
            }
        },
        {
            "$merge": {
                "into": "customer_revenue"
            }
        }
    ])



def product_revenue(db_client, db_name, src_collection, dst_collection):
    pass
