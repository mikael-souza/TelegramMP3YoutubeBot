import requests
import time
import json
import pafy
import os
import configparser as cfg


class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)
            
    def send_audio(self, msg, chat_id):
        if "youtube.com/watch?v=" in msg or "youtu.be/" in msg:
            try:
                video = pafy.new(msg)
                if video.title is not None:
                    audiom4a = video.getbestaudio(preftype="m4a")
                    audiom4a.download(quiet=True)
                    url = self.base + "sendAudio?chat_id={}".format(chat_id)
                    
                    requests.post(url, files={'audio':open(r''+video.title+'.m4a', 'rb')})
                    time.sleep(300)
                    os.remove('./'+video.title+'.m4a')
            except:
                return None
            
    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
