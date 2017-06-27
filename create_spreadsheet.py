import httplib2
import json
import urllib

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

def get_spreadsheets_service():
    CREDENTIALS_FILE = 'creds.json'
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILES, scopes)
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    return service

def get_drive_service():
    CREDENTIALS_FILE = 'creds.json'
    scopes = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE, scopes)
    http = credentials.authorize(httplib2.Http())
    service = build('drive', 'v3', http=http)
    return service

def create_new_spreadsheet():
    PARENT_FOLDER_ID = 'parent_folder_id'
    FILE_NAME = 'skimtest'
    drive_service = get_drive_service()
    file_metadata = {
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'name': FILE_NAME,
        'parents': [PARENT_FOLDER_ID]
    }
    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    file_id = file.get('id')
    print 'Created file ID: %s' % file_id
    return file_id

def write_to_spreadsheet(file_id, data):
    sheets_service = get_spreadsheets_service()
    range_ = 'Sheet1!A:B'
    sheets_service.spreadsheets().values().update(
        spreadsheetId=file_id,
        range=range_,
        valueInputOption='RAW',
        body=data).execute()

def main():
    file_id = create_new_spreadsheet()
    data = {
      "values": [
        ["Steven", "Male"],
        ["Jacob", "Male"],
      ]
    }
    write_to_spreadsheet(file_id, data)

if __name__ == '__main__':
    main()

