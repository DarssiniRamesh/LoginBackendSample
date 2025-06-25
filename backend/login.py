import os
import datetime
import json
from flask import Flask, request, jsonify
import jwt
from flask_cors import CORS

# Configuration
JWT_SECRET = "devsecret"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 60  # 1 minute, configurable

USERS_JSON_PATH = os.path.join(os.path.dirname(__file__), "users.json")
BLACKLIST_JSON_PATH = os.path.join(os.path.dirname(__file__), "blacklist.json")

def load_users():
    """Load user data from users.json file."""
    try:
        with open(USERS_JSON_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)
        return users
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_blacklist():
    """Load blacklist data from blacklist.json file."""
    try:
        with open(BLACKLIST_JSON_PATH, "r", encoding="utf-8") as f:
            bl = json.load(f)
        return bl
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def user_is_blacklisted(user):
    """
    Check if a user is blacklisted, by user_id or by username (if present).
    'username' key is optional in user records.
    """
    blacklist = load_blacklist()
    # Accept both username and user_id as match, case-insensitive for username
    for entry in blacklist:
        if "user_id" in entry and user.get("user_id") == entry["user_id"]:
            return True
        if "username" in entry and "username" in user and user["username"].lower() == entry["username"].lower():
            return True
    return False

app = Flask(__name__)
CORS(app)

# PUBLIC_INTERFACE
def find_user_by_email_and_password(email, password):
    """
    This is a public function.
    Find a user by lowercased email and password from JSON file.
    """
    users = load_users()
    for user in users:
        if user["email"].lower() == email.lower() and user["password"] == password:
            return user
    return None

# PUBLIC_INTERFACE
def find_user_by_user_id(user_id):
    """
    This is a public function.
    Find a user by user_id from JSON file.
    """
    users = load_users()
    for user in users:
        if user["user_id"] == user_id:
            return user
    return None

@app.route("/api/login", methods=["POST"])
def api_login():
    """
    Authenticate user (email/password). Forbid login if user is blacklisted by username or user_id in blacklist.json.
    Returns JWT and expiry on success.
    """
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data["email"]
    password = data["password"]
    user = find_user_by_email_and_password(email, password)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if user_is_blacklisted(user):
        return jsonify({"error": "User is blacklisted and cannot log in"}), 403

    payload = {
        "user_id": user["user_id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return jsonify({"token": token, "expires_in": JWT_EXP_DELTA_SECONDS}), 200

@app.route("/api/profile", methods=["POST"])
def api_profile():
    """
    Given JWT token & user_id, returns the user profile if token valid and user_id matches,
    and user is not blacklisted according to blacklist.json.
    """
    data = request.get_json()
    if not data or "token" not in data or "user_id" not in data:
        return jsonify({"error": "Missing token or user_id"}), 400
    token = data["token"]
    user_id = data["user_id"]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        token_user_id = payload["user_id"]
        if token_user_id != user_id:
            raise Exception("User ID does not match token")
    except Exception:
        return jsonify({"error": "Invalid or expired token, or user_id does not match token"}), 401

    user = find_user_by_user_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user_is_blacklisted(user):
        return jsonify({"error": "User is blacklisted and cannot access profile"}), 403

    # Reply in specific field ordering: name, email, user_id, contact_number
    resp = {
        "name": user["name"],
        "email": user["email"],
        "user_id": user["user_id"],
        "contact_number": user["contact_number"]
    }
    return jsonify(resp), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
