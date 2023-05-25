from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sqlite3
from dotenv import load_dotenv
from mail import send_email

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = os.getenv('SHEET_ID')
RANGE_NAME = 'Sheet1!B:C'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        
        counter = 0
        for v in values:
            if v:
                counter += 1

        conn = sqlite3.connect('AA_db.sqlite')
        cur = conn.cursor()

        cur.execute('SELECT * FROM applications')
        data = cur.fetchall()
        print(data)
        
        current_total = data[-1][2]

        cur.execute(f'INSERT INTO applications (number) values ({counter})')
        conn.commit()

        cur.execute('SELECT * FROM applications WHERE ID = (SELECT MAX(ID) FROM applications)')
        data = cur.fetchall()

        new_total = data[0][2]
        
        net_gain = new_total - current_total

        if net_gain < 3:
            send_email(f"""Past Total = {current_total}\nToday's Total = {new_total}\nYOU APPLIED TO {net_gain} JOBS TODAY...APPLY TO MORE""")    

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()