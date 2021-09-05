from time import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import pickle

scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes = scopes)
credentials = flow.run_console()
pickle.dump(credentials, open("token.pkl", "wb")) 
#credentials = pickle.load(open("token.pkl", "rb"))

service = build("calendar", "v3", credentials=credentials)

result = service.calendarList().list().execute()

calendar_id = result['items'][0]['id']

def getEvent():
    result2 = service.events().list(calendarId=calendar_id).execute()
    print(result2['items'][-1])

getEvent()


event = {
'summary': "Sets - Session 1",
'location': "Bangalore",
'description': "Study Session",
'start': {
    'dateTime': '2021-09-06T09:00:00',
    'timeZone': 'Asia/Kolkata',
},
'end': {
    'dateTime': '2021-09-06T10:00:00',
    'timeZone': 'Asia/Kolkata',
},
'reminders': {
    'useDefault': False,
    'overrides': [
    {'method': 'email', 'minutes': 24 * 60},
    {'method': 'popup', 'minutes': 15},
    ],
},
}

result3 = service.events().insert(calendarId=calendar_id, body=event).execute()
print(result3)


