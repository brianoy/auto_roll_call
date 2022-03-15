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
import time
import os
import datetime
import random
import psycopg2
import discord
import json

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

DATABASE_URL = os.environ['DATABASE_URL']
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']
OPUUID = os.environ['LINE_OP_UUID']
changelog = "flexmsg"
client = discord.Client()
app = Flask(__name__)

EAT = (["全家","7-11","中原夜市","鍋燒意麵","肉羹","拉麵","炒飯","賣麵庄","雞腿便當","摩斯漢堡","麥當勞","烤肉飯","肯德基","石二鍋",
"五花馬","燒肉","咖哩飯","牛排","肉燥飯","SUKIYA","霸味薑母鴨","高雄黑輪","丼飯","薩利亞","mint","火雞肉飯","品田牧場","滷味","Mr.三明治",
"雞柳飯","肉骨茶麵","泡麵","水餃","煎餃","包子","炒麵","鐵板燒","披薩","悟饕","河粉","肉圓","黑宅拉麵","壽司","牛肉麵","鹹酥雞"])

STICKER_LIST = {'465400171':'ㄌㄩㄝ','465400158':'才不美','465400159':'Woooooooow','465400160':'不可以','465400161':'怎樣啦 輸贏啦','465400163':'假K孝濂給',
'465400165':'累屁','465400166':'聽話 讓我看看','465400169':'到底??????','465400172':'他在已讀你','465400173':'大概24小時後才會回你','13744852':'哼',
'349572675':'可憐哪','352138078':'吃屎阿','464946842':'對咩對咩','464946834':'ㄏㄏ','464946841':'亂講','435674449':'嘿嘿','435674452':'兇屁'}

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)# Channel Access Token
handler = WebhookHandler(LINE_CHANNEL_SECRET)# Channel Secret
discord_webhook = DISCORD_WEBHOOK

#userlist = ["11021340","11021339","11021346","11021331","11021338","11021337","11021325"]
#pwlist = ["aA123456789","Zz0123456789","Angel0610","dEEwYupDDCqh9","Daniel@123456","Wolf1017","Ray11021325"]
#namelist = ["歐陽立庭","蔡祐恩","洪晨旻","楊智涵","楊其宸","張子恆","江昱叡"]
#useridlist = []
grouptoken = ["4C0ZkJflAfexSpelBcoEYVobqbbSD0aGFNvpGAVcdUX","vUQ1xrf4cIp7kFlWifowMJf4XHdtUSHeXi1QeUKARa9","WCIuPhhETZysoA6qjdx59kblgzbc6gQuVscBKS91Fi5"]
groupId = ['Cc97a91380e09611261010e4c5c682711','C0041b628a8712ace35095f505520c0bd','Cdebd7e16f5b52db01c3efd20b12ddd35']

url = ""
msgbuffer = ""
public_msgbuffer = ""
success_login_status = 0
fail_login_status = 0

def get_all_user():#turn raw data into 4 argument lists 
    conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM all_info")#choose all the data of target 
    all_user_buffer_list = cursor.fetchall()#start fetch and become a list 
    global userlist
    global pwlist
    global namelist
    global useridlist
    userlist = []
    pwlist = []
    namelist = []
    useridlist = []
    for i in range(len(all_user_buffer_list)):
        userlist.append(all_user_buffer_list[i][3])
    print(userlist)

    for i in range(len(all_user_buffer_list)):
        pwlist.append(all_user_buffer_list[i][4])
    print(pwlist)

    for i in range(len(all_user_buffer_list)):
        namelist.append(all_user_buffer_list[i][1])
    print(namelist)

    for i in range(len(all_user_buffer_list)):
        useridlist.append(all_user_buffer_list[i][2])
    print(useridlist)
    count = cursor.rowcount
    print(count, "筆資料已進入伺服器")
    cursor.close()
    conn.close()


