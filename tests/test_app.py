from starlette.testclient import TestClient
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

from app.main import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize the test client
client = TestClient(app, base_url="http://test")

def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Google Calendar Microservice is running"}

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.parametrize(
    "endpoint,expected_status",
    [
        ("/api/calendars", 401),
        ("/api/calendars/primary/events", 401),
    ],
)
def test_protected_endpoints_without_auth(endpoint, expected_status):
    """Test that protected endpoints return 401 without authentication."""
    response = client.get(endpoint)
    assert response.status_code == expected_status

@patch("app.api.routes.get_auth_service")
def test_login_endpoint(mock_get_auth_service):
    """Test the login endpoint."""
    # Mock the auth service
    mock_auth_service = MagicMock()
    mock_auth_service.get_authorization_url.return_value = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=..."
    mock_get_auth_service.return_value = mock_auth_service
    
    response = client.get("/api/auth/login")
    assert response.status_code == 200
    assert "authorization_url" in response.json()
    mock_auth_service.get_authorization_url.assert_called_once()