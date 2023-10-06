from dotenv import dotenv_values
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load config
input_path = 'input/google_drive_upload/'
config = dotenv_values(f'{input_path}google_drive_upload.env')
driveId = config.get('driveId')

# build service
credentials_file = f'{input_path}service_account_key.json'
scopes = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=scopes)
service = build('drive', 'v3', credentials=credentials)


def run(data: dict):

    # determine create ot update
    all_files_dict = dict()
    all_files = service.files().list(q=f"'{driveId}' in parents").execute()
    for file in all_files.get('files'):
        all_files_dict[file.get('name')] = file.get('id')
    print(f'Existing ids: {all_files_dict}')

    result = dict()
    for key, value in data.items():
        media = MediaFileUpload(value, mimetype='audio/mp3')
        filename = f'{key}.mp3'
        if filename in all_files_dict.keys():
            request = service.files().update(fileId=all_files_dict.get(filename), media_body=media, body={
                'name': filename
            })
        else:
            request = service.files().create(media_body=media, body={
                'parents': [driveId],
                'name': filename
            })
        response = request.execute()
        print(response)
        result[key] = response['id']

    print(f'Processed: {result}')
    return result
