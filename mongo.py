import certifi
from pymongo import MongoClient
from bson import ObjectId

# Your Secure Connection String
uri = "mongodb+srv://kuthiemaryjane:m110304j@cluster0.3l9dg2e.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["legal_management_firm"]
cases_col = db["cases"]
users_col = db["users"]

def smart_auth(u, p, r="Client"):
    """Handles auto-signup and password verification."""
    user = users_col.find_one({"username": u})
    if user:
        if user['password'] == p: return user, "SUCCESS"
        return None, "WRONG_PASS"
    else:
        new_user = {"username": u, "password": p, "role": r}
        users_col.insert_one(new_user)
        return new_user, "CREATED"

def add_case(name, phone, c_type, desc):
    return cases_col.insert_one({
        "name": name, "phone": phone, "type": c_type, 
        "desc": desc, "status": "Pending", "reviewed_by": "None"
    })

def edit_case(case_id, name, phone, c_type, desc):
    return cases_col.update_one(
        {"_id": ObjectId(case_id)},
        {"$set": {"name": name, "phone": phone, "type": c_type, "desc": desc}}
    )

def delete_case(case_id):
    return cases_col.delete_one({"_id": ObjectId(case_id)})

def update_status(case_id, status, staff_identity):
    """Saves the status and the name/title of the legal person."""
    return cases_col.update_one(
        {"_id": ObjectId(case_id)}, 
        {"$set": {"status": status, "reviewed_by": staff_identity}}
    )

def get_cases():
    return list(cases_col.find())