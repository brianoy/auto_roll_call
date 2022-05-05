#from selectors import EpollSelector
#heroku labs:enable log-runtime-metrics #開啟log
#heroku labs:disable log-runtime-metrics
#heroku restart
from flask import Flask, request, abort, render_template, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from lxml import etree #find with xpath
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests
import time
import os
import datetime #倒數 星期幾
import random
import psycopg2
import discord
import json
import ast #str to mapping
from to_do_list_variable import variable_separator, variable_block, variable_main_construct

mode = "stable"
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

DATABASE_URL = os.environ['DATABASE_URL']
if mode == "test":
    LINE_CHANNEL_ACCESS_TOKEN = os.environ['TEST_LINE_CHANNEL_ACCESS_TOKEN']
    LINE_CHANNEL_SECRET = os.environ['TEST_LINE_CHANNEL_SECRET']
else:
    LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
    LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']
OPUUID = os.environ['LINE_OP_UUID']
changelog = "mem leak、點名減速、點名訊息錯誤顯示"#還有成績指令沒寫完、簽到未開放的對列quene、未點名的紀錄
client = discord.Client()
app = Flask(__name__)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0')
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument("--disable-gpu")
wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

EAT = (["全家","7-11","中原夜市","鍋燒意麵","肉羹","拉麵","炒飯","賣麵庄","雞腿便當","摩斯漢堡","麥當勞","烤肉飯","肯德基","石二鍋",
"五花馬","燒肉","咖哩飯","牛排","肉燥飯","SUKIYA","霸味薑母鴨","高雄黑輪","丼飯","薩利亞","mint","火雞肉飯","品田牧場","滷味","Mr.三明治",
"雞柳飯","肉骨茶麵","泡麵","水餃","煎餃","包子","炒麵","鐵板燒","披薩","悟饕","河粉","肉圓","黑宅拉麵","壽司","牛肉麵","鹹酥雞","控肉便當",
"赤麵廠","早到晚到","大時鐘天香麵","豚骨麻辣燙","後站無名麵店","阿倫炒羊肉","炸螃蟹","烤肉","雞蛋糕"])

WHALE =(["\n\n\n\n\n·_______________·","\n\n\n\n\n@_______________@","\n\n\n\n\nX_______________X","\n\n\n\n\nO_______________O","\n\n\n\n\n^_______________^",
"\n\n\n\n\n*_______________*","\n\n\n⠀⠀⠀⠀⠀∞\n\n·_______________·","\n\n\n\n\n·_______________·"])

CHICKEN =(["➖➖➖➖\uD83D\uDFE5\n➖➖➖⬜️⬜️\n➖➖➖⬜️\uD83D\uDD33\uD83D\uDFE7\n⬜️➖➖⬜️⬜️\uD83D\uDFE5\n⬜️⬜️⬜️⬜️⬜️\n⬜️⬛️⬛️⬜️⬜️\n➖⬜️⬜️⬜️\n➖➖\uD83D\uDFE8",
"➖➖➖➖\uD83D\uDFE5\n➖➖➖\uD83D\uDFE7\uD83D\uDFE7\n➖➖➖\uD83D\uDFE7\uD83D\uDD33\uD83D\uDFE8\n\uD83D\uDFE6➖➖\uD83D\uDFE7\uD83D\uDFE7\uD83D\uDFE5\n\uD83D\uDFEB⬜️\uD83D\uDFEB\uD83D\uDFEB\uD83D\uDFEB\n\uD83D\uDFEB\uD83D\uDFE5\uD83D\uDFE5\uD83D\uDFEB\uD83D\uDFEB\n➖\uD83D\uDFEB\uD83D\uDFEB\uD83D\uDFEB\n➖➖\uD83D\uDFE8"])

STICKER_LIST = {'465400171':'ㄌㄩㄝ','465400158':'才不美','465400159':'Woooooooow','465400160':'不可以','465400161':'怎樣啦 輸贏啦','465400163':'假K孝濂給',
'465400165':'累屁','465400166':'聽話 讓我看看','465400169':'到底??????','465400172':'他在已讀你','465400173':'大概24小時後才會回你','13744852':'哼',
'349572675':'可憐哪','352138078':'吃屎阿','464946842':'對咩對咩','464946834':'ㄏㄏ','464946841':'亂講','435674449':'嘿嘿','435674452':'兇屁'}


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)# Channel Access Token
handler = WebhookHandler(LINE_CHANNEL_SECRET)# Channel Secret
discord_webhook = DISCORD_WEBHOOK
grouptoken = ["4C0ZkJflAfexSpelBcoEYVobqbbSD0aGFNvpGAVcdUX","vUQ1xrf4cIp7kFlWifowMJf4XHdtUSHeXi1QeUKARa9","WCIuPhhETZysoA6qjdx59kblgzbc6gQuVscBKS91Fi5"]
groupId = ['Cc97a91380e09611261010e4c5c682711','C0041b628a8712ace35095f505520c0bd','Cdebd7e16f5b52db01c3efd20b12ddd35']
recived = '已收到網址，正在點名中，請靜待約20~30秒，若看見此訊息後請盡量不要重複傳送相同的訊息，以免造成系統塞車'
done = '點名結束\n每次過程將會持續20~30秒\n(視點名人數及當前礙觸摸網路狀況而定)\n仍在測試中，不建議將此系統作為正式使用，在系統回覆點名狀態前建議不要離開本對話框，以免失效時來不及通知其他人手動點名\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' 
announce = '▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n由於line bot官方限制緣故，每個月對於機器人傳送訊息有一定的限額，如超過系統配額，此機器人將會失效\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n'
msgbuffer = ""
public_msgbuffer = ""
success_login_status = 0
fail_login_status = 0
global not_send_msg
not_send_msg = False


def get_all_user():#turn raw data into 4 argument lists 
    conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM all_info")#choose all the data of target 
    global all_user_buffer_list
    global userlist
    global pwlist
    global namelist
    global useridlist
    all_user_buffer_list = cursor.fetchall()#start fetch and become a list 
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

