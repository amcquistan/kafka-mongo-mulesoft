from pymongo import MongoClient


def customer_revenue(db_client, db_name, src_collection, dst_collection):
    db = db_client[db_name]
    db_collection = db[src_collection]
    db_collection.aggregate([
        {
            "$project": {
                "customer_name": { "$concat": ["$customer.first_name", " ", "$customer.last_name"] },
                "product_revenue": { "$multiply": ["items.product.price", "items.quantity"] }
            }
        },
        {
            "$group": {
                "_id": "$customer_name",
                "revenue": { "$sum": "$product_revenue" }
            }
        }
    ])



def product_revenue(db_client, db_name, src_collection, dst_collection):
    pass
