from typing import Dict, Optional
import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from loguru import logger

from app.config.settings import settings

class AuthService:
    """Service for Google OAuth authentication."""
    
    def __init__(self):
        """Initialize the authentication service."""
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
    
    def get_authorization_url(self) -> str:
        """Get the URL for OAuth authorization."""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=settings.GOOGLE_SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        return authorization_url
    
    def get_credentials_from_code(self, code: str) -> Credentials:
        """Exchange the authorization code for credentials."""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=settings.GOOGLE_SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        
        flow.fetch_token(code=code)
        return flow.credentials
    
    @staticmethod
    def credentials_to_dict(credentials: Credentials) -> Dict:
        """Convert credentials to a dictionary for storage."""
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
    
    @staticmethod
    def credentials_from_dict(credentials_dict: Dict) -> Credentials:
        """Create credentials from a dictionary."""
        return Credentials(
            token=credentials_dict['token'],
            refresh_token=credentials_dict['refresh_token'],
            token_uri=credentials_dict['token_uri'],
            client_id=credentials_dict['client_id'],
            client_secret=credentials_dict['client_secret'],
            scopes=credentials_dict['scopes']
        )