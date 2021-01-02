from flask import Flask, render_template, request
import googleapiclient.discovery
from google.oauth2 import service_account

def get_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    GOOGLE_PRIVATE_KEY = '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPWFGTFhfFlHaE\nevvCTe1VURp+CWpH/WCGm2Xrmh5WVoD2xkoD2101ld7CS9/aPi9kNt6Vyu/eTlQ1\nDOpOx4Sv3H0FnwsZKe4Uf/anJ1Hk1QboppN1eaKxv4jKSO/G9v24W/AkMx3+ZYxV\ngtZ2c2SvUP/phPpp2mvrVyE8dNzZjQQmqQf3iscINrmendvhaI9IhmSH1GeNJlTB\niQQWE8HG4MQxsFOs2uxhr9cbBGI5eJwQ/yY9CWTnvzrt2pLkTZiS+ly2XwEozzHr\ngtYFTARgaanxpr4yA7liJ5UaBkyKG3Idr7gRLnZos+nUtpopPCIDlCSh8xCRUWqN\nUfF4xhK9AgMBAAECggEABDFMRYCOa8V8B+5EQc/KAsZPVONim+jByNNvvN8yRvUw\nasdW79ub03mRh95J6wC0SHqVsmI6oiZpWRnfxTPEYj5mhmJl+TOcQTY9mRr8eV8a\nXMtOdyT6c2Ig6/BhLvvCD6vaD2eoAhenQ0hYjHizN7DR+LBegKJrqKOmQbXrUGOV\nGuogAQv9DWYLsZftEVE4Ay6OwV5eUeG4hqpjI0dcT7oMuevHpju5geM6D8DenxY9\n1p+dnG0MzLTseeIcuijcGZqCxPBvLGNKiatlhNbY8GZtJfb6gTD/bX1v5pkhFSrl\nu9bZP8SseyG66y7GQTBRGqamiG0lhGAtntq/G1rFAwKBgQDIFE0GeIfJSEJy/g9c\niK8H1b24fwQJ04j7tCgLxtr18/TgsyOhip+fYQA3KLhe/W1F298GJPGeAqJ6dmax\nHM0JtLZq7vh/nMU7ESt9Eiq/8MlnpTwz7w0GeBqIRhE81x571mfl/69EkUSQsv7D\nzZaCII01VT08QeXPF9RhLvUtbwKBgQC3aKvK8FU5h7cNLjf//jQy1UrlKSO+w0q2\nd0avqAkEN2UBeySl7x6kxuSQNkjvc8EirIGcRWmuk4DkgeFb4LW+mKWcgvi1vufD\nIN3EKWpDACvWmiCfS7u9xzvaXLwCgSctmtRfuxkU+bUwodCTS/eWXULrmCqVwnkT\nDUUH9gzEkwKBgDJjcnaTulbF3P5K36GFRtdpTAt/6Ytz+8awO3mjzhctJlnEo8+W\nMtcXvc8mcTBzEKcMVaGdgkAyF6tR0FEAmN695UcPAgRZfg5/J32rKpsGUCLLKVtG\n8/fSHZR+WO8CmknD2IzDFOfm0ebDPYggaaxB+G4bFn3rdq3uKW2EPvj/AoGAPt0q\nnPl5TKm+zU69NQotXAsNi7RpIxaPAjGp0cVXqdFO1o4dxp5KM5JUfzWMFD7pwPe9\nyRFlose+ExSNaM+Bm914Tkf59VmE2LXoLTdAy8xAOmNDsTXlGKw0UKkebAFWq2P5\nTQK1GyJnv06HTiVorGo06MmUNxacJzKSKaNlRu8CgYB9+nsnUCFvOCn380Itn4jE\nyXmB0bsbNBL/IhjifAVnFYQoHwiN4xxMdlyozLY8TJbnwA5nDobuousbO1L94Imv\nEE1r7FqKUnTLS3tU2BRPR1AUw5IuimJg8wXrWYvRUsc970KKCH1oNpwc838PlAMw\n8jrmyp7p7qhamtSxXUivwg==\n-----END PRIVATE KEY-----\n'
    GOOGLE_CLIENT_EMAIL = 'servaccount@silver-asset-300523.iam.gserviceaccount.com'
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
    spreadsheet_id = '1PaPQzx_w1YaDaW82fZFvX9lOx9gmrKop9rUGiL4L2CA'
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