from flask import Flask
import jwt
import datetime

# Hardcoded users: username maps to dict with password, user_id, profile info
HARDCODED_USERS = {
    "alice": {
        "password": "password123",
        "user_id": "u001",
        "profile": {
            "name": "Alice Smith",
            "role": "admin",
            "email": "alice@example.com",
        },
    },
    "bob": {
        "password": "bobpass",
        "user_id": "u002",
        "profile": {
            "name": "Bob Jones",
            "role": "user",
            "email": "bob@example.com",
        },
    },
    "carol": {
        "password": "carolpw",
        "user_id": "u003",
        "profile": {
            "name": "Carol White",
            "role": "user",
            "email": "carol@example.com",
        },
    },
}

# JWT configuration
JWT_SECRET = "CHANGE_ME_TO_SOMETHING_SECURE"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600  # 1 hour

# PUBLIC_INTERFACE
def check_credentials(username: str, password: str):
    """
    Checks if the provided username and password are correct.

    Returns:
        (bool, dict) - (success, user dictionary if authenticated, else None)
    """
    user = HARDCODED_USERS.get(username)
    if user and user["password"] == password:
        return True, user
    else:
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
        (bool) True if token is valid and user_id matches, False otherwise.
    """
    payload = validate_token(token)
    if not payload or "user_id" not in payload:
        return False
    return payload["user_id"] == user_id

# PUBLIC_INTERFACE
def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)

    # Placeholder for future config and blueprint registrations
    # Currently, no endpoints are registered

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
