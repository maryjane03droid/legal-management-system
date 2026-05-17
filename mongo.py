from pymongo import MongoClient, errors
from bson import ObjectId
import ssl

# --- CLOUD DATABASE CONNECTION ---
# Secure Atlas Connection String
uri = "mongodb+srv://kuthiemaryjane:m110304j@cluster0.3l9dg2e.mongodb.net/?retryWrites=true&w=majority"

try:
    # Optimized connection pooling for a responsive UI
    client = MongoClient(
        uri, 
        serverSelectionTimeoutMS=5000,
        tls=True,
        tlsAllowInvalidCertificates=True,
        maxPoolSize=20 
    )
    db = client["LegalFirmDB"]
    
    # Ping the database to confirm connection
    client.admin.command('ping')
    print("SUCCESS: LEGAL MANAGEMENT SYSTEM")
except Exception as e:
    db = None
    print(f"CRITICAL: Cloud Connection Failed. Error: {e}")

# --- HELPER: ID VALIDATOR ---
def is_valid_id(oid):
    """Prevents crashes by validating MongoDB ObjectIds before use."""
    return ObjectId.is_valid(oid)

# --- CASE MANAGEMENT ---

def add_case(name, phone, ctype, desc):
    """Inserts a new record with metadata for tracking rejections and reviews."""
    if db is None: return None
    try:
        return db.cases.insert_one({
            "name": name.strip(), 
            "phone": phone.strip(), 
            "type": ctype, 
            "desc": desc.strip(), 
            "status": "Pending",
            "rejection_count": 0,    # Tracks the 'two-strike' rule
            "reviewed_by": "None"    # Stores staff name upon approval/lock
        }).inserted_id
    except errors.PyMongoError as e:
        print(f"DB Error (add_case): {e}")
        return None

def get_cases(): 
    """Retrieves all cases. Returns an empty list if database is offline."""
    if db is None: return []
    try:
        return list(db.cases.find())
    except errors.PyMongoError:
        return []

def update_case(case_id, name, phone, ctype, desc):
    """Standard update for client details."""
    if db is None or not is_valid_id(case_id): return
    try:
        db.cases.update_one(
            {"_id": ObjectId(case_id)}, 
            {"$set": {
                "name": name.strip(), 
                "phone": phone.strip(), 
                "type": ctype, 
                "desc": desc.strip()
            }}
        )
    except errors.PyMongoError as e:
        print(f"DB Error (update_case): {e}")

def delete_case(case_id): 
    """Permanently purges a record (Only when explicitly triggered by a UI button click)."""
    if db is None or not is_valid_id(case_id): return
    try:
        db.cases.delete_one({"_id": ObjectId(case_id)})
    except errors.PyMongoError as e:
        print(f"DB Error (delete_case): {e}")

def update_status(case_id, status, reviewer):
    """Binds the case status change directly to the active staff user."""
    if db is None or not is_valid_id(case_id): return
    try:
        db.cases.update_one(
            {"_id": ObjectId(case_id)}, 
            {"$set": {"status": status, "reviewed_by": reviewer}}
        )
    except errors.PyMongoError as e:
        print(f"DB Error (update_status): {e}")

def increment_rejection(case_id, reviewer):
    """Registers a rejection stamp and increments the strike counter. Never deletes automatically."""
    if db is None or not is_valid_id(case_id): return
    try:
        db.cases.update_one(
            {"_id": ObjectId(case_id)},
            {"$inc": {"rejection_count": 1}, "$set": {"status": "Rejected", "reviewed_by": reviewer}}
        )
    except errors.PyMongoError as e:
        print(f"DB Error (increment_rejection): {e}")

# --- USER AUTHENTICATION ---

def create_user(username, password, role):
    """Creates user with case-insensitive uniqueness check."""
    if db is None: return False
    try:
        clean_name = username.strip()
        # Regex check for existing username regardless of uppercase/lowercase
        if db.users.find_one({"username": {"$regex": f"^{clean_name}$", "$options": "i"}}): 
            return False
        
        db.users.insert_one({
            "username": clean_name, 
            "password": password, 
            "role": role
        })
        return True
    except errors.PyMongoError:
        return False

def verify_user(username, password):
    """Verifies credentials with case-insensitive username matching."""
    if db is None: return None
    try:
        clean_name = username.strip()
        return db.users.find_one({
            "username": {"$regex": f"^{clean_name}$", "$options": "i"}, 
            "password": password
        })
    except errors.PyMongoError:
        return None