def url_login(msg):
  start_time = time.time()
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  url = str(msg)
  messageout = ""
  success_login_status = 0
  global fail_login_status
  fail_login_status = 0
  for i in range(0,len(userlist),1):
     usr =  userlist[i]
     pwd = pwlist[i]
     name = namelist[i]
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
         from selenium.webdriver.support import expected_conditions as EC
         password_wrong = EC.alert_is_present()(wd)#如果有錯誤訊息
         if password_wrong:
           failmsg = password_wrong.text
           password_wrong.accept()
           messageout = (messageout + "學號:" + usr + "\n🟥點名失敗❌\n錯誤訊息:密碼錯誤" + failmsg +'\n\n')#error login
           print("密碼錯誤\n------------------\n" + messageout)
           fail_login_status = fail_login_status +1
           wd.quit()
         else:
           soup = BeautifulSoup(wd.page_source, 'html.parser')
           #print(soup.prettify()) #html details
           if (soup.find_all(stroke="#D06079") != []):#fail
               messageout = (messageout + "\n🟥點名失敗❌，"+ name +"好可憐喔😱\n失敗訊息:" + wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text +'\n\n')
               print("點名失敗\n------------------\n" + messageout)
               fail_login_status = fail_login_status +1
           elif (soup.find_all(stroke="#73AF55") != []):#success
               detailmsg = wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text
               messageout = (messageout + "\n🟩點名成功✅，"+ name +"會非常感謝你\n成功訊息:" + detailmsg.replace('&#x6708;','月').replace('&#x65e5;','日').replace('&#x3a;',':').replace('<br>','\n')+'\n\n')
               print("點名成功\n------------------\n" + messageout)
               success_login_status = success_login_status +1
           else:
               messageout = (messageout + name + "\n🟥發生未知的錯誤❌，" + "學號:" + usr + " " + name + "點名失敗😱，趕快聯繫布萊恩，並自行手點" + '\n\n')#unknown failure
               print("點名失敗\n------------------\n" + messageout)
               fail_login_status = fail_login_status +1
  wd.quit()
  messageout = (messageout + '▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + "本次點名人數:" + str(len(userlist)) + "人\n" + "成功點名人數:" + str(success_login_status) + "人\n"+ "失敗點名人數:" + str(fail_login_status)+ "人")
  messageout = (messageout + '\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + "最近一次更新:" + os.environ['HEROKU_RELEASE_CREATED_AT'] + "GMT+0\n" + "版本:" + os.environ['HEROKU_RELEASE_VERSION']+ "\n此次點名耗費時間:" + str(round(time.time() - start_time)) +"秒" +"\n更新日誌:" + changelog)
  return messageout


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    body_ori = json.dumps()
    print(body_ori)
    print(type(body_ori))
    app.logger.info("Request body: " + body)
    print("訊息從line進入:\n" + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
        postback  = body_ori.events.type#or this 
        if postback == "postback":
            print("已收到回傳")
            print(body_ori.events.postback.data)
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
                  line_bot_api.push_message(event_temp.source.user_id, TextSendMessage(distinguish(public_msgbuffer)))
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
        if OPUUID == event.source.user_id :
           print("開始變更權杖")
           line_bot_api.reply_message(event.reply_token, TextSendMessage("已變更權杖"))
        else:
            print("變更權杖失敗，沒有權限")
            line_bot_api.reply_message(event.reply_token, TextSendMessage("沒有權限，無法變更權杖"))
    elif '要吃什麼' in msg or msg == '吃什麼':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(EAT[random.randint(0,len(EAT))]))
    elif '要吃啥' in msg or msg == '吃啥':
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
    elif '/開始綁定' in msg :
        if (event.source.type == "group") :
            line_bot_api.push_message(event_temp.source.group_id, TextSendMessage("無法在群組進行綁定，請以私訊機器人的形式進行此動作，謝謝"))
        elif(event.source.type == "user"):
            get_now_user_id = event_temp.source.user_id
            if (get_now_user_id in useridlist):
                print("使用者重複綁定")
                line_bot_api.push_message(event_temp.source.user_id, TextSendMessage("已有帳號密碼綁定於此line帳戶上，無法使用同一個Line帳戶綁定多支ilearning帳號\n若需要清除綁定，請輸入「/清除綁定」"))
            else:
                binding(get_now_user_id)
                line_bot_api.push_message(event_temp.source.user_id, TextSendMessage("你已成功綁定！"))
        else:
            print("")

    elif '/清除綁定' == msg :
        get_now_user_id = event_temp.source.user_id
        get_now_name = namelist[useridlist.index(get_now_user_id)]
        get_now_user = userlist[useridlist.index(get_now_user_id)]
        delete_on_database_via_uuid(get_now_user_id)
        respond = "已成功清除" + get_now_user + get_now_name + "的資料" + "，如需重新綁定，請輸入「/開始綁定」"
        print(respond)
        line_bot_api.push_message(event_temp.source.user_id, TextSendMessage(respond))

    elif '/重新整理' == msg :
        get_all_user()
        respond = "已重新抓取"
        print(respond)
        line_bot_api.push_message(event_temp.source.user_id, TextSendMessage(respond))

    elif '/我的uuid' == msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(event_temp.source.user_id))





    elif "我只是測試" == msg :#flex msg postback respond 
        with open("test.json") as path:
                FlexMessage = json.loads(path.read())
        flex_message = FlexSendMessage(
                           alt_text = '(請點擊聊天室已取得更多消息)' ,
                           contents = FlexMessage)
        line_bot_api.reply_message(event.reply_token, flex_message)





    elif '/我的帳號' == msg:
        get_now_user_id = event_temp.source.user_id
        if get_now_user_id in useridlist:#帳號存在
            get_now_name = namelist[useridlist.index(get_now_user_id)]
            get_now_user = userlist[useridlist.index(get_now_user_id)]
            with open("my_account.json") as path:
                FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id,"get_now_name" : get_now_name,"get_now_user" : get_now_user})
            flex_message = FlexSendMessage(
                           alt_text = '(請點擊聊天室已取得更多消息)' ,
                           contents = FlexMessage)
            line_bot_api.reply_message(event.reply_token, flex_message)
        else:#帳號不存在
            with open("account_not_exist.json") as path:
                FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
            flex_message = FlexSendMessage(
                           alt_text = '(請點擊聊天室已取得更多消息)' ,
                           contents = FlexMessage)
            line_bot_api.reply_message(event.reply_token, flex_message)


    elif '/變更密碼' in msg :
        get_now_user_id = event_temp.source.user_id
        if get_now_user_id in useridlist:#帳號存在
            change_password = msg.replace("/變更密碼 ","")
            with open("change_password.json") as path:
                    FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id , "change_password" : change_password})
            flex_message = FlexSendMessage(
                               alt_text = '(請點擊聊天室已取得更多消息)' ,
                               contents = FlexMessage)
            line_bot_api.reply_message(event.reply_token, flex_message)
        else:#帳號不存在
            with open("account_not_exist.json") as path:
                FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
            flex_message = FlexSendMessage(
                           alt_text = '(請點擊聊天室已取得更多消息)' ,
                           contents = FlexMessage)
            line_bot_api.reply_message(event.reply_token, flex_message)
        


    elif '/changepassword' in msg :
        get_now_user_id = event_temp.source.user_id
        if get_now_user_id in useridlist:#帳號存在
            change_password = msg.replace("/changepassword ","")
            change_password_via_uuid(change_password , get_now_user_id)
            with open("changed_password.json") as path:
                    FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
            flex_message = FlexSendMessage(
                               alt_text = '(請點擊聊天室已取得更多消息)' ,
                               contents = FlexMessage)
            line_bot_api.reply_message(event.reply_token, flex_message)

        else:#帳號不存在
            with open("account_not_exist.json") as path:
                    FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
            flex_message = FlexSendMessage(
                            alt_text = '(請點擊聊天室已取得更多消息)' ,
                            contents = FlexMessage)
            line_bot_api.reply_message(event.reply_token, flex_message)
        
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


def binding(uuid):#start binding the account
    print("")
    return 


def my_msg(msg_info):#send msg to me
    line_bot_api.push_message(OPUUID, TextSendMessage(msg_info))
    print("進入管理員私訊:" + msg_info)
    return

def delete_on_database_via_uuid(delete_uuid):
    conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    delete_uuid_pros = "'" + delete_uuid + "'"
    postgres_delete_query = "DELETE FROM all_info WHERE uuid = " + delete_uuid_pros
    cursor.execute(postgres_delete_query)
    conn.commit()
    cursor.close()
    conn.close()
    get_all_user()
    return

def change_password_via_uuid(change_password , uuid):
    conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    postgres_update_query = f"""UPDATE all_info set password = %s WHERE uuid = %s"""
    cursor.execute(postgres_update_query, (change_password, uuid))
    conn.commit()
    cursor.close()
    conn.close()
    get_all_user()
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
    get_all_user()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
