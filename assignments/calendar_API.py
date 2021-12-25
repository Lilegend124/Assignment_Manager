from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
import datetime
from allauth.socialaccount.models import SocialApp, SocialAccount
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './google-credentials.json'

def get_credentials(request):
    app = SocialApp.objects.get(provider='google')
    account = SocialAccount.objects.get(user=request.user)

    user_tokens = account.socialtoken_set.first()

    creds = Credentials(
        token=user_tokens.token,
        # refresh_token=user_tokens.refresh_token,
        client_id=app.client_id,
        client_secret='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'
    )

    return creds

def add_event_to_calendar(summary, startDateTime, endDateTime, request):
    creds = get_credentials(request)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

    # CREATE A NEW EVENT
    new_event = {
    'summary': summary,
    'start': {
        'dateTime': startDateTime,
        'timeZone': 'US/Eastern',
    },
    'end': {
        'dateTime': endDateTime,
        'timeZone': 'US/Eastern',
    },
    }
    new_event = service.events().insert(calendarId="primary", body=new_event).execute()
    event = new_event.get('htmlLink')
    # GET ALL EXISTING EVENTS
    # events_result = service.events().list(calendarId="primary", maxResults=2500).execute()
    # events = events_result.get('items', [])


    #uncomment the following lines to delete each existing item in the calendar
    #event_id = e['id']
    # service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()

    return event
