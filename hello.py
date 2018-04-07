from flask import Flask
import os

# import telepot
# import datetime
#example = environ.get('EXAMPLE)

app = Flask(__name__)

# def handle(msg):
#         chat_id = msg['chat']['id']
#         command = msg['text']
#         user = str(chat_id)
#         msg = ""
#         print( 'User: ' + user + ' Nachricht: ' + str(command) )
#
#         elif command == '/time':
#                 bot.sendMessage(chat_id, str(datetime.datetime.now()))
#
# bot = telepot.Bot('43211234')
# bot.message_loop(handle)

@app.route('/')
def hello_world():
    times = os.environ.get('EXAMPLE',3)
    return times

if __name__ == "__main__":
	app.run()


# @app.route('/env')
# def hello_example():
#     return example

# @app.route('/hello/<name>')
# def hello_name(name):
#    return 'Hello %s!' % name
