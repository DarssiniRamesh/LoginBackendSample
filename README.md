- [Installation & Setup](#installation--setup)
- [Running the Backend](#running-the-backend)
- [API Reference](#api-reference)
  - [/api/login (POST)](#apilogin-post)
  - [/api/profile (POST)](#apiprofile-post)
- [Hardcoded User Accounts](#hardcoded-user-accounts)
- [Token Expiry & Configuration](#token-expiry--configuration)
- [Testing with curl](#testing-with-curl)
- [Notes for Developers](#notes-for-developers)

---

## Overview

**Flask Login Service** implements an isolated authentication system providing two main API endpoints:

- `POST /api/login` — Authenticate a user by email & password, get a JWT token.
- `POST /api/profile` — Given a JWT and a user_id, return the authenticated user profile.

All data is hardcoded and no external database or persistent storage is involved; all responses are standard JSON.

---

## Architecture & Features

- **Framework:** Python 3.x, Flask, Flask-CORS, PyJWT
- **Design:** Stateless REST API, CORS enabled (development)
- **Endpoints:** `/api/login` and `/api/profile` (both POST)
- **Authentication:** Hardcoded user credentials, JWT-based sessions with expiry
- **No Persistence:** No external databases or services; ready for frontend prototyping & extension
- **Response Structure:** Deterministic, with clear error codes and field ordering

---

## Prerequisites

- **Python:** Version 3.8 or higher recommended
- **pip:** Standard Python package manager

### Python Dependencies

All required Python packages are listed in [`backend/requirements.txt`](backend/requirements.txt):

- Flask >=2.3, <3.0
- Flask-CORS >=3.0.10, <4.0
- PyJWT >=2.8, <3.0

---

## Installation & Setup

1. **Clone/Download the Project**

   ```sh
   git clone <your-repo-url>
   cd LoginBackendSample
   ```

2. **Set up a Python Virtual Environment** (recommended):

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python Dependencies:**
   ```sh
   pip install -r backend/requirements.txt
   ```

---

## Running the Backend

From the project root directory, run:

```sh
python backend/login.py
```

- The server will start on http://0.0.0.0:5000/
- No custom configuration is needed for defaults.

---

## API Reference

### /api/login (POST)

**Authenticate a user and receive a short-lived JWT token.**

- **URL:** `/api/login`
- **Method:** POST
- **Content-Type:** `application/json`

#### Request Body

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

- Both fields are required. Email is **case-insensitive**.

#### Success Response

- **Status:** 200 OK
- **Body:**

```json
{
  "token": "<JWT_TOKEN>",
  "expires_in": 60
}
```

- `token`: A JWT string to be used for profile requests (valid for 60 seconds, by default).
- `expires_in`: Lifetime of the token in seconds.

#### Failure Responses

- **Missing fields:** `400 Bad Request`
  ```json
  { "error": "Missing email or password" }
  ```
- **Invalid credentials:** `401 Unauthorized`
  ```json
  { "error": "Invalid email or password" }
  ```

---

### /api/profile (POST)

**Fetch the user profile for a validated user.**

- **URL:** `/api/profile`
- **Method:** POST
- **Content-Type:** `application/json`

#### Request Body

```json
{
  "token": "<JWT_TOKEN>",
  "user_id": "USER001"
}
```
- Both fields are required.

#### Success Response

- **Status:** 200 OK
- **Body:** (example for user johndoe, output ordering is always: name, email, user_id, contact_number)

```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "user_id": "USER001",
  "contact_number": "1234567890"
}
```

#### Error Responses

- **Missing fields:** `400 Bad Request`
  ```json
  { "error": "Missing token or user_id" }
  ```
- **Invalid/expired token or user_id mismatch:** `401 Unauthorized`
  ```json
  { "error": "Invalid or expired token, or user_id does not match token" }
  ```
- **User not found:** `404 Not Found`
  ```json
  { "error": "User not found" }
  ```

---

## Hardcoded User Accounts

The following users are available for testing. Use these credentials for `/api/login`:

| Username   | Email                       | Password            | user_id  | Name              | Contact Number |
|------------|----------------------------|---------------------|----------|-------------------|----------------|
| johndoe    | user@example.com           | password123         | USER001  | John Doe          | 1234567890     |
| alicew     | alice.williams@example.com | alicepass321        | USER002  | Alice Williams    | 5551234561     |
| bobb       | bob.brown@example.com      | bobsecure!          | USER003  | Bob Brown         | 5552233445     |
| carlaj     | carla.johnson@example.com  | carla_j_pass        | USER004  | Carla Johnson     | 5556677889     |
| daves      | dave.smith@example.com     | davesafepassword    | USER005  | Dave Smith        | 5559988776     |
| elenaq     | elena.quintana@example.com | elenaQ@pass         | USER006  | Elena Quintana    | 5553344556     |
| frankm     | frank.moore@example.com    | frankman123         | USER007  | Frank Moore       | 5554455667     |
| ginaw      | gina.white@example.com     | ginawelcome         | USER008  | Gina White        | 5555566778     |
| heidic     | heidi.clark@example.com    | heidiComplexPwd9    | USER009  | Heidi Clark       | 5556677880     |
| ignacioq   | ignacio.quint@example.com  | iggyQpass2024       | USER010  | Ignacio Quint     | 5557788991     |

---

## Token Expiry & Configuration

- **JWT Expiry:** Tokens are **valid for 60 seconds** (1 minute) by default.
- **Location to change expiry:**
  - See `JWT_EXP_DELTA_SECONDS` near the top of [`backend/login.py`](backend/login.py).
  - To change lifetime, edit:

    ```python
    JWT_EXP_DELTA_SECONDS = <desired_seconds>
    ```

    Example: for 10 minutes, set `JWT_EXP_DELTA_SECONDS = 600`

- **Secret:** The JWT secret key (`JWT_SECRET`) should be changed for real deployments.

---

## Testing with curl

### 1. Login and get a token:

```sh
curl -X POST http://localhost:5000/api/login \
  -H 'Content-Type: application/json' \
  -d '{"email": "user@example.com", "password": "password123"}'
```

**Expected output:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJh...",
  "expires_in": 60
}
```

### 2. Fetch user profile (replace TOKEN and USER_ID):

```sh
curl -X POST http://localhost:5000/api/profile \
  -H 'Content-Type: application/json' \
  -d '{"token": "<TOKEN_FROM_LOGIN>", "user_id": "USER001"}'
```

**Expected output:**
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "user_id": "USER001",
  "contact_number": "1234567890"
}
```

### 3. Error Case Example: Expired/Invalid Token

If you wait longer than `expires_in` seconds, the token becomes invalid:

```json
{ "error": "Invalid or expired token, or user_id does not match token" }
```

---

## Notes for Developers

- All credentials and user details are **hardcoded** for demo and prototyping.
- JWTs are signed and verified but transport security (HTTPS) and robust token management are **not included**—add for production.
- Modify/add users in `HARDCODED_USERS` in [`backend/login.py`](backend/login.py) for more test cases.
- This project is ideal for frontend login/profile UI development or for automated API test harnesses.
- The code is easily extensible for integration with persistent databases, additional authentication policies, or more endpoints.
- CORS is enabled for all origins for local development.
- Contributions, feedback, and new feature proposals are welcome!

---

## Contact & License

This service was generated as a demo/sample. Feel free to extend or adapt.
