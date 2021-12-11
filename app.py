from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import tempfile, os
import datetime
import time
import json
import sys

sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi('mn0w8gkHEbWQQAbRC7sw1F1J9SFegKNHPVDsRfsAsuOJ2vgQPgx0/zB/ZeB6sM2ybrFrLh8qKKKsc97iPyW5/qUg0mPp7Tpfhkc9+RncWfdW4TUmscADLAW4FfurNsKgdElaTaLlzDA39SJG357lFgdB04t89/1O/w1cDnyilFU=')# Channel Access Token
handler = WebhookHandler('3e6656d8b069ab3bf6c057c1e1a84018')# Channel Secret
url = str("")
msgbuffer = str("")
success_login_status = int(0)
fail_login_status = int(0)
discord_webhook = 'https://discord.com/api/webhooks/919022348433231925/qROUJ50jdA40eL6dF7opy9dHOEKtq7cc9kDqi-qTSTcEZX73NHTdu3endVbJq5e0M4OR'
userlist = ["11021340","10922248","11021339","11052132"]
pwlist = ["Aa123456789","Opl5931665","Aa0123456789","Howard22922"]

def url_login(msg):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  url = str(msg)
  messageout = ""
  success_login_status = 0
  fail_login_status = 0
  for i in range(0,len(userlist),1):
     usr =  userlist[i]
     pwd = pwlist[i]
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
       messageout = (messageout + "學號:" + usr + "\n點名失敗\n錯誤訊息:密碼錯誤" + failmsg +'\n\n')#error login
       print("密碼錯誤")
       fail_login_status = fail_login_status +1
       wd.quit()
     else:
       soup = BeautifulSoup(wd.page_source, 'html.parser')
       #print(soup.prettify()) #html details
       if (soup.find_all(stroke="#D06079") != []):#fail
           messageout = (messageout + "學號:" + usr + "\n點名失敗，好可憐喔\n失敗訊息:" + wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text +'\n\n')
           print("點名失敗" + messageout)
           fail_login_status = fail_login_status +1
       elif (soup.find_all(stroke="#73AF55") != []):#success
           detailmsg = wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text
           messageout = (messageout + "學號:" + usr + "\n點名成功，歐陽非常感謝你\n成功訊息:" + detailmsg.replace('&#x6708;','月').replace('&#x65e5;','日').replace('&#x3a;',':')+'\n\n')
           print("點名成功" + messageout)
           success_login_status = success_login_status +1
       else:
           messageout = (messageout + "學號:" + usr + "\n發生未知的錯誤點名失敗，趕快聯繫管理員"+'\n\n')#unknown failure
           print("點名失敗" + messageout)
           fail_login_status = fail_login_status +1
  wd.quit()
  messageout = (messageout + '▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + "本次點名人數:" + str(len(userlist)) + "人\n" + "成功點名人數:" + str(success_login_status) + "人\n"+ "失敗點名人數:" + str(fail_login_status)+ "人")
  return messageout


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print("訊息:" + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("嚴重失敗!")
        abort(400)
    return 'OK'

def create_request_data(event, text=None) -> dict:
    profile = line_bot_api.get_group_member_profile(event.source.group_id,event.source.user_id)
    request_data = {
        "content":text,
        "username":profile.display_name + " from LINE",
        "avatar_url":profile.picture_url
    }
    return request_data

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) :
    msg = event.message.text
    if 'itouch.cycu.edu.tw' in msg :
      if 'learning_activity' in msg :
          msgbuffer = url_login(msg)
          line_bot_api.reply_message(event.reply_token, TextSendMessage('點名結束\n每次過程將會持續20~30秒\n(視點名人數及當前礙觸摸網路狀況而定)\n仍在測試中，不建議將此系統作為正式使用，在系統回覆點名狀態前建議不要離開本對話框，以免失效時來不及通知其他人手動點名\n若超過30分鐘無人使用，伺服器將會增加約10秒的開啟時間，請見諒\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + msgbuffer))
      else:
         line_bot_api.reply_message(event.reply_token, TextSendMessage('▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n請輸入正確的點名網址'))
    elif 'https://' in msg or '.com' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n此非itouch網域'))   
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n無法對這則訊息做出任何動作\n如要完成點名，請傳送該網址即可\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n系統若超過30分鐘無人使用會進入休眠模式，輸入的第一則連結會無法回覆，建議傳兩次'))
    request_data = create_request_data(event, event.message.text)
    requests.post(url=discord_webhook, data=request_data)
    return 

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入急難救助會~ \n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n如要完成點名，請傳送該網址即可')
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

