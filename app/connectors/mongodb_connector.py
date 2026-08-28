from app.connectors.base.connector_interface import BaseConnector
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)

class MongoDBConnector(BaseConnector):
    def connect(self):
        uri = self.config.get('uri')
        if not uri:
            # Build URI from parts
            user = self.config.get('user')
            password = self.config.get('password')
            host = self.config.get('host', 'localhost')
            port = self.config.get('port', 27017)
            uri = f"mongodb://{user}:{password}@{host}:{port}/"
            
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        return client

    def test_connection(self):
        try:
            client = self.connect()
            client.admin.command('ping')
            client.close()
            return True
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection test failed: {e}")
            return False

    def fetch_data(self, database, collection, query=None, limit=1000):
        client = self.connect()
        try:
            db = client[database]
            col = db[collection]
            results = list(col.find(query or {}).limit(limit))
            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            return results
        finally:
            client.close()

    def push_data(self, database, collection, data):
        client = self.connect()
        try:
            db = client[database]
            col = db[collection]
            if isinstance(data, list):
                result = col.insert_many(data)
                return [str(id) for id in result.inserted_ids]
            else:
                result = col.insert_one(data)
                return str(result.inserted_id)
        finally:
            client.close()
