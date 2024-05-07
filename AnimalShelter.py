from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    # CRUD operations for Animal collection in MongoDB

    def __init__(self, username, password):
        "Initialize the MongoClient. This helps to access the MongoDB databses and collections"      
        self.client = MongoClient('mongodb://%s:%s@localhost:27017' % (username, password))
        self.database = self.client['AAC']

    # Method to check the connection
    def check_connection(self):
        try:
            # Try to execute a simple query to verify the connection
            result = self.database.command("ping")
            print("Connected to MongoDB successfully.")
        except Exception as e:
            print("Connection to MongoDB failed:", e)
        
        
    # CREATE Method
    def create(self, data):
        if isinstance(data, dict) and data:
            try:
                self.database.animals.insert_one(data)
                print("Document inserted successfully.")
                return True
            except Exception as e:
                print(f"Error inserting document: {e}")
                return False
        else:
            print("Error: Data parameter must be a non-empty dictionary.")
            return False

    # READ Method
    def read(self, criteria=None, exclude_id=None):
        try:
            # Check if the _id field should be excluded
            projection = {"_id": False} if exclude_id else {}
            # Check if criteria is provided
            if criteria is None:
                criteria = {}
            # Perform Query
            cursor = self.database.animals.find(criteria, projection)
            # Optionally print the documents (can be removed if not needed)
            for document in cursor:
                print(document)
            return cursor
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    # Update Method
    def update(self, searchData, updateData):
        try:
            result = self.database.animals.update_many(searchData, {'$set' : updateData})
            # Check if the update was successfull
            if result.modified_count > 0 :
                return {'status' : 'success', ' matched_count': result.matched_count, 'modified_count' : result.modified_count}
            else:
                return {'status' : 'no changes', ' matched_count': result.matched_count, 'modified_count' : result.modified_count}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    #Delete Method  
    def delete(self, deleteData):
        try:
            result = self.database.animals.delete_many(deleteData)
            if result.deleted_count > 0 :
                return {'status': 'success', 'deleted_count': result.deleted_count}
            else:
                return {'status': 'no changes', 'deleted_count': result.deleted_count}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}