def get_now_all_user_status():#turn raw data into 4 argument lists 
    conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM all_info")#choose all the data of target 
    all_list = cursor.fetchall()#fetch 
    cursor.close()
    conn.close()
    return str(all_list)

@app.route("/time_quene")#post#未完成
def time_quene():
    print("加入對列")
    return 


@app.route("/chinese_ans", methods=["GET"])#國文的主網頁
def chinese_ans():
    my_msg("【進入chinese_ans的ip】" + request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))#傳給我手機點進來的Ip，HTTP_X_REAL_IP不起作用，會變成heroku內部ip
    return render_template('chinese_ans.html')

@app.route("/chinese_ques")#國文的副網頁
def chinese_ques():
    return render_template('chinese_ques.html')

@app.route('/chinese_test_files/title_on_01.gif')#國文的圖案
def title_on_01():
    return send_file("chinese_test_files/title_on_01.gif", mimetype='image/gif')

@app.route('/chinese_test_files/title_on_03.gif')
def title_on_03():
    return send_file("chinese_test_files/title_on_03.gif", mimetype='image/gif')

@app.route('/chinese_test_files/icon_wrong.gif')
def icon_wrong():
    return send_file("chinese_test_files/icon_wrong.gif", mimetype='image/gif')

def quene(url,time):#將未開始的點名加入對列#未完成
    print("已成功加入")


