from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import tempfile, os
import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi('mn0w8gkHEbWQQAbRC7sw1F1J9SFegKNHPVDsRfsAsuOJ2vgQPgx0/zB/ZeB6sM2ybrFrLh8qKKKsc97iPyW5/qUg0mPp7Tpfhkc9+RncWfdW4TUmscADLAW4FfurNsKgdElaTaLlzDA39SJG357lFgdB04t89/1O/w1cDnyilFU=')# Channel Access Token
handler = WebhookHandler('3e6656d8b069ab3bf6c057c1e1a84018')# Channel Secret
url = str("")
msgbuffer = str("")
userlist = ["11021340"]
pwlist = ["Aa123456789"]
login_status_list = []

def url_login(msg,usr,pwd):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  url = str(msg)
  messageout = ""
  wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
  wd.get(url)
  wd.execute_script('document.getElementById("UserNm").value ="' + usr + '"')
  wd.execute_script('document.getElementById("UserPasswd").value ="' + pwd + '"')
  wd.execute_script('document.getElementsByClassName("w3-button w3-block w3-green w3-section w3-padding")[0].click();')
  from selenium.webdriver.support import expected_conditions as EC
  fail = EC.alert_is_present()(wd)#如果有錯誤訊息
  if fail:
    failmsg = fail.text
    fail.accept()
    messageout = ("學號:" + usr + '\\n' + "點名錯誤，錯誤訊息:" + failmsg)#error login
    wd.quit()
  else:
    soup = BeautifulSoup(wd.page_source, 'html.parser')
    #print(soup.prettify()) #html details
    if (soup.find_all(stroke="#D06079") != []):#fail
        messageout = ("學號:" + usr + '\\n' +"點名失敗，好可憐喔，失敗訊息:" + wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text + '\\n')
        login_status_list.append("0")
    elif (soup.find_all(stroke="#73AF55") != []):#success
        detailmsg = wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text
        messageout = ("學號:" + usr + '\\n' +"點名成功，歐陽非常感謝你，成功訊息:" + detailmsg.replace('&#x6708;','月').replace('&#x65e5;','日').replace('&#x3a;',':') + '\\n')
        login_status_list.append("1")
    else:
        messageout = ("學號:" + usr + '\\n' +"發生未知的錯誤"+ '\\n' + "點名失敗，趕快聯繫管理員" + '\\n')#unknown failure
        login_status_list.append("0")
    wd.quit()
    return messageout


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
def handle_message(event) :
    msg = event.message.text
    usr = ""
    pwd = ""
    msgbuffer = "" 
    login_status_list = []
    if 'itouch.cycu.edu.tw' in msg :
      if 'itouch.cycu.edu.tw/active_system/query_course/learning_activity' in msg :
         for i in range(0,len(userlist),1):
           usr = userlist[i]
           pwd = pwlist[i]
           msgbuffer = (msgbuffer + url_login(msg,usr,pwd))
           msgbuffer = (msgbuffer + '--------------------' + '\\n')
         msgbuffer = (msgbuffer + "本次點名人數:" + len(userlist) + "人" + '\\n')
         msgbuffer = (msgbuffer + "成功點名人數:" + login_status_list.count("1") + "人" + '\\n')
         msgbuffer = (msgbuffer + "失敗點名人數:" + login_status_list.count("0") + "人" + '\\n')
         line_bot_api.reply_message(event.reply_token, TextSendMessage(msgbuffer))
      else:
         line_bot_api.reply_message(event.reply_token, TextSendMessage('請輸入正確的點名網址'))
    elif 'https://' in msg or '.com' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('此非itouch網域'))   
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('無法對這則訊息做出任何動作' + '\\n' + '如要完成點名，請傳送該網址即可'))
    return 


@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入歐陽急難救助會~')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

