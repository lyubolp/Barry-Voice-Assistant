#!/usr/bin/python3
from __future__ import print_function
import datetime
import pathlib
import pickle
import os.path
import sys
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


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


def load_service():
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

    return service


def main():
    service = load_service()

    event_name = ''
    event_location = ''  # Can be empty
    start_date = ''  # YYYY-MM-DD
    start_time = ''  # HH:MM, can be empty.
    end_date = ''  # YYYY-MM-DD
    end_time = ''  # HH:MM, can be empty

    event_name = sys.argv[1]

    event = {
        'summary': event_name
    }

    time_zone = 'Europe/Sofia'
    amount_of_args = len(sys.argv)

    if amount_of_args == 4 or amount_of_args == 5:
        start_date = sys.argv[amount_of_args - 2]
        end_date = sys.argv[amount_of_args - 1]

        event['start'] = {
            'date': start_date,
            'timeZone': time_zone
        }
        event['end'] = {
            'date': end_date,
            'timeZone': time_zone
        }
        if amount_of_args == 5:
            event_location = sys.argv[amount_of_args - 3]
            event['location'] = event_location
    elif amount_of_args == 6 or amount_of_args == 7:
        start_date = sys.argv[amount_of_args - 4]
        start_time = sys.argv[amount_of_args - 3]
        end_date = sys.argv[amount_of_args - 2]
        end_time = sys.argv[amount_of_args - 1]

        start = datetime.datetime.fromisoformat(start_date + 'T' + start_time+':00.000000')
        end = datetime.datetime.fromisoformat(end_date + 'T' + end_time+':00.000000')

        event['start'] = {
            'dateTime': start.isoformat(),
            'timeZone': time_zone
        }

        event['end'] = {
            'dateTime': end.isoformat(),
            'timeZone': time_zone
        }
        if amount_of_args == 7:
            event_location = sys.argv[amount_of_args - 5]
            event['location'] = event_location
    else:
        print('Invalid amount of arguments. Please visit README.md')
        return

    # event = {
    #     'summary': 'TestEvent',
    #     'location': 'TempLocation',
    #     'start': {
    #         'dateTime': datetime.datetime.now().isoformat(),
    #         'timeZone': 'Europe/Sofia',
    #     },
    #     'end': {
    #         'dateTime': '2020-06-08T14:53:40.615119',
    #         'timeZone': 'Europe/Sofia',
    #     },
    # }

    event = service.events().insert(calendarId='primary', body=event).execute()

    print('Created the event: ' + event.get('summary'))


if __name__ == '__main__':
    main()
