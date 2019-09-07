import gspread
from oauth2client.service_account import ServiceAccountCredentials

sheet = False

def getSheet():
    global sheet

    if sheet:
        print("Sheet existed, no need for refetch.")
        return sheet
    else:
        print("Fetching Sheet for the first time.")
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('privatePecunia/creds.json', scope)
        client = gspread.authorize(creds)
            
        # Find a workbook by name and open the first sheet
        workbook = client.open('WORKBOOK NAME')
        sheet = workbook.worksheet("SHEET NAME")
        return sheet