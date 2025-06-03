from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime


# Hardcoded users: mapping username -> dict with password, user_id, profile info
HARDCODED_USERS = {
    "johndoe": {
        "password": "password123",
        "user_id": "USER001",
        "profile": {
            "name": "John Doe",
            "email": "user@example.com",
            "contact_number": "1234567890",
        },
    },
    "alicew": {
        "password": "alicepass321",
        "user_id": "USER002",
        "profile": {
            "name": "Alice Williams",
            "email": "alice.williams@example.com",
            "contact_number": "5551234561",
        }
    },
    "bobb": {
        "password": "bobsecure!",
        "user_id": "USER003",
        "profile": {
            "name": "Bob Brown",
            "email": "bob.brown@example.com",
            "contact_number": "5552233445",
        }
    },
    "carlaj": {
        "password": "carla_j_pass",
        "user_id": "USER004",
        "profile": {
            "name": "Carla Johnson",
            "email": "carla.johnson@example.com",
            "contact_number": "5556677889",
        }
    },
    "daves": {
        "password": "davesafepassword",
        "user_id": "USER005",
        "profile": {
            "name": "Dave Smith",
            "email": "dave.smith@example.com",
            "contact_number": "5559988776",
        }
    },
    "elenaq": {
        "password": "elenaQ@pass",
        "user_id": "USER006",
        "profile": {
            "name": "Elena Quintana",
            "email": "elena.quintana@example.com",
            "contact_number": "5553344556",
        }
    },
    "frankm": {
        "password": "frankman123",
        "user_id": "USER007",
        "profile": {
            "name": "Frank Moore",
            "email": "frank.moore@example.com",
            "contact_number": "5554455667",
        }
    },
    "ginaw": {
        "password": "ginawelcome",
        "user_id": "USER008",
        "profile": {
            "name": "Gina White",
            "email": "gina.white@example.com",
            "contact_number": "5555566778",
        }
    },
    "heidic": {
        "password": "heidiComplexPwd9",
        "user_id": "USER009",
        "profile": {
            "name": "Heidi Clark",
            "email": "heidi.clark@example.com",
            "contact_number": "5556677880",
        }
    },
    "ignacioq": {
        "password": "iggyQpass2024",
        "user_id": "USER010",
        "profile": {
            "name": "Ignacio Quint",
            "email": "ignacio.quint@example.com",
            "contact_number": "5557788991",
        }
    }
}

# JWT configuration
JWT_SECRET = "CHANGE_ME_TO_SOMETHING_SECURE"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 60  # 1 minute

# PUBLIC_INTERFACE
def check_credentials_by_email(email: str, password: str):
    """
    Checks if a user exists with given email and password.
    Returns:
        (success: bool, user: dict or None)
    """
    for user in HARDCODED_USERS.values():
        if user["profile"]["email"].lower() == email.lower() and user["password"] == password:
            return True, user
    return False, None

# PUBLIC_INTERFACE
def generate_token(user_id: str):
    """
    Generates a JWT token for the given user_id with an expiry.

    Returns:
        (str) JWT token
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # PyJWT>=2 returns str by default, but older versions return bytes
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token

# PUBLIC_INTERFACE
def validate_token(token: str):
    """
    Validates a JWT token and returns the payload if valid and not expired.

    Returns:
        (dict) payload if valid, else None
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
        return None

# PUBLIC_INTERFACE
def get_user_by_id(user_id: str):
    """
    Returns user dictionary (containing username, user_id, profile, etc.) by user_id.
    Returns:
        (tuple) (username, user_dict), or (None, None) if not found
    """
    for username, data in HARDCODED_USERS.items():
        if data["user_id"] == user_id:
            return username, data
    return None, None

# PUBLIC_INTERFACE
def check_user_identity(token: str, user_id: str):
    """
    Validates token and checks if the embedded user_id matches the supplied user_id.
    Returns:
        True if token valid and user_id matches, else False.
    """
    payload = validate_token(token)
    if not payload or "user_id" not in payload:
        return False
    return payload["user_id"] == user_id

# PUBLIC_INTERFACE
def create_app():
    """Creates and configures the Flask application with required authentication endpoints."""
    app = Flask(__name__)
    # Allow CORS for all routes and origins (development mode)
    CORS(app)

    # POST /api/login endpoint
    @app.route("/api/login", methods=["POST"])
    # PUBLIC_INTERFACE
    def login():
        """
        Authenticates a user using hardcoded credentials (email + password).
        """
        data = request.get_json(silent=True)
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Missing email or password"}), 400

        email = data["email"].strip()
        password = data["password"]

        success, user = check_credentials_by_email(email, password)
        if not success:
            return jsonify({"error": "Invalid email or password"}), 401

        token = generate_token(user["user_id"])
        return jsonify({
            "token": token,
            "expires_in": JWT_EXP_DELTA_SECONDS,
            "user_id": user["user_id"]
        }), 200

    # POST /api/profile endpoint
    @app.route("/api/profile", methods=["POST"])
    # PUBLIC_INTERFACE
    def profile():
        """
        Accepts a token and user_id, validates both, and returns the user profile if valid.
        """
        data = request.get_json(silent=True)
        if not data or "token" not in data or "user_id" not in data:
            return jsonify({"error": "Missing token or user_id"}), 400

        token = data["token"]
        user_id = data["user_id"]

        # Validate token and user_id
        if not check_user_identity(token, user_id):
            return jsonify({"error": "Invalid or expired token, or user_id does not match token"}), 401

        username, user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Build flat profile dict including user_id as specified, in required field order
        from collections import OrderedDict
        profile = user["profile"]
        profile_data = OrderedDict([
            ("name", profile.get("name", "")),
            ("email", profile.get("email", "")),
            ("user_id", user["user_id"]),
            ("contact_number", profile.get("contact_number", "")),
        ])

        return jsonify(profile_data), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
