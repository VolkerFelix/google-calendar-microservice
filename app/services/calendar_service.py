import json
from typing import Dict, List, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger

from app.config.settings import settings

class CalendarService:
    """Service for interacting with Google Calendar API."""
    
    def __init__(self, credentials: Optional[Credentials] = None):
        """Initialize the calendar service with optional credentials."""
        self.credentials = credentials
        self.service = None
        if credentials:
            self._build_service()
    
    def _build_service(self) -> None:
        """Build the Google Calendar service."""
        if not self.credentials:
            raise ValueError("Credentials are required to build the service")
        
        self.service = build("calendar", "v3", credentials=self.credentials)
    
    def set_credentials(self, credentials: Credentials) -> None:
        """Set the credentials and rebuild the service."""
        self.credentials = credentials
        self._build_service()
    
    def list_calendars(self) -> List[Dict]:
        """List all available calendars for the authenticated user."""
        if not self.service:
            raise ValueError("Service is not initialized. Set credentials first.")
        
        try:
            calendars_result = self.service.calendarList().list().execute()
            return calendars_result.get("items", [])
        except HttpError as error:
            logger.error(f"Error listing calendars: {error}")
            raise
    
    def get_calendar_events(self, calendar_id: str = "primary", max_results: int = 10, 
                          time_min: Optional[str] = None) -> List[Dict]:
        """Get events from a specified calendar."""
        if not self.service:
            raise ValueError("Service is not initialized. Set credentials first.")
        
        try:
            events_result = self.service.events().list(
                calendarId=calendar_id,
                maxResults=max_results,
                timeMin=time_min,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            
            return events_result.get("items", [])
        except HttpError as error:
            logger.error(f"Error getting calendar events: {error}")
            raise
    
    def create_event(self, calendar_id: str = "primary", event_data: Dict = None) -> Dict:
        """Create a new event in the specified calendar."""
        if not self.service:
            raise ValueError("Service is not initialized. Set credentials first.")
        
        if not event_data:
            raise ValueError("Event data is required to create an event")
        
        try:
            event = self.service.events().insert(
                calendarId=calendar_id,
                body=event_data
            ).execute()
            
            return event
        except HttpError as error:
            logger.error(f"Error creating event: {error}")
            raise
    
    def update_event(self, calendar_id: str = "primary", event_id: str = None, 
                   event_data: Dict = None) -> Dict:
        """Update an existing event in the specified calendar."""
        if not self.service or not event_id or not event_data:
            raise ValueError("Service, event_id, and event_data are required")
        
        try:
            event = self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event_data
            ).execute()
            
            return event
        except HttpError as error:
            logger.error(f"Error updating event: {error}")
            raise
    
    def delete_event(self, calendar_id: str = "primary", event_id: str = None) -> bool:
        """Delete an event from the specified calendar."""
        if not self.service or not event_id:
            raise ValueError("Service and event_id are required")
        
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            return True
        except HttpError as error:
            logger.error(f"Error deleting event: {error}")
            raise