from pymongo import MongoClient
from app.core.config import MONGO_URI, DB_NAME

# Global client for internal use
client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

# Optional FastAPI dependency
def get_mongo_db():
    client = MongoClient(MONGO_URI)
    try:
        yield client[DB_NAME]
    finally:
        client.close()