def url_login(msg,event,force):
    try:
        global not_send_msg
        not_send_msg = False
        now_unix_time = int(event.timestamp/1000)#強制將unix時間取整
        wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        start_time = time.time()
        url = str(msg).replace("&afterLogin=true","")
        messageout = ""
        success_login_status = 0
        global fail_login_status
        fail_login_status = 0
        wd.get(url)
        #time.sleep(1)
        soup_1 = BeautifulSoup(wd.page_source, 'html.parser')
        dom = etree.HTML(str(soup_1))
        not_open = "未開放 QRCODE簽到功能" in wd.page_source
        time_and_class = str(dom.xpath('/html/body/div/div[2]/p/text()[3]')[0])
        curriculum_name = str(dom.xpath('/html/body/div/div[2]/p/text()[4]')[0])
        soup_1.decompose()
        if not_open:
            fail_login_status = len(userlist)
            messageout = "🟥警告❌，點名並沒有開放，請稍後再試或自行手點，全數點名失敗\n"#反正也傳不出去
            not_send_msg = True
            with open("json/limited_class.json") as path:
                FlexMessage = json.loads(path.read() % {"msg_1" : "偵測到課程點名失敗，是否需要重新點名?" , "unix_time" : now_unix_time , "force_url_login" : url })
                flex_message = FlexSendMessage(
                                alt_text = '(請點擊聊天室已取得更多消息)' ,
                                contents = FlexMessage)
                print("傳出flexmsg")
                line_bot_api.reply_message(event.reply_token, flex_message)
                not_send_msg = False
            #break
        else:
            if (("英文" in curriculum_name or "化學實驗" in curriculum_name) and force != True):
                with open("json/limited_class.json") as path:
                    FlexMessage = json.loads(path.read() % {"msg_1" : "此課程不建議全體點名，確定要點名?" , "unix_time" : now_unix_time , "force_url_login" :  url })
                    flex_message = FlexSendMessage(
                                alt_text = '(請點擊聊天室已取得更多消息)' ,
                                contents = FlexMessage)
                print("傳出flexmsg不建議全體點名")
                line_bot_api.reply_message(event.reply_token, flex_message)
                not_send_msg = True
            else:#確認所有條件都適合點名
                #my_msg(url)
                for i in range(0,len(userlist),1):
                    wd.execute_script("window.open('');")#取一 我也不知道差在哪
                    #wd.switch_to.new_window('tab')
                    wd.switch_to.window(wd.window_handles[i+1])
                    wd.get(url)#打開所有對應數量的分頁並到網址
                    print("已打開第"+ str(i) + "個分頁")
                for i in range(0,len(userlist),1):
                    wd.switch_to.window(wd.window_handles[i+1])#先跑到對應的視窗
                    usr =  userlist[i]
                    pwd = pwlist[i]
                    name = namelist[i]
                    wd.execute_script('document.getElementById("UserNm").value ="' + usr + '"')
                    wd.execute_script('document.getElementById("UserPasswd").value ="' + pwd + '"')
                    wd.execute_script('document.getElementsByClassName("w3-button w3-block w3-green w3-section w3-padding")[0].click();')
                    print("已登入第"+ str(i) + "個分頁")
                for i in range(0,len(userlist),1):
                    usr =  userlist[i]#之後的訊息要顯示
                    pwd = pwlist[i]
                    name = namelist[i]
                    wd.switch_to.window(wd.window_handles[i+1])#先跑到對應的視窗
                    password_wrong = EC.alert_is_present()(wd)#如果有錯誤訊息#不太確定要先切換視窗再按確認還是反過來
                    if password_wrong:
                        failmsg = password_wrong.text
                        password_wrong.accept()
                        messageout = (messageout + "學號:" + usr + "\n🟥點名失敗❌\n錯誤訊息:密碼錯誤" + failmsg +'\n\n')#error login
                        print("密碼錯誤\n------------------\n" + messageout)
                        fail_login_status = fail_login_status +1
                    else:
                        soup_2 = BeautifulSoup(wd.page_source, 'html.parser')#疑似要把他強制轉為str並在尾巴decompose#疑似mem leak 不會吐error msg
                        #print(soup_2.prettify()) #html details
                        #print(str(soup_2.find_all(stroke="#D06079")))
                        #print(str(soup_2.find_all(stroke="#73AF55")))
                        if str(soup_2.find_all(stroke="#D06079")) != "[]":#fail #將清單強制轉為字串，若清單為空，輸出的字串為"[]"
                            messageout = (messageout + "\n🟥點名失敗❌，"+ name +"好可憐喔😱\n失敗訊息:" + wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text +'\n\n')
                            print("點名失敗\n------------------\n" + messageout)
                            fail_login_status = fail_login_status +1
                        elif str(soup_2.find_all(stroke="#73AF55")) != "[]":#success #將清單強制轉為字串，若清單為空，輸出的字串為"[]"
                            detailmsg = wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text
                            messageout = (messageout + "\n🟩點名成功✅，"+ name +"會非常感謝你\n成功訊息:" + detailmsg.replace('&#x6708;','月').replace('&#x65e5;','日').replace('&#x3a;',':').replace('<br>','\n')+'\n\n')
                            print("點名成功\n------------------\n" + messageout)
                            success_login_status = success_login_status +1
                        else:
                            messageout = (messageout + name + "\n🟥發生未知的錯誤❌，" + "學號:" + usr + " " + name + "點名失敗😱，趕快聯繫布萊恩，並自行手點" + '\n\n')#unknown failure
                            print("點名失敗\n------------------\n" + messageout)
                            fail_login_status = fail_login_status +1
                        soup_2.decompose()
        messageout = (messageout + '▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + "本次點名人數:" + str(len(userlist)) + "人\n" + "成功點名人數:" + str(success_login_status) + "人\n"+ "失敗點名人數:" + str(fail_login_status)+ "人\n" + str(time_and_class) + "\n" + str(curriculum_name))
        messageout = (messageout + '\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n' + "最近一次更新:" + os.environ['HEROKU_RELEASE_CREATED_AT'].replace("Z","").replace("T"," ") + "GMT+0\n" + "版本:" + os.environ['HEROKU_RELEASE_VERSION']+ "\n此次點名耗費時間:" + str(round(time.time() - start_time)+2) +"秒" +"\n更新日誌:" + changelog)
        wd.close()
    except IndexError:
        messageout = "🟥🟥FATAL ERROR🟥🟥\n可能是由ilearning網頁故障或是輸入錯誤的網址所引起\n請盡快手點和連繫我"
    except Exception:#記得有Bug的時候一定要把它撤下來 不然會吐不出錯誤訊息
        messageout = "🟥🟥UNKNOWN ERROR🟥🟥\n可能是由輸入錯誤的網址所引起，或是整體系統出錯，請聯絡我"
        print('不知道怎麼了，反正發生錯誤')
    return messageout

@handler.add(PostbackEvent)
def handle_postback(event):
    global public_msgbuffer
    postback_msg = event.postback.data
    get_now_user_id = event.source.user_id
    now_unix_time = int(event.timestamp/1000)#強制將unix時間取整
    time_end = now_unix_time
    print("現在時間:" + str(now_unix_time))

    if '/changepassword' in postback_msg :
        if get_now_user_id in useridlist:#帳號存在
            change_password = postback_msg.replace("/changepassword","").replace(" ","")
            change_password_via_uuid(change_password , get_now_user_id)
            with open("json/changed_password.json") as path:
                    FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
            flex_message = FlexSendMessage(
                               alt_text = '(請點擊聊天室已取得更多消息)' ,
                               contents = FlexMessage)
            print("傳出flexmsg")
            line_bot_api.reply_message(event.reply_token, flex_message)
    elif("/deleteall" in postback_msg):
        get_now_name = namelist[useridlist.index(get_now_user_id)]
        get_now_user = userlist[useridlist.index(get_now_user_id)]
        get_now_user_id = postback_msg.replace("/deleteall","").replace(" ","")
        delete_on_database_via_uuid(get_now_user_id)
        respond = "已成功清除" + get_now_user + get_now_name + "的資料" + "，如需重新綁定，請輸入「/開始綁定」"
        print(respond)
        my_msg(respond)
        line_bot_api.push_message(event.source.user_id, TextSendMessage(respond))
    elif("/force_url_login " in postback_msg):
        get_now_name = namelist[useridlist.index(get_now_user_id)]
        get_now_user = userlist[useridlist.index(get_now_user_id)]
        time_start = int((postback_msg.replace("/force_url_login ","").replace(" ",""))[0:10])
        url = postback_msg.replace("/force_url_login ","").replace(" ","").replace(str(time_start),"")
        print("標記時間:" + str(time_start))
        print("相扣時間:" + str(time_end-time_start))
        print("Raw data:" + postback_msg)
        print(url)
        if (event.source.type == "group") :
            if(event.source.group_id == groupId[0]):
                headers= {
                "Authorization": "Bearer " + grouptoken[0], 
                }
                if(time_end-time_start<=1800):
                    requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n觸發者:" + get_now_name + "\n" +recived })#翹課大魔王
                    msgbuffer = url_login(url,event,force = True)
                    public_msgbuffer = done + msgbuffer
                    payload = {'message': distinguish(public_msgbuffer) }
                    group_not_send_msg_func(not_send_msg,headers,payload)
                else:
                    requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n觸發者:" + get_now_name + "\n" + "按鈕時效已過期" })#翹課大魔王
                
            elif(event.source.group_id == groupId[1]):
                headers= {
                "Authorization": "Bearer " + grouptoken[1], 
                }
                if(time_end-time_start<=1800):
                    requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + recived })#秘密基地
                    msgbuffer = url_login(url,event,force = True)
                    public_msgbuffer = done + msgbuffer
                    payload = {'message': distinguish(public_msgbuffer) }
                    group_not_send_msg_func(not_send_msg,headers,payload)
                else:
                    requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n觸發者:" + get_now_name + "\n" + "按鈕時效已過期" })#秘密基地
            else:
                print("有不知名的群組")
        elif(event.source.type == "user") :
            if(time_end-time_start<=1800):
                person_not_send_msg_func(not_send_msg,event.source.user_id,TextSendMessage(recived))
                msgbuffer = url_login(url,event,force=True)
                public_msgbuffer = (done + msgbuffer)
                line_bot_api.push_message(event.source.user_id, TextSendMessage(distinguish(public_msgbuffer)))
            else:
                line_bot_api.push_message(event.source.user_id, TextSendMessage("按鈕時效已過期"))
        else:
            print("ERROR:invalid source type during force login")

    elif("/delete_to_do_list " in postback_msg):
        conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        name = "'" + postback_msg.replace("/delete_to_do_list ","") + "'"
        postgres_delete_query = "DELETE FROM shoplist WHERE name = " + name
        cursor.execute(postgres_delete_query)
        conn.commit()
        cursor.close()
        conn.close()
        to_do_list_show(event)

    else:
        print("ERROR:invalid postback event")


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
    if "ERROR" in msgbuffer:
        msgbuffer = msgbuffer.replace(done,"")#將多產生的點名訊息再刪掉
    else:
        if (fail_login_status > 0):
            msgbuffer = "🟥\n" + msgbuffer
        else:
            msgbuffer = "🟩\n" + msgbuffer
    return msgbuffer


