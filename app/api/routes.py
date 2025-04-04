from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.services.calendar_service import CalendarService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api")

# Models for request/response
class EventBase(BaseModel):
    summary: str
    location: Optional[str] = None
    description: Optional[str] = None
    start: Dict
    end: Dict
    attendees: Optional[List[Dict]] = None

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventResponse(EventBase):
    id: str

class CalendarResponse(BaseModel):
    id: str
    summary: str
    description: Optional[str] = None
    primary: Optional[bool] = None

# Services as dependencies
def get_auth_service():
    return AuthService()

def get_calendar_service(request: Request):
    # In a production app, you would retrieve the user's credentials from a session or database
    # For simplicity, we'll use a mock implementation
    auth_service = get_auth_service()
    
    if not hasattr(request.session, "credentials"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    credentials = auth_service.credentials_from_dict(request.session.credentials)
    return CalendarService(credentials=credentials)

# Auth routes
@router.get("/auth/login")
async def login(auth_service: AuthService = Depends(get_auth_service)):
    """Get authorization URL for Google OAuth."""
    authorization_url = auth_service.get_authorization_url()
    return {"authorization_url": authorization_url}

@router.get("/auth/callback")
async def callback(
    request: Request,
    code: str = Query(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Handle OAuth callback from Google."""
    credentials = auth_service.get_credentials_from_code(code)
    
    # In a production app, you would store these credentials securely
    # For simplicity, we'll use the session
    request.session["credentials"] = auth_service.credentials_to_dict(credentials)
    
    return RedirectResponse(url="/api/calendars")

# Calendar routes
@router.get("/calendars", response_model=List[CalendarResponse])
async def get_calendars(
    calendar_service: CalendarService = Depends(get_calendar_service)
):
    """Get all calendars for the authenticated user."""
    calendars = calendar_service.list_calendars()
    return calendars

@router.get("/calendars/{calendar_id}/events", response_model=List[EventResponse])
async def get_events(
    calendar_id: str,
    max_results: int = 10,
    calendar_service: CalendarService = Depends(get_calendar_service)
):
    """Get events from a specific calendar."""
    events = calendar_service.get_calendar_events(
        calendar_id=calendar_id,
        max_results=max_results
    )
    return events

@router.post("/calendars/{calendar_id}/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    calendar_id: str,
    event: EventCreate,
    calendar_service: CalendarService = Depends(get_calendar_service)
):
    """Create a new event in a calendar."""
    created_event = calendar_service.create_event(
        calendar_id=calendar_id,
        event_data=event.dict()
    )
    return created_event

@router.put("/calendars/{calendar_id}/events/{event_id}", response_model=EventResponse)
async def update_event(
    calendar_id: str,
    event_id: str,
    event: EventUpdate,
    calendar_service: CalendarService = Depends(get_calendar_service)
):
    """Update an existing event."""
    updated_event = calendar_service.update_event(
        calendar_id=calendar_id,
        event_id=event_id,
        event_data=event.dict()
    )
    return updated_event

@router.delete("/calendars/{calendar_id}/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    calendar_id: str,
    event_id: str,
    calendar_service: CalendarService = Depends(get_calendar_service)
):
    """Delete an event."""
    calendar_service.delete_event(
        calendar_id=calendar_id,
        event_id=event_id
    )
    return None