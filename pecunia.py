#1.0
import telepot
import datetime

BOT_TOKEN = str(os.environ.get('BOT_TOKEN',3))

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        user = str(chat_id)
        msg = ""
        print( 'User: ' + user + ' Nachricht: ' + str(command) )

        elif command == '/time':
                bot.sendMessage(chat_id, str(datetime.datetime.now()))

bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handle)

print( 'I am listening ...')

while 1:
    time.sleep(10)