def get_curriculum_pros(get_now_user,get_now_pwd):
    curriculum_list = []
    classroom_list = []
    url="https://itouch.cycu.edu.tw/active_system/login/loginfailt.jsp?User_url=/active_system/quary/s_query_course_list.jsp"
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #wd = webdriver.Chrome('chromedriver',options=chrome_options)
    wd.get(url)
    wd.execute_script('document.getElementById("UserNm").value ="' + get_now_user + '"')
    wd.execute_script('document.getElementById("UserPasswd").value ="' + get_now_pwd + '"')
    xpath = "/html/body/div[3]/form/table/tbody/tr[1]/td/table/tbody/tr[4]/td/div[1]/input"
    wd.find_element(by=By.XPATH, value=xpath).click()
    wd.get("https://itouch.cycu.edu.tw/active_system/quary/s_query_course_list.jsp");
    soup = BeautifulSoup(wd.page_source, 'html.parser')
    dom = etree.HTML(str(soup))
    for j in range(3,10,1):#星期
        for i in range(3,32,2):#一天14節課
            a = dom.xpath('/html/body/table[1]/tbody/tr['+ str(i) + ']/td[' + str(j) + ']')[0].text#課程名
            if a != None:#有課
                try:
                    b = dom.xpath('/html/body/table[1]/tbody/tr['+ str(i) +']/td[' + str(j) +']/font')[0].text#如果有課程，課程的教室
                except IndexError: #有課程但是沒教室
                    print("") 
                    b = ""
            else:#沒課
                b = ""
                a = ""
            classroom_list.append(str(b))
            curriculum_list.append(str(a))
    wd.quit
    return curriculum_list,classroom_list


def curriculum(event):
    get_now_user_id = event.source.user_id
    if get_now_user_id in useridlist:#帳號存在
        get_now_user = userlist[useridlist.index(get_now_user_id)]
        get_now_pwd = pwlist[useridlist.index(get_now_user_id)]
        curriculum_list,classroom_list = get_curriculum_pros(get_now_user,get_now_pwd)
        with open("json/curriculum.json") as path:
            FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
            flex_message = FlexSendMessage(
                alt_text = '(請點擊聊天室已取得更多消息)' ,
                contents = FlexMessage)
            print("傳出flexmsg")
            line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("你尚未綁定帳號"))
    return
        

def today_curriculum(event):
    get_now_user_id = event.source.user_id
    day_list_num = (datetime.datetime.today().isoweekday()*14)-14
    if get_now_user_id in useridlist:#帳號存在
        get_now_user = userlist[useridlist.index(get_now_user_id)]
        get_now_pwd = pwlist[useridlist.index(get_now_user_id)]
        curriculum_list,classroom_list = get_curriculum_pros(get_now_user,get_now_pwd)
        print(classroom_list)
        print(curriculum_list)
        switcher = { "1": '"星期一"', "2": '"星期二"', "3": '"星期三"', "4": '"星期四"', "5": '"星期五"', "6": '"星期六"', "7": '"星期日"'}
        substitute = '"day" : ' + switcher.get(str(datetime.datetime.today().isoweekday()))
        for k in range(day_list_num , day_list_num+15 , 1):
            substitute = (substitute + ',' + '"curriculum_' + str(k - day_list_num + 1) + '" : "' + curriculum_list[k] + ' ",' + '"place_' + str(k - day_list_num + 1) + '" : "' +classroom_list[k] + ' "') 
        substitute = "{" + substitute + "}"
        #print(substitute)
        #print(type(substitute))
        substitute = ast.literal_eval(substitute)
        #print(substitute)
        #print(type(substitute))
        with open("json/today_curriculum.json") as path:
            FlexMessage = json.loads(path.read() % substitute)
            flex_message = FlexSendMessage(
                alt_text = '(請點擊聊天室已取得更多消息)' ,
                contents = FlexMessage)
            print("傳出flexmsg")
            line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("你尚未綁定帳號"))
    return

def group_not_send_msg_func(not_send_msg,headers,payload):
    if not_send_msg == True:
        print()
    else:
        requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return

