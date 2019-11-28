from __future__ import print_function
import datetime, pickle, os.path, webbrowser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Navigating to next event.')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        try:
            print(start + ' | ' + event['summary'] + ' | ' + event['location'])
            webbrowser.open(
                'https://www.google.com/maps/dir/?api=1&origin=Your+Location&destination=' + event['location']
                + '&travelmode=transit')
        except KeyError:
            # Will work on setting it up so that instead of coming back with this unhelpful statement, will call on the
            # next event that has a location and navigate to there
            print('No location defined.')
            print(start + ' | ' + event['summary'])


if __name__ == '__main__':
    main()
