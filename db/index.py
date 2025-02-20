from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ConnectionFailure

class MongoDBHandler:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """Establish a connection to the MongoDB server."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            # Test the connection
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully.")
        except ConnectionFailure as e:
            print(f"Connection failed: {e}")
    
    def save_emission(self, americanEnergyUsage, diselGallonsConsumed, phonesCharged, day, month, year):
        emission = dict({'americanEnergyUsage=': americanEnergyUsage, 'diselGallonsConsumed': diselGallonsConsumed,
        'phonesCharged': phonesCharged, 'day': day,'month': month,'year': year})

        self.upsert_document({"name": "latest"}, emission)

    def upsert_document(self, filter_query: dict, update_data: dict):
        """
        Perform an upsert operation. Update the document if it exists;
        otherwise, insert a new document.

        :param filter_query: Dictionary to filter the document to update.
        :param update_data: Dictionary containing the fields to update or insert.
        :return: The updated or inserted document.
        """

        updated_document = self.collection.find_one_and_update(
            filter_query,
            {'$set': update_data},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return updated_document