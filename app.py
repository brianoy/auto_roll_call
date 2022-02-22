from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests
import tempfile, os
import datetime
import time
import json
import random
import sys
import discord

sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
client = discord.Client()
app = Flask(__name__)
EAT = (["全家","7-11","中原夜市","鍋燒意麵","肉羹","拉麵","炒飯","賣麵庄","雞腿便當","摩斯漢堡","麥當勞","烤肉飯","肯德基","石二鍋",
"五花馬","燒肉","咖哩飯","牛排","肉燥飯","SUKIYA","霸味薑母鴨","高雄黑輪","凍飯","薩利亞","mint","火雞肉飯","品田牧場","滷味","Mr.三明治",
"雞柳飯","肉骨茶麵","泡麵","水餃","煎餃","包子","炒麵","鐵板燒","披薩","悟饕","河粉","肉圓","黑宅拉麵","壽司","牛肉麵","鹹酥雞"])
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi('mn0w8gkHEbWQQAbRC7sw1F1J9SFegKNHPVDsRfsAsuOJ2vgQPgx0/zB/ZeB6sM2ybrFrLh8qKKKsc97iPyW5/qUg0mPp7Tpfhkc9+RncWfdW4TUmscADLAW4FfurNsKgdElaTaLlzDA39SJG357lFgdB04t89/1O/w1cDnyilFU=')# Channel Access Token
handler = WebhookHandler('3e6656d8b069ab3bf6c057c1e1a84018')# Channel Secret
discord_webhook = 'https://discord.com/api/webhooks/919053709307179029/5whB53gtFXSykfAVcqsFOSSMA6-b_Y1yk4koHC0fx3snjTIweNuAz4qgGlYtIdVvHlev'
userlist = ["11021340","11021339","11021346","11021331","11021338"]
pwlist = ["aA123456789","Zz0123456789","Anson0610","dEEwYupDDCqh9","Daniel@123456"]
opId = "Ueca105de2ec07b6c502d6b639f56d119"
grouptoken = ["4C0ZkJflAfexSpelBcoEYVobqbbSD0aGFNvpGAVcdUX","vUQ1xrf4cIp7kFlWifowMJf4XHdtUSHeXi1QeUKARa9","WCIuPhhETZysoA6qjdx59kblgzbc6gQuVscBKS91Fi5"]
groupId = ['Cc97a91380e09611261010e4c5c682711','C0041b628a8712ace35095f505520c0bd','Cdebd7e16f5b52db01c3efd20b12ddd35']
url = str("")
msgbuffer = str("")
public_msgbuffer = str("")
success_login_status = int(0)
fail_login_status = int(0)
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
     wd = webdriver.Chrome('chromedriver',options=chrome_options)
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
       print("密碼錯誤\n------------------\n" + messageout)
       fail_login_status = fail_login_status +1
       wd.quit()
     else:
       soup = BeautifulSoup(wd.page_source, 'html.parser')
       #print(soup.prettify()) #html details
       if (soup.find_all(stroke="#D06079") != []):#fail
           messageout = (messageout + "學號:" + usr + "\n點名失敗，好可憐喔\n失敗訊息:" + wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text +'\n\n')
           print("點名失敗\n------------------\n" + messageout)
           fail_login_status = fail_login_status +1
       elif (soup.find_all(stroke="#73AF55") != []):#success
           detailmsg = wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text
           messageout = (messageout + "學號:" + usr + "\n點名成功，歐陽非常感謝你\n成功訊息:" + detailmsg.replace('&#x6708;','月').replace('&#x65e5;','日').replace('&#x3a;',':').replace('<br>','\n')+'\n\n')
           print("點名成功\n------------------\n" + messageout)
           success_login_status = success_login_status +1
       else:
           messageout = (messageout + "學號:" + usr + "\n發生未知的錯誤點名失敗，趕快聯繫管理員"+'\n\n')#unknown failure
           print("點名失敗\n------------------\n" + messageout)
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
    print("訊息從line進入:\n" + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("嚴重失敗!")
        abort(400)
    return 'OK'

@app.route("/")
def activate():
    print("強迫喚醒成功")
    return '強迫喚醒成功'

def deliver_data(public_msgbuffer, event_temp, text=None) -> dict:
    if (event_temp.source.type == "user"):

        profile = line_bot_api.get_profile(event_temp.source.user_id)
        request_data = {
          "content":"------------------------------------------\n\n" + "傳入機器人的訊息:\n" + text + "\n" + "傳出的訊息:\n" + public_msgbuffer + "\n\n------------------------------------------" ,
          "username":"<line 同步訊息><個人使用>   " + profile.display_name,
          "avatar_url":profile.picture_url
          }
    elif (event_temp.source.type == "group"):
        profile = line_bot_api.get_group_member_profile(event_temp.source.group_id,event_temp.source.user_id)
        request_data = {
          "content":"------------------------------------------\n\n" + "傳入機器人的訊息:\n" + text + "\n" + "傳出的訊息:\n" + public_msgbuffer + "\n\n------------------------------------------" ,
          "username":"<line 同步訊息><群組訊息>   " + profile.display_name,
          "avatar_url":profile.picture_url
         }
    return request_data

 #warning! reply token would expired after send msg about 30seconds. use push msg! 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) :
    public_msgbuffer = ""
    msg = event.message.text
    event_temp = event
    if 'itouch.cycu.edu.tw' in msg :
      if 'learning_activity' in msg :
          if (event.source.type == "group") :
               if(event.source.group_id == groupId[0]):
                   headers= {
                   "Authorization": "Bearer " + grouptoken[0], 
                   }
                   requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + "已收到網址，正在點名中，請靜待約20~30秒，若看見此訊息後請盡量不要重複傳送相同的訊息，以免造成系統塞車" })#翹課大魔王
                   msgbuffer = url_login(msg)
                   public_msgbuffer = ('點名結束\n每次過程將會持續20~30秒\n(視點名人數及當前礙觸摸網路狀況而定)\n仍在測試中，不建議將此系統作為正式使用，在系統回覆點名狀態前建議不要離開本對話框，以免失效時來不及通知其他人手動點名\n若超過30分鐘無人使用，伺服器將會增加約10秒的開啟時間，請見諒\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + msgbuffer)
                   payload = {'message': "\n" + public_msgbuffer }   
                   requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)#翹課大魔王
               elif(event.source.group_id == groupId[1]):
                   headers= {
                   "Authorization": "Bearer " + grouptoken[1], 
                   }
                   requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + "已收到網址，正在點名中，請靜待約20~30秒，若看見此訊息後請盡量不要重複傳送相同的訊息，以免造成系統塞車" })#秘密基地
                   msgbuffer = url_login(msg)
                   public_msgbuffer = ('點名結束\n每次過程將會持續20~30秒\n(視點名人數及當前礙觸摸網路狀況而定)\n仍在測試中，不建議將此系統作為正式使用，在系統回覆點名狀態前建議不要離開本對話框，以免失效時來不及通知其他人手動點名\n若超過30分鐘無人使用，伺服器將會增加約10秒的開啟時間，請見諒\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + msgbuffer)
                   payload = {'message': "\n" + public_msgbuffer }
                   requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)#秘密基地
               else:
                   line_bot_api.reply_message(event_temp.reply_token, TextSendMessage("已收到網址，正在點名中，請靜待約20~30秒，若看見此訊息後請盡量不要重複傳送相同的訊息，以免造成系統塞車"))
                   msgbuffer = url_login(msg)
                   public_msgbuffer = ('點名結束\n每次過程將會持續20~30秒\n(視點名人數及當前礙觸摸網路狀況而定)\n仍在測試中，不建議將此系統作為正式使用，在系統回覆點名狀態前建議不要離開本對話框，以免失效時來不及通知其他人手動點名\n若超過30分鐘無人使用，伺服器將會增加約10秒的開啟時間，請見諒\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + msgbuffer)
                   payload = {'message': "\n" + public_msgbuffer }
                   print("有不知名的群組")
                   line_bot_api.push_message(event_temp.source.group_id, TextSendMessage(public_msgbuffer))#除了以上兩個群組
          elif (event.source.type == "user") :
              line_bot_api.reply_message(event_temp.reply_token, TextSendMessage("已收到網址，正在點名中，請靜待約20~30秒，若一個人已傳網址則不需重複傳送"))
              msgbuffer = url_login(msg)
              public_msgbuffer = ('點名結束\n每次過程將會持續20~30秒\n(視點名人數及當前礙觸摸網路狀況而定)\n仍在測試中，不建議將此系統作為正式使用，在系統回覆點名狀態前建議不要離開本對話框，以免失效時來不及通知其他人手動點名\n若超過30分鐘無人使用，伺服器將會增加約10秒的開啟時間，請見諒\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + msgbuffer)
              line_bot_api.push_message(event_temp.source.user_id, TextSendMessage(public_msgbuffer))
          else:
              print("錯誤:偵測不到itouch網址訊息類型")
              line_bot_api.reply_message(event.reply_token, TextSendMessage("偵測不到itouch網址類型，請再試一次"))
      else:
          public_msgbuffer = ('▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n請輸入正確的點名網址')
          line_bot_api.reply_message(event.reply_token, TextSendMessage(public_msgbuffer))
    elif 'https://' in msg or '.com' in msg :
        public_msgbuffer = ('▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n此非itouch網域')
        if (event.source.type == "group") :
            if(event.source.group_id == groupId[0]):
                headers= {
                "Authorization": "Bearer " + grouptoken[0], 
                }
                requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': public_msgbuffer })#翹課大魔王
            elif(event.source.group_id == groupId[1]):
                headers= {
                "Authorization": "Bearer " + grouptoken[1], 
                }
                requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n好像有人傳了網址還是怎麼樣的" })#秘密基地
            elif(event.source.group_id == groupId[2]):
                headers= {
                "Authorization": "Bearer " + grouptoken[2], 
                }
                requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n好像有人傳了網址還是怎麼樣的" })#小歐陽機器人
            else:
                public_msgbuffer = ('▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n此非itouch網域')
                line_bot_api.reply_message(event.reply_token, TextSendMessage(public_msgbuffer))
    elif '變更權杖:' in msg:
        if opId == event.source.user_id :
           print("開始變更權杖")
           line_bot_api.reply_message(event.reply_token, TextSendMessage("已變更權杖"))
        else:
            print("變更權杖失敗，沒有權限")
            line_bot_api.reply_message(event.reply_token, TextSendMessage("沒有權限，無法變更權杖"))
    elif '要吃什麼' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(EAT[random.randint(0,len(EAT))]))
    elif '女朋友' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("你沒有女朋友啦幹"))
    elif '閉嘴' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("你好兇喔"))
    elif '約' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("又要約又要約"))
    elif '王顥' in msg and '單身' in msg:
        days = datetime.datetime.today()-datetime.datetime(2019,4,30,16)
        days = str(days)[0:4]
        sendbuffer = "小提醒:王顥已單身"+ days +"天"
        print(sendbuffer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(sendbuffer))
    elif '開啟' in msg :
        print("強制喚醒")
    else:
        public_msgbuffer = ('▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n無法對這則訊息做出任何動作\n如要完成點名，請傳送該網址即可\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n系統若超過30分鐘無人使用會進入休眠模式，輸入的第一則連結會無法回覆，建議傳兩次')
        if (event.source.type == "group") :
            if(event.source.group_id == groupId[0]):
                headers= {
                "Authorization": "Bearer " + grouptoken[0], 
                }
                #requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': public_msgbuffer })#翹課大魔王
            elif(event.source.group_id == groupId[1]):
                headers= {
                "Authorization": "Bearer " + grouptoken[1], 
                }
                requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': (public_msgbuffer) })#秘密基地
            elif(event.source.group_id == groupId[2]):
                headers= {
                "Authorization": "Bearer " + grouptoken[2], 
                }
                #requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': (public_msgbuffer) })#煤船組
            else:
                print("有不知名的群組傳送了非相關訊息")
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(public_msgbuffer))
    request_data = deliver_data(public_msgbuffer, event_temp, event.message.text)
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

