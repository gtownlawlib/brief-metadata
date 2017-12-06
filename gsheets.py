import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def gSheets(pdf, docket, year, name, full):
    try:
        import argparse
        flags = tools.argparser.parse_args(args=['--noauth_local_webserver'])
    except ImportError:
        flags = None

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = [YOUR_GOOGLE_API_APPLICATION_NAME]

    def get_credentials():
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.brief-metadata.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    credentials = get_credentials()
    service = discovery.build('sheets', 'v4', credentials=credentials)

    spreadsheet_id = [YOUR_GOOGLE_SHEET_ID]

    range_ = '!A2:E2'

    value_input_option = 'RAW'

    insert_data_option = 'INSERT_ROWS'

    values = [
        [
            pdf, docket, year, name, full
        ]
    ]

    body = {
        'values': values
    }

    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=body
    )
    response = request.execute()
