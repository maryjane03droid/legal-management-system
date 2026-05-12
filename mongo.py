import certifi
from pymongo import MongoClient
from bson import ObjectId

# CONNECTION: Using certifi to bypass SSL errors
connection_string = "mongodb+srv://albejquarshie_db_user:bimVT2PLuZGLOtS8@vroomify.fzlbwnh.mongodb.net/?appName=vroomify"
client = MongoClient(connection_string, tlsCAFile=certifi.where())

# DATABASE: Clean Legal Management naming
db = client["legal_management"]
staff_users = db["staff_credentials"] # Collection for Login/Signup
client_cases = db["legal_cases"]       # Collection for Case Data

# --- AUTHENTICATION LOGIC ---

def signup_staff(username, password):
    """Saves a new staff member to MongoDB."""
    if staff_users.find_one({"username": username}):
        return False  # User already exists
    staff_users.insert_one({"username": username, "password": password})
    return True

def check_login(username, password):
    """Checks credentials for the pop-up authentication."""
    user = staff_users.find_one({"username": username, "password": password})
    return True if user else False

# --- CASE SAVING LOGIC ---

def add_new_case(client_name, phone, case_type):
    """Saves a legal case record directly to MongoDB."""
    case_entry = {
        "client_name": client_name,
        "phone": phone,
        "case_type": case_type,
        "status": "Pending Review"
    }
    return client_cases.insert_one(case_entry)

def get_all_cases():
    """Fetches all cases to show in the UI table."""
    return list(client_cases.find())

def remove_case(case_id):
    """Deletes a record from MongoDB."""
    return client_cases.delete_one({"_id": ObjectId(case_id)})

try:
    client.admin.command("ping")
    print("--- DATABASE CONNECTED ---")
except Exception as e:
    print("--- CONNECTION ERROR ---:", e)