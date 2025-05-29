from flask import Blueprint, request, jsonify

# Create a Flask blueprint for login-related routes
login_bp = Blueprint('login', __name__, url_prefix='/api')

# Hardcoded list of users. Each user is a dictionary with the required fields.
USERS = [
    {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "employee_id": "EMP001",
        "contact_number": "1234567890",
        "password": "alicepw"
    },
    {
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "employee_id": "EMP002",
        "contact_number": "2345678901",
        "password": "bobpw"
    },
    {
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "employee_id": "EMP003",
        "contact_number": "3456789012",
        "password": "charliepw"
    },
    {
        "name": "David Lee",
        "email": "david@example.com",
        "employee_id": "EMP004",
        "contact_number": "4567890123",
        "password": "davidpw"
    },
    {
        "name": "Emily Clark",
        "email": "emily@example.com",
        "employee_id": "EMP005",
        "contact_number": "5678901234",
        "password": "emilypw"
    },
    {
        "name": "Frank Miller",
        "email": "frank@example.com",
        "employee_id": "EMP006",
        "contact_number": "6789012345",
        "password": "frankpw"
    },
    {
        "name": "Grace Wilson",
        "email": "grace@example.com",
        "employee_id": "EMP007",
        "contact_number": "7890123456",
        "password": "gracepw"
    },
    {
        "name": "Hannah Adams",
        "email": "hannah@example.com",
        "employee_id": "EMP008",
        "contact_number": "8901234567",
        "password": "hannahpw"
    },
    {
        "name": "Isaac Turner",
        "email": "isaac@example.com",
        "employee_id": "EMP009",
        "contact_number": "9012345678",
        "password": "isaacpw"
    },
    {
        "name": "Julia Evans",
        "email": "julia@example.com",
        "employee_id": "EMP010",
        "contact_number": "0123456789",
        "password": "juliapw"
    }
]

# PUBLIC_INTERFACE
@login_bp.route('/login', methods=['POST'])
def login():
    """
    Handle user login. Checks submitted email and password against hardcoded users.
    ---
    Request: JSON {"email": "...", "password": "..."}
    Success: 200, JSON with user fields (excluding password)
    Error: 401, JSON {"error": "Invalid email or password"}
    """
    # Get JSON data from the request (expects email and password)
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required."}), 400

    email = data['email']
    password = data['password']

    # Find user with matching email and password
    user = next(
        (u for u in USERS if u['email'] == email and u['password'] == password),
        None
    )

    if user:
        # Prepare result without password
        user_result = {k: v for k, v in user.items() if k != 'password'}
        return jsonify(user_result), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401
