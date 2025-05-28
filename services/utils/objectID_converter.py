from bson import ObjectId

def convert_objectid_to_string(items: list[dict]) -> list[dict]:
    for item in items:
        if "_id" in item and isinstance(item["_id"], ObjectId):
            item["_id"] = str(item["_id"])
    return items