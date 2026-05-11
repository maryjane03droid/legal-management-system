from pymongo import MongoClient
from bson.objectid import ObjectId

class DatabaseManager:
    def __init__(self):
        # 1. Connect to the local MongoDB server
        # Standard connection string for a local setup
        self.client = MongoClient("mongodb://localhost:27017/")
        
        # 2. Access the database [cite: 5]
        self.db = self.client['legal_management_system']
        
        # 3. Define our main collections [cite: 4, 7]
        self.clients = self.db['clients']
        self.appointments = self.db['appointments']
        self.cases = self.db['cases']
        
        print("Successfully connected to MongoDB")

    # --- CLIENT OPERATIONS (CRUD) [cite: 6] ---

    def add_client(self, name, phone, email):
        """Adds a new client document to the collection """
        client_data = {
            "name": name,
            "phone": phone,
            "email": email
        }
        return self.clients.insert_one(client_data)

    def get_all_clients(self):
        """Retrieves every client in the database [cite: 6]"""
        return list(self.clients.find())

    def delete_client(self, client_id):
        """Removes a client using their unique ID [cite: 6]"""
        self.clients.delete_one({"_id": ObjectId(client_id)})

# To test if it works:
if __name__ == "__main__":
    db = DatabaseManager()