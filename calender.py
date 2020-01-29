"""
This python script is responsible for loading items from the database into Google Calendar
and then keeping entries up-to-date when the script is executed.

(c) Vincent Lee
"""

import config
from tinydb import TinyDB, Query
import time
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

database = TinyDB(config.database)
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    # From Google API Example
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('config/token.pickle'):
        with open('config/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.googleAPIKeyFile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('config/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def AddEvents(service):
    for event in database:
        startDate = event['Date']+'/'+event['start']
        startDate = datetime.datetime.strptime(startDate, '%d/%m/%Y/%H:%M')
        endDate = event['Date']+'/'+event['end']
        endDate = datetime.datetime.strptime(endDate, '%d/%m/%Y/%H:%M')
        response = {
            'summary': event['Module'] + ' ' + event['ClassType'],
            'location': event['Location'],
            'start': {
                'dateTime': startDate.isoformat(),
                'timeZone': 'Europe/London',
            },
            'end': {
                'dateTime': endDate.isoformat(),
                'timeZone': 'Europe/London',
            },
            'id': event['UUID'],
            'colorId': event['colourID']
        }
        try:
            event = service.events().insert(calendarId=config.CalendarID, body=response).execute()
            print('Event created: %s' % (event.get('htmlLink')))
            print(event)
        except:
            print('Error uploading')
            print(event)
        time.sleep(0.1)
    database.update({"updated": False, "Checked": False, 'added': True})


def updateAndDeleteEvents(service):
    find = Query()
    newEvents = database.search(find.added == False)
    for event in newEvents:
        startDate = event['Date'] + '/' + event['start']
        startDate = datetime.datetime.strptime(startDate, '%d/%m/%Y/%H:%M')
        endDate = event['Date'] + '/' + event['end']
        endDate = datetime.datetime.strptime(endDate, '%d/%m/%Y/%H:%M')
        response = {
            'summary': event['Module'] + ' ' + event['ClassType'],
            'location': event['Location'],
            'start': {
                'dateTime': startDate.isoformat(),
                'timeZone': 'Europe/London',
            },
            'end': {
                'dateTime': endDate.isoformat(),
                'timeZone': 'Europe/London',
            },
            'id': event['UUID'],
            'colorId': event['colourID']
        }
        try:
            event = service.events().insert(calendarId=config.CalendarID, body=response).execute()
            print('Event created: %s' % (event.get('htmlLink')))
            print('Added event: ' + event['UUID'])
        except:
            print('Error uploading')
            print(event)
        database.update({'updated': False, 'added': True}, find.UUID == event['UUID'])


    updatedEvents = database.search(find.updated == True)
    for event in updatedEvents:
        # https://developers.google.com/calendar/v3/reference/events/update
        startDate = event['Date'] + '/' + event['start']
        startDate = datetime.datetime.strptime(startDate, '%d/%m/%Y/%H:%M')
        endDate = event['Date'] + '/' + event['end']
        endDate = datetime.datetime.strptime(endDate, '%d/%m/%Y/%H:%M')
        response = {
            'summary': event['Module'] + ' ' + event['ClassType'],
            'location': event['Location'],
            'start': {
                'dateTime': startDate.isoformat(),
                'timeZone': 'Europe/London',
            },
            'end': {
                'dateTime': endDate.isoformat(),
                'timeZone': 'Europe/London',
            },
            'colorId': event['colourID']
        }
        try:
            eventToUpdate = service.events().get(calendarId=config.CalendarID, eventId=event['UUID']).execute()
            update = service.events().update(calendarId=config.CalendarID, eventId=eventToUpdate['id'], body=response).execute()
            print('Event Updated: %s' % (update.get('htmlLink')))
        except:
            print('Error updating')

    deletedEvents = database.search(find.Checked == False)
    for event in deletedEvents:
        try:
            update = service.events().delete(calendarId=config.CalendarID, eventId=event['UUID']).execute()
            print('Event Updated: %s' % (update.get('htmlLink')))
            database.remove(find.UUID == event['UUID'])
        except:
            print('Error updating')

    database.update({"updated": False, "Checked": False})


def deleteEvents(service):
    find = Query()
    for event in database:
        update = service.events().delete(calendarId=config.CalendarID, eventId=event['UUID']).execute()
        print('Event Deleted: ' + event["UUID"])
        database.remove(find.UUID == event['UUID'])


def getCalID(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry["accessRole"] == "owner":
                print(calendar_list_entry['summary'] + ' : ' + calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


if __name__ == '__main__':
    print("I'm going to delete all entries made to Google Calendar by this program in 5 seconds")
    print('Ctrl/CMD + C to cancel')
    time.sleep(5)
    service = main()
    deleteEvents(service)
