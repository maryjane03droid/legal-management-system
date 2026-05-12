from pymongo import MongoClient
from bson.objectid import ObjectId

class DatabaseManager:
    def __init__(self):
        # 1. Connect to the local MongoDB server
        # Standard connection string for a local setup
        self.client = MongoClient("mongodb+srv://kuthiemaryjane:m110304j@cluster0.3l9dg2e.mongodb.net/")
        
        # 2. Access the database [cite: 5]
        self.db = self.client['legal_management_system']
        
        # 3. Define our main collections [cite: 4, 7]
        self.clients = self.db['clients']
        self.appointments = self.db['appointments']
        self.cases = self.db['cases']
        self.users = self.db['users']
        
        print("Successfully connected to MongoDB")

    # --- CLIENT OPERATIONS (CRUD) [cite: 6] ---

    def authenticate_or_signup(self, username, password, role="staff"):
        """Finds a user or creates one if they don't exist."""
        user = self.db.users.find_one({"username": username})
        
        if user:
            # User exists, check password
            if user['password'] == password:
                return user
            else:
                return None # Wrong password
        else:
            # First timer! Create the account
            new_user = {
                "username": username,
                "password": password,
                "role": role
            }
            self.db.users.insert_one(new_user)
            return new_user
        
    def check_login(self, username, password):
        """Checks if the user exists and the password matches"""
        # In a real app, we would use 'bcrypt' to hash these passwords!
        user = self.db.users.find_one({"username": username, "password": password})
        return user is not None
    
    def add_client(self, name, phone, email="no email provided", case_type="General"):
        """Adds a new client document to the collection """
        client_data = {
            "name": name,
            "phone": phone,
            "email": email,
            "case_type": case_type,
            "status": "Active"
        }
        return self.clients.insert_one(client_data)

    def get_all_clients(self):
        """Retrieves every client in the database [cite: 6]"""
        return list(self.clients.find())

    def delete_client(self, client_id):
        
        try:
            # We must convert the string ID from the UI back into a MongoDB ObjectId
            self.clients.delete_one({"_id": ObjectId(client_id)})
            return True
        except Exception as e:
            print(f"Delete Error: {e}")
            return False
# To test if it works:
if __name__ == "__main__":
    db = DatabaseManager()