def person_not_send_msg_func(not_send_msg,user_id,payload):
    if not_send_msg == True:
        print()
    else:
        line_bot_api.push_message(user_id, payload)
    return

 #warning! reply token would expired after send msg about 30seconds. use push msg! 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) :
    public_msgbuffer = ""
    msg = event.message.text
    msg_type = event.message.type
    #now_unix_time = int(event.timestamp/1000)#強制將unix時間取整
    print(msg_type)
    event_temp = event
    if 'itouch.cycu.edu.tw' in msg and '/force_url_login' not in msg:
         if 'learning_activity' in msg :
             if (event.source.type == "group") :
                 if(event.source.group_id == groupId[0]):
                      headers= {
                      "Authorization": "Bearer " + grouptoken[0], 
                      }
                      requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + recived })#翹課大魔王
                      msgbuffer = url_login(msg,event,force=False)
                      public_msgbuffer = done + msgbuffer
                      payload = {'message': distinguish(public_msgbuffer) }
                      group_not_send_msg_func(not_send_msg,headers,payload)
                 elif(event.source.group_id == groupId[1]):
                      headers= {
                      "Authorization": "Bearer " + grouptoken[1], 
                      }
                      requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + recived })#秘密基地
                      msgbuffer = url_login(msg,event,force=False)
                      public_msgbuffer = done + msgbuffer
                      payload = {'message': distinguish(public_msgbuffer) }
                      group_not_send_msg_func(not_send_msg,headers,payload)
                 else:
                      line_bot_api.reply_message(event_temp.reply_token, TextSendMessage(recived))
                      msgbuffer = url_login(msg,event,force=False)
                      public_msgbuffer = done + msgbuffer
                      payload = {'message': distinguish(public_msgbuffer) }
                      print("有不知名的群組")
                      line_bot_api.push_message(event_temp.source.group_id, TextSendMessage(distinguish(public_msgbuffer)))#除了以上兩個群組
             elif(event.source.type == "user") :
                  line_bot_api.push_message(event_temp.source.user_id, TextSendMessage(recived))
                  msgbuffer = url_login(msg,event,force=False)
                  public_msgbuffer = (done + msgbuffer)
                  person_not_send_msg_func(not_send_msg,event_temp.source.user_id,TextSendMessage(distinguish(public_msgbuffer)))
             else:
                 print("錯誤:偵測不到itouch網址訊息類型")
                 line_bot_api.reply_message(event.reply_token, TextSendMessage("偵測不到itouch網址類型，請再試一次"))
         else:
             public_msgbuffer = ('請輸入正確的點名網址')
             line_bot_api.reply_message(event.reply_token, TextSendMessage(public_msgbuffer))

    elif '/' in msg and msg[0] == "/":#all command
        command(msg,event)

    elif 'https://' in msg or '.com' in msg :
        public_msgbuffer = (announce + '此非itouch網域')
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
                requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n好像有人傳了網址還是怎麼樣的" })#秘密基地
            elif(event.source.group_id == groupId[2]):
                headers= {
                "Authorization": "Bearer " + grouptoken[2], 
                }
                requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n好像有人傳了網址還是怎麼樣的" })#小歐陽機器人
            else:
                public_msgbuffer = (announce + '此非itouch網域')
                line_bot_api.reply_message(event.reply_token, TextSendMessage(public_msgbuffer))
    elif '要吃什麼' in msg or msg == '吃什麼':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(EAT[random.randint(0,len(EAT)-1)]))
    elif '要吃啥' in msg or msg == '吃啥':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(EAT[random.randint(0,len(EAT)-1)]))
    elif '陪我' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("我不想跟你欸"))
    elif '在一次' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("再啦幹"))
    elif '我失戀了' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("反正你小王那麼多"))
    elif '暈了' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("寶"))
    elif 'ok' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("ok"))
    elif '有沒有人' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("沒有"))
    elif '大鯨魚' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(WHALE[random.randint(0,len(WHALE)-1)]))
    elif '雞' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(CHICKEN[random.randint(0,len(CHICKEN)-1)]))
    elif '怪咖' in msg :
        line_bot_api.reply_message(event.reply_token, TextSendMessage("對阿你很怪"))
    elif '笑死' in msg or '習近平' in msg  or '習大大' in msg or '習維尼' in msg or '維尼' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("哈哈很好笑\n⣿⣿⣿⠟⠋⠄⠄⠄⠄⠄⠄⠄⢁⠈⢻⢿⣿⣿⣿⣿⣿\n⣿⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⡀⠭⢿⣿⣿\n⣿⣿⡟⠄⢀⣾⣿⣿⣿⣷⣶⣿⣷⣶⣶⡆⠄⠄⠄⣿⣿\n⣿⣿⡇⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠄⠄⢸⣿⣿\n⣿⣿⣇⣼⣿⣿⠿⠶⠙⣿⡟⠡⣴⣿⣽⣿⣧⠄⢸⣿⣿\n⣿⣿⣿⣾⣿⣿⣟⣭⣾⣿⣷⣶⣶⣴⣶⣿⣿⢄⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⡟⣩⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣹⡋⠘⠷⣦⣀⣠⡶⠁⠈⠁⠄⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣍⠃⣴⣶⡔⠒⠄⣠⢀⠄⠄⠄⡨⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣦⡘⠿⣷⣿⠿⠟⠃⠄⠄⣠⡇⠈⠻⣿⣿\n⣿⣿⡿⠟⠋⢁⣷⣠⠄⠄⠄⠄⣀⣠⣾⡟⠄⠄⠄⠄⠉\n⠋⠁⠄⠄⠄⢸⣿⣿⡯⢓⣴⣾⣿⣿⡟⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⣿⡟⣷⠄⠹⣿⣿⣿⡿⠁⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⣿⣿⠃⣦⣄⣿⣿⣿⠇⠄⠄⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⢸⣿⠗⢈⡶⣷⣿⣿⡏⠄⠄⠄⠄⠄⠄⠄⠄⠄\n去新疆"))
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
    elif '三小' in msg or "幹你娘"in msg or "幹妳娘"in msg or "幹您娘"in msg or "耖機掰"in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("好兇"))
    elif '王顥' in msg and '單身' in msg:
        days = datetime.datetime.today()-datetime.datetime(2019,4,30,16)
        days = str(days)[0:4]
        sendbuffer = "小提醒:王顥已單身"+ days +"天"
        print(sendbuffer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(sendbuffer))
        
    elif '/' == msg:#fastreply
            if (event.source.type == "group") :
                quick_reply(event.source.group_id)
            if (event.source.type == "user") :
                user_quick_reply(event.source.user_id)

    elif '要買' in msg :
        if(event.source.type == "group" and event.source.group_id == groupId[1]):
            to_do_list_insert(msg,event)
            to_do_list_show(event)

    elif '查看清單' in msg :
        if(event.source.type == "group" and event.source.group_id == groupId[1]):
            to_do_list_show(event)

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
    
    if (event.source.type == "group") :
        #if (event.source.group_id == groupId[0]) :
            #quick_reply(groupId[0])
        #elif (event.source.group_id == groupId[1]) :
            #quick_reply(groupId[1])    
        print("限制使用quick reply")
    elif (event.source.type == "user") :
        user_quick_reply(event.source.user_id)
    else:
        print("不做quick_reply")
    return 


