from crewai.tools import tool
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

@tool("google_calendar_tool")
def google_calendar_tool(event_title: str, date: str, start_hour: int, duration: int) -> str:
    """
    Creates an event in Google Calendar.

    Args:
        event_title (str): The title or summary of the calendar event.
        date (str): The date of the event in YYYY-MM-DD format.
        start_hour (int): The starting hour of the event (0-23) in 24-hour format.
        duration (int): The duration of the event in hours.

    Returns:
        str: A confirmation message with the link to the created Google Calendar event.
    """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    start_time = datetime.strptime(date, "%Y-%m-%d") + timedelta(hours=start_hour)
    end_time = start_time + timedelta(hours=duration)

    event = {
        'summary': event_title,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created successfully: {event.get('htmlLink')}"
    except Exception as e:
        return f"An error occurred while creating the event: {str(e)}"