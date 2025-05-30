from flask import Flask

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
