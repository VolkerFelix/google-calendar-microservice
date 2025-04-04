# Google Calendar Microservice

A Python-based microservice for interacting with the Google Calendar API.

## Features

- OAuth2 authentication with Google
- List user calendars
- Get events from specific calendars
- Create, update, and delete calendar events
- RESTful API endpoints

## Requirements

- Python 3.9+
- Google Cloud Platform account with Calendar API enabled
- OAuth2 client credentials

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/google-calendar-microservice.git
   cd google-calendar-microservice
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up Google Cloud Platform:
   - Create a new project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Google Calendar API
   - Create OAuth2 credentials (Web application)
   - Add `http://localhost:8000/api/auth/callback` as an authorized redirect URI

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your Google client ID and secret.

## Running the service

Start the service:
```bash
python -m app.main
```

The service will be available at http://localhost:8000.

## API Endpoints

### Authentication

- `GET /api/auth/login` - Get the authorization URL for Google OAuth
- `GET /api/auth/callback` - Handle the OAuth callback from Google

### Calendars

- `GET /api/calendars` - List all available calendars
- `GET /api/calendars/{calendar_id}/events` - Get events from a specific calendar
- `POST /api/calendars/{calendar_id}/events` - Create a new event
- `PUT /api/calendars/{calendar_id}/events/{event_id}` - Update an existing event
- `DELETE /api/calendars/{calendar_id}/events/{event_id}` - Delete an event

## Development

### Running tests

```bash
pytest
```

### Future improvements

- Add database integration for storing user credentials
- Implement token refresh mechanism
- Add rate limiting
- Add user management for multi-user support
- Containerize the application using Docker

## License

[MIT](LICENSE)