def command(msg,event):
    if '/重新抓取資料庫' == msg :
        get_all_user()
        respond = "已重新抓取"
        print(respond)
        not_send_msg = False
        person_not_send_msg_func(not_send_msg,event.source.user_id,TextSendMessage(respond))

    elif '/我的uuid' == msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(event.source.user_id))

    elif '/資料庫' == msg and event.source.user_id == OPUUID :
        respond = ""
        for x in range(0,len(all_user_buffer_list),1):
            respond = respond + str("\n")
            for y in range(0,len(all_user_buffer_list[x]),1):
                respond = respond + str(all_user_buffer_list[x][y])
                respond = respond + str("\n")
        my_msg(str(respond))

    elif '/請假紀錄' == msg or '/請假' == msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(day_off(event)))

    elif '/你今天被實驗助教搞了嗎' == msg or '/實驗課成績' == msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(experiment_course_score(event)))

    elif '/我的帳號' == msg:
        get_now_user_id = event.source.user_id
        if get_now_user_id in useridlist:#帳號存在
            get_now_name = namelist[useridlist.index(get_now_user_id)]
            get_now_user = userlist[useridlist.index(get_now_user_id)]
            with open("json/my_account.json") as path:
                FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id,"get_now_name" : get_now_name,"get_now_user" : get_now_user})
            flex_message = FlexSendMessage(
                           alt_text = '(請點擊聊天室已取得更多消息)' ,
                           contents = FlexMessage)
            print("傳出flexmsg")
            line_bot_api.reply_message(event.reply_token, flex_message)
        else:#帳號不存在
            with open("json/account_not_exist.json") as path:
                FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
            flex_message = FlexSendMessage(
                           alt_text = '(請點擊聊天室已取得更多消息)' ,
                           contents = FlexMessage)
            print("傳出flexmsg")
            line_bot_api.reply_message(event.reply_token, flex_message)

    elif '/help' == msg or '/幫助' == msg or '/開始綁定帳號' == msg or '/我要綁定帳號' == msg or '/我想要綁定帳號' == msg or '指令列表' == msg or '/指令' == msg or '/指令列表' == msg: 
        with open("json/help.json") as path:
                FlexMessage = json.loads(path.read())
        flex_message = FlexSendMessage(
                       alt_text = '(請點擊聊天室已取得更多消息)' ,
                       contents = FlexMessage)
        print("傳出flexmsg")
        line_bot_api.reply_message(event.reply_token, flex_message)
    
    elif("/force_url_login" in msg):#以明語訊息強制把訊息force_login
        not_send_msg = False #要傳訊息 在flexmsg彈出時才會變為true
        get_now_user_id = event.source.user_id
        get_now_name = namelist[useridlist.index(get_now_user_id)]
        get_now_user = userlist[useridlist.index(get_now_user_id)]
        url = msg.replace("/force_url_login ","").replace("/force_url_login","").replace(" ","")
        print("明文訊息強制點名:")
        print(url)
        if (event.source.type == "group") :
            if(event.source.group_id == groupId[0]):
                headers= {
                "Authorization": "Bearer " + grouptoken[0], 
                }
                requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + recived })#翹課大魔王
                msgbuffer = url_login(url,event,force = True)
                public_msgbuffer = done + msgbuffer
                payload = {'message': distinguish(public_msgbuffer) }
                group_not_send_msg_func(not_send_msg,headers,payload)
            elif(event.source.group_id == groupId[1]):
                headers= {
                "Authorization": "Bearer " + grouptoken[1], 
                }
                requests.post("https://notify-api.line.me/api/notify", headers = headers, params = {'message': "\n" + recived })#秘密基地
                msgbuffer = url_login(url,event,force = True)
                public_msgbuffer = done + msgbuffer
                payload = {'message': distinguish(public_msgbuffer) }
                group_not_send_msg_func(not_send_msg,headers,payload)
            else:
                print("有不知名的群組")
        elif(event.source.type == "user") :
            person_not_send_msg_func(not_send_msg,event.source.user_id,TextSendMessage(recived))
            msgbuffer = url_login(url,event,force=True)
            public_msgbuffer = (done + msgbuffer)
            line_bot_api.push_message(event.source.user_id, TextSendMessage(distinguish(public_msgbuffer)))
        else:
            print("ERROR:invalid source type during force login")


    else:
        if (event.source.type == "user") :
            limited_command(msg,event)
        else:
            line_bot_api.push_message(event.source.group_id, TextSendMessage("無法在群組使用此指令，請以私訊機器人的形式進行，謝謝"))
        print("指令不存在此區")
    return


def quick_reply(id):
    quick_reply = TextSendMessage(
    text="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="今天要吃什麼",text="今天要吃什麼")
                ),
            QuickReplyButton(
                action=MessageAction(label="指令列表",text="/help")
                ),
            QuickReplyButton(
                action=MessageAction(label="我的帳號",text="/我的帳號")
                ),
            QuickReplyButton(
                action=MessageAction(label="我的uuid",text="/我的uuid")
                ),
            QuickReplyButton(
                action=MessageAction(label="今日課表",text="/今日課表")
                ),
            QuickReplyButton(
                action=MessageAction(label="請假紀錄",text="/請假紀錄")
                ),
            QuickReplyButton(
                action=MessageAction(label="你今天被實驗助教搞了嗎",text="/你今天被實驗助教搞了嗎")
                )
        ]
    )
    )
    line_bot_api.push_message(id, quick_reply)
    return

