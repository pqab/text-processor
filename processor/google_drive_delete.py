import csv
from dotenv import dotenv_values
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load config
input_path = 'input/google_drive_delete/'
config = dotenv_values(f'{input_path}google_drive_delete.env')
driveId = config.get('driveId')

# build service
credentials_file = f'{input_path}service_account_key.json'
scopes = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=scopes)
service = build('drive', 'v3', credentials=credentials)


def run(data: dict):

    result = dict()

    file = open(f'{input_path}input.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        key = row[0]
        request = service.files().delete(fileId=key)
        response = request.execute()
        result[key] = None

    print(f'Processed: {result}')
    return result
