import telepot
from telepot.loop import MessageLoop
import datetime
import json
import time
import googleConnect
import re
from pprint import pprint

config = json.load(open('private/config.json'))
BOT_TOKEN = config['telegram']['token']
VALID_USER = int(config['telegram']['account'])

checkValue = False
checkPlace = False
value = 0.0
place = "nowhere"

def handle(msg):
    global value
    global place
    global checkPlace
    global checkValue

    chat_id = msg['chat']['id']
    command = msg['text']
    user = str(chat_id)
    print( 'User: ' + user + ' Nachricht: ' + str(command) )

    if(chat_id != VALID_USER):
        #bot.sendMessage(chat_id, "Darfst niicht")
        return
    #string mit zahl -> Problem
    if re.search(r"\d\d[-]\d\d", command):
        expenses(msg)

    elif re.search(r"\d+[,.]?\d?\d?", command):
        if(checkPlace):
            bot.sendMessage(chat_id, "Adding place and value.")
        else:
            bot.sendMessage(chat_id, "Where did you spend the money?")
        value = float(command.replace(",","."))
        checkValue = True
        print("Changed value: {}".format(command))
    #nachträglich
    elif command == '/guide':
         bot.sendMessage(chat_id, "18-04 -> Expenses for April 2018 \n 22,32 new entry")

    elif command == '/clear':
         checkPlace = False
         checkValue = False
         value = 0
         place = "nowhere"

         bot.sendMessage(chat_id,"B")
    else:
        if(checkValue):
            bot.sendMessage(chat_id, "Adding place and value.")
        else:
            bot.sendMessage(chat_id, "How much did you spend?")
        place = command
        checkPlace = True
        print("Changed place: {}".format(command))

    if(checkValue and checkPlace):
        addPrice(msg)


def addPrice(msg):
    sheet = googleConnect.getSheet(2)
    chat_id = msg['chat']['id']

    global value
    global place
    global checkPlace
    global checkValue

    timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    print("Adding Values to spreadsheet")
    print("Value: {}".format(value))
    print("Place: {}".format(place))
    print("timestamp: {}".format(timestamp))

    columEntries = len(sheet.col_values(1))+1
    sheet.update_cell(columEntries, 1, timestamp)
    sheet.update_cell(columEntries, 2, value)
    sheet.update_cell(columEntries, 3, place)
    sheet.update_cell(columEntries, 4, timestamp[:5])
    checkPlace = False
    checkValue = False
    bot.sendMessage(chat_id, "Values added.")

def expenses(msg):
    sheet = googleConnect.getSheet(2)
    spending = 0.0
    chat_id = msg['chat']['id']
    date = msg['text']

    for x in sheet.findall(date):
        if(x.row == 1):
            spending = sheet.cell(2,(x.col)).value
    print("Expense for: {} is {}€".format(date, spending))
    bot.sendMessage(chat_id, "Expense for: {} is {}€".format(date, spending))

bot = telepot.Bot(BOT_TOKEN)
#bot.message_loop(handle)
MessageLoop(bot, handle).run_as_thread()

print( 'I am listening ...')

while True:
    time.sleep(10)
