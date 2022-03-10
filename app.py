from glob import glob
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
import os
import datetime
import random
import sys
import discord
import asyncio
import time

sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
client = discord.Client()
app = Flask(__name__)

EAT = (["全家","7-11","中原夜市","鍋燒意麵","肉羹","拉麵","炒飯","賣麵庄","雞腿便當","摩斯漢堡","麥當勞","烤肉飯","肯德基","石二鍋",
"五花馬","燒肉","咖哩飯","牛排","肉燥飯","SUKIYA","霸味薑母鴨","高雄黑輪","凍飯","薩利亞","mint","火雞肉飯","品田牧場","滷味","Mr.三明治",
"雞柳飯","肉骨茶麵","泡麵","水餃","煎餃","包子","炒麵","鐵板燒","披薩","悟饕","河粉","肉圓","黑宅拉麵","壽司","牛肉麵","鹹酥雞"])

STICKER_LIST = {'465400171':'ㄌㄩㄝ','465400158':'才不美','465400159':'Woooooooow','465400160':'不可以','465400161':'怎樣啦 輸贏啦','465400163':'假K孝濂給',
'465400165':'累屁','465400166':'聽話 讓我看看','465400169':'到底??????','465400172':'他在已讀你','465400173':'大概24小時後才會回你','13744852':'哼',
'349572675':'可憐哪','352138078':'吃屎阿','464946842':'對咩對咩','464946834':'ㄏㄏ','464946841':'亂講','435674449':'嘿嘿','435674452':'兇屁'}

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi('mn0w8gkHEbWQQAbRC7sw1F1J9SFegKNHPVDsRfsAsuOJ2vgQPgx0/zB/ZeB6sM2ybrFrLh8qKKKsc97iPyW5/qUg0mPp7Tpfhkc9+RncWfdW4TUmscADLAW4FfurNsKgdElaTaLlzDA39SJG357lFgdB04t89/1O/w1cDnyilFU=')# Channel Access Token
handler = WebhookHandler('3e6656d8b069ab3bf6c057c1e1a84018')# Channel Secret
discord_webhook = 'https://discord.com/api/webhooks/919053709307179029/5whB53gtFXSykfAVcqsFOSSMA6-b_Y1yk4koHC0fx3snjTIweNuAz4qgGlYtIdVvHlev'
userlist = ["11021340","11021339","11021346","11021331","11021338","11021337","11021325"]
pwlist = ["aA123456789","Zz0123456789","Angel0610","dEEwYupDDCqh9","Daniel@123456","Wolf1017","Ray11021325"]
namelist = ["歐陽立庭","蔡祐恩","洪晨旻","楊智涵","楊其宸","張子恆","江昱叡"]
useridlist = []
opuuId = "Ueca105de2ec07b6c502d6b639f56d119"
grouptoken = ["4C0ZkJflAfexSpelBcoEYVobqbbSD0aGFNvpGAVcdUX","vUQ1xrf4cIp7kFlWifowMJf4XHdtUSHeXi1QeUKARa9","WCIuPhhETZysoA6qjdx59kblgzbc6gQuVscBKS91Fi5"]
groupId = ['Cc97a91380e09611261010e4c5c682711','C0041b628a8712ace35095f505520c0bd','Cdebd7e16f5b52db01c3efd20b12ddd35']
url = str("")
msgbuffer = str("")
public_msgbuffer = str("")

global success_login_status 
success_login_status = int(0)
global fail_login_status
fail_login_status = int(0)
global single_msg_list
single_msg_list = []

