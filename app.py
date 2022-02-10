from bot import telegram_chatbot
from flask import Flask, request, jsonify
import streamlit as st

app = Flask(__name__)
app.debug = True

bot = telegram_chatbot(st.secrets["token"])

@app.route('/webhook', methods=['POST'])
def make_reply(msg):
    reply = None
    if msg is not None:
#        reply = msg
        if "youtube.com/watch?v=" in msg or "youtu.be/" in msg:
            reply = msg
        else:
            reply = None
    return reply

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            first_name = item["message"]["from"]["first_name"]
            from_ = item["message"]["from"]["id"]
            reply = make_reply(message)            
#            bot.send_message(reply, from_)
            if reply is not None:
                bot.send_audio(reply, from_)
            else:
                reply = "Please, send a valid video url."
                bot.send_message(reply, from_)
