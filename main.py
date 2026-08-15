import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient, errors
from bson import ObjectId

# 1. Initialize the Flask Web App (This is what Gunicorn is looking for!)
app = Flask(__name__)
load_dotenv()

# 2. Connect to your MongoDB Database
uri = os.getenv("MONGO_URI")
try:
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
    db = client["LegalFirmDB"]
    client.admin.command('ping')
    print("SUCCESS: DATABASE CONNECTED")
except Exception as e:
    db = None
    print(f"CRITICAL: Connection Failed. Error: {e}")

# 3. Create your Web Routes (The pages people will see)
@app.route('/')
def home():
    if db is None:
        return "<h1>Database Error</h1><p>Check your MONGO_URI in Render.</p>"
    return "<h1>Welcome to the Legal Management System</h1><p>The web server is running!</p>"

@app.route('/api/cases')
def api_cases():
    if db is None: return jsonify({"error": "No database connection"})
    cases = list(db.cases.find())
    for case in cases:
        case['_id'] = str(case['_id']) # Convert IDs to text
    return jsonify(cases)

# 4. Run the app locally
if __name__ == '__main__':
    app.run(debug=True, port=5000)