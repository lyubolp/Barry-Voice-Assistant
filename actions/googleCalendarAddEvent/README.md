# Add event to Google Calendar

This is a Python3 script that creates an event in the user's
Google Calendar. In order for it to be used, the following
files must be present:
- `credentials.json` - Google Calendar API credentials
- `token.pickle` - To get this file, run the script on a
machine with a UI, in order to authenticate it for your
Google account


To run the script:

- `python3 google_calendar_add_event.py <event_name> <start_date> <end_date>`
- `python3 google_calendar_add_event.py <event_name> <event_location> <start_date> <end_date>`
- `python3 google_calendar_add_event.py <event_name> <start_date> <start_time> <end_date> <end_time>`
- `python3 google_calendar_add_event.py <event_name> <event_location> <start_date> <start_time> <end_date> <end_time>`

Where:
- `<event_name> - String`
- `<event_location> - String, can be empty`
- `<start_date> - YYY-MM-DD`
- `<start_time> - HH:MM, can be empty`
- `<end_date> - YYYY-MM-DD`
- `<end_time> - HH:MM, can be empty`
