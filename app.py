from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#from selenium import webdriver
#from bs4 import BeautifulSoup

#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('mn0w8gkHEbWQQAbRC7sw1F1J9SFegKNHPVDsRfsAsuOJ2vgQPgx0/zB/ZeB6sM2ybrFrLh8qKKKsc97iPyW5/qUg0mPp7Tpfhkc9+RncWfdW4TUmscADLAW4FfurNsKgdElaTaLlzDA39SJG357lFgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3e6656d8b069ab3bf6c057c1e1a84018')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if 'https://' in msg:
        message = "this is website"
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = "我不知道你在說什麼欸"
        line_bot_api.reply_message(event.reply_token, message)



@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入急難救助會')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
