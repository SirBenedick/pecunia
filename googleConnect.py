import gspread
from oauth2client.service_account import ServiceAccountCredentials


def getSheet(sheetNumber):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('private/creds.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    #sheet = client.open("Instagram-Insights").sheet1
    sh = client.open('MannheimMoney')
    sheet = sh.get_worksheet(sheetNumber)
    return sheet
