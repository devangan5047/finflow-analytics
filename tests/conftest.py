import pytest
from app import app as flask_app # Import your Flask app instance

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # You can add test-specific configurations here if needed
    flask_app.config['TESTING'] = True
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()