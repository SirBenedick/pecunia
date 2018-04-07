from flask import Flask
import telepot
import random
import datetime
import time
import subprocess

app = Flask(__name__)

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        user = str(chat_id)
        msg = ""
        print( 'User: ' + user + ' Nachricht: ' + str(command) )

        if command == '/roll':
                bot.sendMessage(chat_id, random.randint(1,6))
        elif command == '/time':
                bot.sendMessage(chat_id, str(datetime.datetime.now()))
        elif command == '/temp':
                msg = subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp")
                bot.sendMessage(chat_id,msg)
                print(user + ": " + msg )
bot = telepot.Bot('431470615:AAFPuJvtiSWiAr2NdYxDVYwXlggUgq09hRQ')
bot.message_loop(handle)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name