async def login_pros(msg,usr,pwd,name):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  await asyncio.sleep(1)
  url = str(msg)
  messageout = ""
  global success_login_status
  global fail_login_status
  wd = webdriver.Chrome('chromedriver',options=chrome_options)
  wd.get(url)
  not_open = "未開放 QRCODE簽到功能" in wd.page_source
  if not_open:
     fail_login_status = len(userlist)
     messageout = "\n🟥警告❌，點名並沒有開放，請稍後再試或自行手點，全數點名失敗\n"
  else:
     wd.execute_script('document.getElementById("UserNm").value ="' + usr + '"')
     wd.execute_script('document.getElementById("UserPasswd").value ="' + pwd + '"')
     wd.execute_script('document.getElementsByClassName("w3-button w3-block w3-green w3-section w3-padding")[0].click();')
     print("有到第一點")
     password_wrong = EC.alert_is_present()(wd)#如果有錯誤訊息
     print("有到第二點")
     if password_wrong:
       failmsg = password_wrong.text
       password_wrong.accept()
       messageout = (messageout + "學號:" + usr + "\n🟥點名失敗❌\n錯誤訊息:密碼錯誤" + failmsg +'\n\n')#error login
       print("密碼錯誤\n------------------\n" + messageout)
       fail_login_status = fail_login_status +1
       wd.quit()
     else:
       print("有到第三點")
       soup = BeautifulSoup(wd.page_source, 'html.parser')
       if(soup.find_all(stroke="#D06079") != []):#fail
            messageout = (messageout + "\n🟥點名失敗❌，"+ name +"好可憐喔😱\n失敗訊息:" + wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text +'\n\n')
            print("點名失敗\n------------------\n" + messageout)
            fail_login_status = fail_login_status +1
       elif(soup.find_all(stroke="#73AF55") != []):#success
            detailmsg = wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text
            messageout = (messageout + "\n🟩點名成功✅，"+ name +"會非常感謝你\n成功訊息:" + detailmsg.replace('&#x6708;','月').replace('&#x65e5;','日').replace('&#x3a;',':').replace('<br>','\n')+'\n\n')
            print("點名成功\n------------------\n" + messageout)
            success_login_status = success_login_status +1
       else:
            messageout = (messageout + name + "\n🟥發生未知的錯誤❌，" + "學號:" + usr + " " + name + "點名失敗😱，趕快聯繫布萊恩，並自行手點" + '\n\n')#unknown failure
            print("點名失敗\n------------------\n" + messageout)
            fail_login_status = fail_login_status +1
     print("有到第四點")
  single_msg_list.append(messageout)
  wd.quit()
  return messageout

