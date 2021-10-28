from flask import Flask, render_template, request
import googleapiclient.discovery
from google.oauth2 import service_account

def get_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    GOOGLE_PRIVATE_KEY = '-----BEGIN PRIVATE KEY-----'
    GOOGLE_CLIENT_EMAIL = ''
    # The environment variable has escaped newlines, so remove the extra backslash
    GOOGLE_PRIVATE_KEY = GOOGLE_PRIVATE_KEY.replace('\\n', '\n')

    account_info = {
      "private_key": GOOGLE_PRIVATE_KEY,
      "client_email": GOOGLE_CLIENT_EMAIL,
      "token_uri": "https://accounts.google.com/o/oauth2/token",
    }

    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
    return credentials

def get_service(service_name='sheets', api_version='v4'):
    credentials = get_credentials()
    service = googleapiclient.discovery.build(service_name, api_version, credentials=credentials)
    return service

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    service = get_service()
    spreadsheet_id = ''
    range_name = 'Sheet1!A2:E'
    if request.method == 'POST':
        lst = []
        score = 0
        name = [request.form.get('Name')]
        question1 = [request.form.get('Question1')]
        if 'yes' in question1:
            score += 1
        question2 = [request.form.get('Question2')]
        if 'yes' in question2:
            score += 3
        question3 = [request.form.get('Question3')]
        if 'yes' in question3:
            score += 3
        lst.append(name)
        lst.append(question1)
        lst.append(question2)
        lst.append(question3)
        lst.append([score])
        body = {
            'majorDimension': 'COLUMNS',
            'values': lst
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name, valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body=body).execute()
           
        return 'Done'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