def user_quick_reply(id):
    quick_reply = TextSendMessage(
    text="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="今天要吃什麼",text="今天要吃什麼")
                ),
            QuickReplyButton(
                action=MessageAction(label="指令列表",text="/help")
                ),
            QuickReplyButton(
                action=MessageAction(label="我的帳號",text="/我的帳號")
                ),
            QuickReplyButton(
                action=MessageAction(label="我的uuid",text="/我的uuid")
                ),
            QuickReplyButton(
                action=MessageAction(label="重新抓取資料庫",text="/重新抓取資料庫")
                ),
            QuickReplyButton(
                action=MessageAction(label="清除綁定",text="/清除綁定")
                ),
            QuickReplyButton(
                action=MessageAction(label="今日課表",text="/今日課表")
                ),
            QuickReplyButton(
                action=MessageAction(label="請假紀錄",text="/請假紀錄")
                ),
            QuickReplyButton(
                action=MessageAction(label="你今天被實驗助教搞了嗎",text="/你今天被實驗助教搞了嗎")
                )#還有成績指令沒寫完
        ]
    )
    )
    line_bot_api.push_message(id, quick_reply)
    return

def limited_command(msg,event):
    if '/變更密碼' in msg or '/更改密碼' in msg:
        get_now_user_id = event.source.user_id
        if get_now_user_id in useridlist:#帳號存在
            change_password = msg.replace("/變更密碼","").replace(" ","").replace("/更改密碼","")
            if change_password == "":
                line_bot_api.reply_message(event.reply_token, TextSendMessage("警告 密碼不能為空"))  
            else:
                with open("json/change_password.json") as path:
                    FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id , "change_password" : change_password})
                flex_message = FlexSendMessage(
                            alt_text = '(請點擊聊天室已取得更多消息)' ,
                            contents = FlexMessage)
                print("傳出flexmsg")
                line_bot_api.reply_message(event.reply_token, flex_message)
        else:#帳號不存在
            with open("json/account_not_exist.json") as path:
                FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
            flex_message = FlexSendMessage(
                           alt_text = '(請點擊聊天室已取得更多消息)' ,
                           contents = FlexMessage)
            print("傳出flexmsg")
            line_bot_api.reply_message(event.reply_token, flex_message)

    elif '/整日課表' == msg or '/我的課表' == msg :
        curriculum(event)

    elif '/今日課表' == msg or '/今天的課表' == msg :
        today_curriculum(event)

    elif '/清除綁定' == msg or '/清楚綁定' == msg:
        get_now_user_id = event.source.user_id
        #get_now_name = namelist[useridlist.index(get_now_user_id)]
        #get_now_user = userlist[useridlist.index(get_now_user_id)]
        with open("json/comfirmed_delete.json") as path:
                FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id})
        flex_message = FlexSendMessage(
                        alt_text = '(請點擊聊天室已取得更多消息)' ,
                        contents = FlexMessage)
        print("傳出flexmsg")
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif '/開始綁定' in msg :
        get_now_user_id = event.source.user_id
        if (get_now_user_id in useridlist):
            print("使用者重複綁定")
            line_bot_api.push_message(event.source.user_id, TextSendMessage("已有帳號密碼綁定於此line帳戶上，無法使用同一個Line帳戶綁定多支ilearning帳號\n若需要清除綁定，請輸入「/清除綁定」"))
        else:
            try:
                split_msg = []
                split_msg = msg.split(' ')
                set_now_name = split_msg[1]
                set_now_password = split_msg[3]
                try:
                    set_now_account = int(split_msg[2])
                    register(set_now_name, get_now_user_id, set_now_account, set_now_password)
                    with open("json/create_account.json") as path:
                        FlexMessage = json.loads(path.read() % {"get_now_user_id" : get_now_user_id,"get_now_name" : set_now_name,"get_now_user" : set_now_account,"get_now_password" : set_now_password})
                    flex_message = FlexSendMessage(
                                    alt_text = '(請點擊聊天室已取得更多消息)' ,
                                    contents = FlexMessage)
                    print("傳出flexmsg")
                    line_bot_api.reply_message(event.reply_token, flex_message)
                except ValueError:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("帳號請輸入學號(純數字)"))
                except IndexError:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("格式輸入錯誤，請輸入「/開始綁定 [你的名字] [你的學號] [你的密碼]」(請注意空格)\n如果還是不會使用，就連絡我吧"))
                except Exception:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage("未知的錯誤，請連絡我吧"))
            except IndexError:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("你應該是輸入了錯誤的指令或是用錯了指令\n請輸入/help取得更詳細的使用說明或是聯絡我"))
            except Exception:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("未知的錯誤，請連絡我吧"))
    else:
        if (event.source.user_id == OPUUID):
            op_command(msg,event)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("沒有這個指令或是你沒有這個權限"))

def op_command(msg,event):

    if ("/名單" in msg):#名單au/620 
       my_msg(get_now_all_user_status().replace("),","),\n\n"))

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

def my_msg(msg_info):#send msg to me
    line_bot_api.push_message(OPUUID, TextSendMessage("【admin】" + msg_info))
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

def register(name,uuid,account,password):
    conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    insert_arguments = (name, uuid, account, password)
    table_columns = '(name, uuid, account, password)'
    postgres_insert_query = f"""INSERT INTO all_info {table_columns} VALUES (%s,%s,%s,%s)"""
    cursor.execute(postgres_insert_query, insert_arguments)
    conn.commit()
    cursor.close()
    conn.close()
    get_all_user()
    return

