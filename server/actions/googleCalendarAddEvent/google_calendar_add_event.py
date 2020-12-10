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


def is_time_format_valid(time_string) -> bool:
    if len(time_string) != 5:
        return False

    if time_string[2] != ':':
        return False

    if not('0' <= time_string[0] <= '2'):
        return False

    if not('0' <= time_string[1] <= '9') or not('0' <= time_string[4] <= '9'):
        return False
    else:
        if time_string[0] == '2' and time_string[1] >= '5':
            return False

    if not('0' <= time_string[3] <= '5'):
        return False

    return True

def is_date_format_valid(date_string) -> bool:
    # YYYY-MM-DD
    if len(date_string) != 10:
        return False

    if date_string[4] != '-' or date_string[7] != '-':
        return False

    if not(1 <= date_string[0] <= 2):
        return False

    if date_string[1] != 9 and date_string[1] != 0:
        return False

    if not('0' <= date_string[2] <= '9') or not('0' <= date_string[3] <= '9'):
        return False

    if date_string[5] != '0' and date_string[5] != '1':
        return False
    elif date_string[5] == 1:
        if date_string[6] >= '3':
            return False

    if not('0' <= date_string[6] <= '9'):
        return False

    if not('0' <= date_string[8] <= '3'):
        return False

    if not('0' <= date_string[9] <= '9'):
        return False


def are_arguments_valid(args) -> bool:
    if len(args) == 4:
        if not is_date_format_valid(args[2]) or not is_date_format_valid(args[3]):
            return False
    elif len(args) == 5:
        if not is_date_format_valid(args[3]) or not is_date_format_valid(args[4]):
            return False
    elif len(args) == 6:
        if not is_date_format_valid(args[2]) or not is_date_format_valid(args[4]):
            return False
        if not is_time_format_valid(args[3]) or not is_time_format_valid(args[5]):
            return False
    elif len(args) == 7:
        if not is_date_format_valid(args[3]) or not is_date_format_valid(args[5]):
            return False
        if not is_time_format_valid(args[4]) or not is_time_format_valid(args[6]):
            return False
    else:
        return False

    return True


def main():
    service = load_service()

    # event_location = ''  # Can be empty
    # start_date = ''  # YYYY-MM-DD
    # start_time = ''  # HH:MM, can be empty.
    # end_date = ''  # YYYY-MM-DD
    # end_time = ''  # HH:MM, can be empty

    if not are_arguments_valid(sys.argv):
        print('Invalid arguments, please refer to the README for valid format')
        return

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

    event = service.events().insert(calendarId='primary', body=event).execute()

    print('Created the event: ' + event.get('summary'))


if __name__ == '__main__':
    main()
