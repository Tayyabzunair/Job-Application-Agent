"""Tracks approved job applications in MongoDB Atlas."""
from datetime import datetime
from pymongo import MongoClient
from src.config import MONGODB_URI, DB_NAME, COLLECTION_NAME

# Create a single client connection (reused across calls)
_client = None
_collection = None


def _get_collection():
    """Lazy-load the MongoDB collection (connect only once)."""
    global _client, _collection
    if _collection is None:
        _client = MongoClient(MONGODB_URI)
        _collection = _client[DB_NAME][COLLECTION_NAME]
    return _collection


def log_application(result: dict) -> dict:
    """Save an approved application to MongoDB. Overwrites if same result_id exists."""
    col = _get_collection()
    entry = {
        "result_id": result["result_id"],
        "role": result["role"],
        "seniority": result.get("seniority", ""),
        "match_score": result["match_score"],
        "ats_score": result.get("ats_score", 0),
        "status": "Applied",
        "applied_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    # Upsert: replace existing entry with same result_id, or insert new one
    col.replace_one({"result_id": entry["result_id"]}, entry, upsert=True)
    return entry


def get_all_applications() -> list[dict]:
    """Return all tracked applications (newest first), without MongoDB's _id field."""
    col = _get_collection()
    return list(col.find({}, {"_id": 0}).sort("applied_date", -1))