def to_do_list_insert(msg,event):
    now_time = str(datetime.datetime.fromtimestamp(time.time()+28800).strftime('%Y-%m-%d %H:%M:%S'))#time.time是秒記數)
    conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    records = (msg.replace("要",""), now_time)
    table_columns = '(name, date)'
    postgres_insert_query = f"""INSERT INTO shoplist {table_columns} VALUES (%s,%s)"""
    cursor.execute(postgres_insert_query, records)
    conn.commit()
    cursor.close()
    conn.close()
    return

def to_do_list_show(event):
    conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    postgres_select_query = "SELECT * FROM shoplist"
    cursor.execute(postgres_select_query)
    to_do_list = cursor.fetchall()
    content = ""
    for i in range(0,len(to_do_list),1):
        name = str(to_do_list[i][1])
        date = str(to_do_list[i][2])
        delete = "/delete_to_do_list " + name
        order = str(i+1) + "."
        #print(name)
        #print(date)
        block = variable_block().replace("name",name).replace("date",date).replace("order",order).replace("delete_data",delete)
        if content != "":
            content = content + "," + variable_separator() + "," + block
        else:
            content = block
    #print(content)
    content = variable_main_construct().replace("main_construct", content)
    FlexMessage = json.loads(content, strict=False)
    flex_message = FlexSendMessage(
        alt_text = '(請點擊聊天室已取得更多消息)',
        contents = FlexMessage)
    print("傳出flexmsg")
    line_bot_api.reply_message(event.reply_token, flex_message)
    return

def day_off(event):
    get_now_user_id = event.source.user_id
    if get_now_user_id in useridlist:#帳號存在#密碼暫時被視為正確
        get_now_user = userlist[useridlist.index(get_now_user_id)]
        get_now_pwd = pwlist[useridlist.index(get_now_user_id)]
        wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        wd.get("https://itouch.cycu.edu.tw/active_project/cycu2100h_18/case_09/login.jsp")
        wd.execute_script('document.getElementById("UserNm").value ="' + get_now_user + '"')
        wd.execute_script('document.getElementById("UserPasswd").value ="' + get_now_pwd + '"')
        wd.execute_script('document.getElementsByClassName("button12")[0].click();')
        wd.get("https://itouch.cycu.edu.tw/active_project/cycu2100h_18/case_09/inquiry.jsp")
        name = wd.find_element(By.XPATH,"/html/body/div[1]/div[2]/table[1]/tbody/tr/td[2]/span").text
        i = 1
        msg = ""
        while True:
            try:#find element有放進cache嗎?還是浪費效能抓取?
                #需要改成etree嗎
                start_date = wd.find_element(By.XPATH,"/html/body/div[1]/div[2]/table[2]/tbody/tr["+str(1+i)+"]/td[3]").text
                end_date = wd.find_element(By.XPATH,"/html/body/div[1]/div[2]/table[2]/tbody/tr["+str(1+i)+"]/td[4]").text
                reason = wd.find_element(By.XPATH,"/html/body/div[1]/div[2]/table[2]/tbody/tr["+str(1+i)+"]/td[7]").text
                permit = wd.find_element(By.XPATH,"/html/body/div[1]/div[2]/table[2]/tbody/tr["+str(1+i)+"]/td[8]").text
                msg = "\n\n" + start_date + "~" + end_date + " : " + reason + "(已審核 " + permit + ")" + msg
                i+=1
            except NoSuchElementException:
                if msg == "":
                    msg = name + "的請假紀錄:\n無"
                else:
                    msg = name + "的請假紀錄:" + msg
                break
    else:
        print("有人想要查詢但是帳號不存在")
    wd.close()
    return msg

def experiment_course_score(event):
    get_now_user_id = event.source.user_id
    if get_now_user_id in useridlist:#帳號存在#密碼暫時被視為正確
        get_now_user = userlist[useridlist.index(get_now_user_id)]
        get_now_pwd = pwlist[useridlist.index(get_now_user_id)]
        get_now_name = namelist[useridlist.index(get_now_user_id)]
        wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        wd.get("https://i-learning.cycu.edu.tw/index.php")
        wd.execute_script('document.getElementById("username").value ="' + get_now_user + '"')
        wd.execute_script('document.getElementById("password").value ="' + get_now_pwd + '"')
        wd.execute_script('document.getElementsByClassName("submitBtn")[0].click()')
        #已登入完畢 跳轉進入我的課程
        wd.execute_script('parent.chgCourse("10127138", 1, 1)')#決定課程，實驗課課程代碼10127138
        wd.get("https://i-learning.cycu.edu.tw/learn/grade/grade_list.php")
        i = 1
        msg = ""
        while True:
            try:
                score_name = wd.find_element(By.XPATH,"/html/body/div/div[2]/div/div[3]/div/table/tbody/tr["+str(i)+"]/td[1]/div").text
                score_value = wd.find_element(By.XPATH,"/html/body/div/div[2]/div/div[3]/div/table/tbody/tr["+str(i)+"]/td[4]/div").text
                msg = "\n\n" + score_name + " : " + score_value + msg
                i+=1
            except NoSuchElementException:
                if msg == "":
                    msg = get_now_name + "的實驗課成績:\n無"
                else:
                    msg = get_now_name + "的實驗課成績:" + msg.replace("  :  \n\n","")#把最後一排空白的表格取代掉
                break
    else:
        print("有人想要查詢但是帳號不存在")
    wd.close()
    return msg
        
        
@handler.add(MemberJoinedEvent)
def welcome(event):
    #uid = event.joined.members[0].user_id
    #gid = event.source.group_id
    #profile = line_bot_api.get_group_member_profile(gid, uid)
    #name = profile.display_name
    quick_reply = TextSendMessage(
    text ="歡淫加入\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n如要完成點名，請傳送該網址即可\n歡迎邀請其他人\n如需綁定請參考快速回覆的指令按鈕或是直接輸入「/help」",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="指令列表",text="/help")
                )
        ]
    )
    )
    line_bot_api.reply_message(event.reply_token, quick_reply)

if __name__ == "__main__":
    get_all_user()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
