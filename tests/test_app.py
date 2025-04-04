import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch

from app.main import app

# Create a test client
client = TestClient(app)

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
def test_protected_endpoints_without_auth(endpoint, expected_status, monkeypatch):
    """Test that protected endpoints return 401 without authentication."""
    # Mock the get_calendar_service function to simulate authentication failure
    with patch("app.api.routes.get_calendar_service") as mock_get_service:
        mock_get_service.side_effect = Exception("Not authenticated")
        response = client.get(endpoint)
        assert response.status_code == expected_status

@patch("app.services.auth_service.AuthService.get_authorization_url")
def test_login_endpoint(mock_get_authorization_url):
    """Test the login endpoint."""
    # Set up the mock to return a URL
    mock_get_authorization_url.return_value = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=..."
    
    # Call the endpoint
    response = client.get("/api/auth/login")
    
    # Check the response
    assert response.status_code == 200
    assert "authorization_url" in response.json()
    
    # Verify the mock was called
    mock_get_authorization_url.assert_called_once()