async def url_login(msg):
    global success_login_status
    global fail_login_status
    global single_msg_list
    success_login_status = 0
    fail_login_status = 0
    single_msg_list = []
    start_time = time.time()
    results = await asyncio.gather(*[login_pros(msg,userlist[i],pwlist[i],namelist[i]) for i in range(userlist)])
    for i in range(len(single_msg_list)):
        messageout = messageout + '▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + single_msg_list[i]
    messageout = (messageout + '▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + "本次點名人數:" + str(len(userlist)) + "人\n" + "成功點名人數:" + str(success_login_status) + "人\n"+ "失敗點名人數:" + str(fail_login_status)+ "人")
    messageout = (messageout + '\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + "最近一次更新:" + os.environ['HEROKU_RELEASE_CREATED_AT'] + "GMT+0\n" + "版本:" + os.environ['HEROKU_RELEASE_VERSION']+ "\n此次點名耗費時間:" + str(time.time() - start_time)+"秒")
    print(results)
    return str(messageout)

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


def distinguish(msgbuffer):
    if (fail_login_status > 0):
        msgbuffer = "🟥\n" + msgbuffer
    else:
        msgbuffer = "🟩\n" + msgbuffer
    return msgbuffer

 #warning! reply token would expired after send msg about 30seconds. use push msg! 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) :
    public_msgbuffer = ""
    msg = event.message.text
    msg_type = event.message.type
    print(msg_type)
    #print(event)
    event_temp = event
    recived = '已收到網址，正在點名中，請靜待約20~30秒，若看見此訊息後請盡量不要重複傳送相同的訊息，以免造成系統塞車'
    done = '點名結束\n每次過程將會持續20~30秒\n(視點名人數及當前礙觸摸網路狀況而定)\n仍在測試中，不建議將此系統作為正式使用，在系統回覆點名狀態前建議不要離開本對話框，以免失效時來不及通知其他人手動點名\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' 
    announce = '▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n'
    if 'itouch.cycu.edu.tw' in msg :
         if 'learning_activity' in msg :
             if (event.source.type == "group") :
                 if(event.source.group_id == groupId[0]):
                      headers= {
                      "Authorization": "Bearer " + grouptoken[0], 
                      }
                      requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + recived })#翹課大魔王
                      msgbuffer = url_login(msg)
                      public_msgbuffer = done + msgbuffer
                      payload = {'message': distinguish(public_msgbuffer) }
                      requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
                 elif(event.source.group_id == groupId[1]):
                      headers= {
                      "Authorization": "Bearer " + grouptoken[1], 
                      }
                      requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + recived })#秘密基地
                      msgbuffer = url_login(msg)
                      public_msgbuffer = done + msgbuffer
                      payload = {'message': distinguish(public_msgbuffer) }
                      requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
                 else:
                      line_bot_api.reply_message(event_temp.reply_token, TextSendMessage(recived))
                      msgbuffer = url_login(msg)
                      public_msgbuffer = done + msgbuffer
                      payload = {'message': distinguish(public_msgbuffer) }
                      print("有不知名的群組")
                      line_bot_api.push_message(event_temp.source.group_id, TextSendMessage(distinguish(public_msgbuffer)))#除了以上兩個群組
             elif(event.source.type == "user") :
                  line_bot_api.reply_message(event_temp.reply_token, TextSendMessage(recived))
                  msgbuffer = url_login(msg)
                  public_msgbuffer = (done + msgbuffer)
                  line_bot_api.push_message(event_temp.source.user_id, TextSendMessage(public_msgbuffer))
             else:
                 print("錯誤:偵測不到itouch網址訊息類型")
                 line_bot_api.reply_message(event.reply_token, TextSendMessage("偵測不到itouch網址類型，請再試一次"))
         else:
             public_msgbuffer = ('請輸入正確的點名網址')
             line_bot_api.reply_message(event.reply_token, TextSendMessage(public_msgbuffer))
    elif 'https://' in msg or '.com' in msg :
        public_msgbuffer = (announce + '此非itouch網域')
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
                public_msgbuffer = (announce + '此非itouch網域')
                line_bot_api.reply_message(event.reply_token, TextSendMessage(public_msgbuffer))
    elif '變更權杖:' in msg:
        if opuuId == event.source.user_id :
           print("開始變更權杖")
           line_bot_api.reply_message(event.reply_token, TextSendMessage("已變更權杖"))
        else:
            print("變更權杖失敗，沒有權限")
            line_bot_api.reply_message(event.reply_token, TextSendMessage("沒有權限，無法變更權杖"))
    elif '要吃什麼' in msg or msg == '吃什麼':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(EAT[random.randint(0,len(EAT))]))
    elif '陪我' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("我不想跟你欸"))
    elif '在一次' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("再啦幹"))
    elif '我失戀了' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("反正你小王那麼多"))
    elif 'ok' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("ok"))
    elif '怪咖' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("對阿你很怪"))
    elif '都已讀' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("沒有 是你太邊緣"))
    elif 'peko' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("好油喔"))
    elif '女朋友' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("你沒有女朋友啦幹"))
    elif '閉嘴' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("你好兇喔"))
    elif '約' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("又要約又要約"))
    elif '三小' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("好兇"))
    elif '王顥' in msg and '單身' in msg:
        days = datetime.datetime.today()-datetime.datetime(2019,4,30,16)
        days = str(days)[0:4]
        sendbuffer = "小提醒:王顥已單身"+ days +"天"
        print(sendbuffer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(sendbuffer))
    elif '開啟' in msg :
        print("強制喚醒")

    elif '開始綁定' in msg :
        if (event.source.type == "group") :
            line_bot_api.push_message(event_temp.source.group_id, TextSendMessage("無法在群組進行綁定，請以私訊的形式進行此動作，謝謝"))
        elif(event.source.type == "user"):
            line_bot_api.push_message(event_temp.source.user_id, TextSendMessage("無法在群組進行綁定，請以私訊的形式進行此動作，謝謝"))
        else:
            print("")
    else:
        public_msgbuffer = (announce + '無法對這則訊息做出任何動作\n如要完成點名，請傳送該網址即可\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀')
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


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    msg_type = event.message.type
    print(msg_type)
    #print(event)
    if "sticker" in msg_type :
        packageid = event.message.package_id
        stickerid = event.message.sticker_id
        print(stickerid)
        print(packageid)
        if(event.source.group_id == groupId[0]):
            headers= {
            "Authorization": "Bearer " + grouptoken[0], 
            }
        elif(event.source.group_id == groupId[1]):
            headers= {
            "Authorization": "Bearer " + grouptoken[1], 
            }
            if STICKER_LIST.get(stickerid,"No") != "No":
                line_bot_api.reply_message(event.reply_token, TextSendMessage(STICKER_LIST.get(stickerid,"No")))#load sticker id ,if it doesn't found it'll return "No"
        elif(event.source.group_id == groupId[2]):
            headers= {
            "Authorization": "Bearer " + grouptoken[2], 
            }
            if STICKER_LIST.get(stickerid,"No") != "No":
                line_bot_api.reply_message(event.reply_token, TextSendMessage(STICKER_LIST.get(stickerid,"No")))
        else:
            print("有不知名的群組傳送了貼圖")
    return


def binding(uuid):
    print("")
    return 


def my_msg(msg_info):
    line_bot_api.push_message(opuuId, TextSendMessage(msg_info))
    print("進入管理員私訊:" + msg_info)
    return


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡淫加入\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n如要完成點名，請傳送該網址即可\n歡迎邀請其他人')
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
