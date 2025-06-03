import React, { useState } from "react";
import "./App.css";

/**
 * PUBLIC_INTERFACE
 * App - Minimal UI for testing /api/login and /api/profile of Flask Login Service.
 */
function App() {
  // Form and API state
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginResult, setLoginResult] = useState(null);
  const [loginError, setLoginError] = useState("");
  const [profileResult, setProfileResult] = useState(null);
  const [profileError, setProfileError] = useState("");
  const [fetching, setFetching] = useState(false);

  // In most cases, we POST to /api/login, and then use the result to fetch profile.
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError("");
    setLoginResult(null);
    setProfileResult(null);
    setProfileError("");
    setFetching(true);

    try {
      const resp = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: loginEmail, password: loginPassword }),
      });
      const data = await resp.json();
      if (!resp.ok) {
        setLoginError(data.error || "Unknown error");
      } else {
        setLoginResult(data);
      }
    } catch (err) {
      setLoginError("Network or client error: " + err.message);
    }
    setFetching(false);
  };

  // Use fields from loginResult as input for the profile
  const handleFetchProfile = async (e) => {
    e.preventDefault();
    setProfileError("");
    setProfileResult(null);
    setFetching(true);

    try {
      const resp = await fetch("/api/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token: loginResult.token,
          user_id: loginResult.user_id,
        }),
      });
      const data = await resp.json();
      if (!resp.ok) {
        setProfileError(data.error || "Unknown error");
      } else {
        setProfileResult(data);
      }
    } catch (err) {
      setProfileError("Network or client error: " + err.message);
    }
    setFetching(false);
  };

  return (
    <div className="test-app-root">
      <h1>Flask Login Service Frontend Tester</h1>
      <section className="panel">
        <h2>1. Login</h2>
        <form onSubmit={handleLogin} autoComplete="off">
          <div className="form-row">
            <label>Email: </label>
            <input
              type="email"
              value={loginEmail}
              onChange={(e) => setLoginEmail(e.target.value)}
              required
              autoComplete="username"
            />
          </div>
          <div className="form-row">
            <label>Password: </label>
            <input
              type="password"
              value={loginPassword}
              onChange={(e) => setLoginPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>
          <button type="submit" disabled={fetching}>
            Log In
          </button>
        </form>
        {loginError && (
          <div className="error-block" data-testid="login-error">
            <b>Login Error:</b> {loginError}
          </div>
        )}
        {loginResult && (
          <div className="result-block" data-testid="login-success">
            <b>Login Success!</b>
            <pre>{JSON.stringify(loginResult, null, 2)}</pre>
          </div>
        )}
      </section>

      {/* Profile fetcher only enabled after login success */}
      {loginResult && loginResult.token && loginResult.user_id && (
        <section className="panel">
          <h2>2. Fetch Profile (with Token &amp; User ID)</h2>
          <form onSubmit={handleFetchProfile}>
            <div className="form-row">
              <label>
                Token:
                <input
                  type="text"
                  value={loginResult.token}
                  readOnly
                  className="token-output"
                />
              </label>
            </div>
            <div className="form-row">
              <label>
                User ID:
                <input
                  type="text"
                  value={loginResult.user_id}
                  readOnly
                  className="user-id-output"
                />
              </label>
            </div>
            <button type="submit" disabled={fetching}>
              Fetch Profile
            </button>
          </form>
          {profileError && (
            <div className="error-block" data-testid="profile-error">
              <b>Profile Error:</b> {profileError}
            </div>
          )}
          {profileResult && (
            <div className="result-block" data-testid="profile-success">
              <b>Profile Result:</b>
              <pre>{JSON.stringify(profileResult, null, 2)}</pre>
            </div>
          )}
        </section>
      )}

      <section className="instructions">
        <p>
          <b>Testing accounts:</b> Use emails/passwords from your backend's README
          table. (E.g., user@example.com / password123)
        </p>
        <p>
          <small>
            This UI is for functional testing only. Any field or API errors will
            appear above. Token expires in 60 seconds by default.
          </small>
        </p>
      </section>
    </div>
  );
}

export default App;
