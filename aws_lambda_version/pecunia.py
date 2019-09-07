import json
from botocore.vendored import requests
import googleConnect
from datetime import datetime
from pytz import timezone


config = json.load(open('privatePecunia/config.json'))
TELE_TOKEN = config['telegram']['token']
TELE_CHATID = int(config['telegram']['account'])
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)
TIMESTAMP_COLUM = 1
VALUES_COLUM = 2
DESCRIPTION_COLUM = 3


def check_if_value_is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def add_timestamp(colum):
    sheet = googleConnect.getSheet()

    timeFormat = "%y-%m-%d-%H-%M"
    eastern = timezone('US/Eastern')

    timestamp = datetime.now(eastern).strftime(timeFormat)

    sheet.update_cell(colum, 1, timestamp)

def compare_price_description_length():
    sheet = googleConnect.getSheet()

    columValue = len(sheet.col_values(VALUES_COLUM))+1
    columDescription = len(sheet.col_values(DESCRIPTION_COLUM))+1

    if columValue > columDescription:
        return "Please enter the description."
    elif columValue < columDescription:
        return "Please enter the value."
    else:
        return "All values added."

def add_value_to_sheet(msg):
    sheet = googleConnect.getSheet()

    if(check_if_value_is_number(msg)):
        # add price
        columEntries = len(sheet.col_values(VALUES_COLUM))+1
        sheet.update_cell(columEntries, VALUES_COLUM, msg)
        add_timestamp(columEntries)
    else:
        # add description
        columEntries = len(sheet.col_values(DESCRIPTION_COLUM))+1
        sheet.update_cell(columEntries, DESCRIPTION_COLUM, msg)
        add_timestamp(columEntries)

def send_message(msg, chatId):
    url = URL + "sendMessage?text={}&chat_id={}".format(msg, chatId)
    requests.get(url)

def handle_command(msg, chatId):
    sheet = googleConnect.getSheet()

    if msg == "/month":
        final_response = "Your expenses are: \n"

        # position where monthly expenses are calculated in google sheets
        row = 1
        colum = 7
        # generates message for each month that has expenses
        while True:
            month = sheet.cell(row, colum).value
            monthly_expense = sheet.cell(row + 1 , colum).value

            if month == "":
                break

            monthly_respsonse = month + ": " + monthly_expense + "\n"
            final_response += monthly_respsonse
            colum += 1

        send_message(final_response, chatId)

def lambda_handler(event, context):
    lambdaMessage = json.loads(event['body'])
    chatId = lambdaMessage['message']['chat']['id']
    replyFromTelegram = lambdaMessage['message']['text']

    # access controll
    if chatId != TELE_CHATID:
        send_message("Sorry, access denied!", chatId)
        return {'statusCode': 200}
    
    # check if msg is a command
    if replyFromTelegram[0] == "/":
        handle_command(replyFromTelegram, chatId)
        return {'statusCode': 200}
    
    # else add expense to sheet    
    add_value_to_sheet(replyFromTelegram)
    send_message(compare_price_description_length(), chatId)

    return {'statusCode': 200}
