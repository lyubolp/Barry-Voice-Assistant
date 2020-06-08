#!/usr/bin/python3
from __future__ import print_function
import datetime
import pathlib
import pickle
import os.path
import sys

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def format_number_as_time(number):
    if number <= 9:
        return '0' + str(number)
    else:
        return str(number)


def format_number_as_month(number):
    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    return months[number]


def add_suffix_to_number(number):
    result = str(number)
    if number % 10 == 1:
        result += 'st'
    elif number % 10 == 2:
        result += 'nd'
    elif number % 10 == 3:
        result += 'rd'
    else:
        result += 'th'

    return result


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    main_directory = (str(pathlib.Path(__file__).parent.absolute()))
    pickle_path = main_directory + '/token.pickle'
    credentials_path = main_directory + '/credentials.json'
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        date_as_object = datetime.datetime.fromisoformat(start)

        result = event['summary']
        result += ' at ' + format_number_as_time(date_as_object.hour) + ':' + format_number_as_time(date_as_object.minute)
        result += ' on the ' + add_suffix_to_number(date_as_object.day) + ' of ' + format_number_as_month(date_as_object.month)
        print(result)


if __name__ == '__main__':
    main()
