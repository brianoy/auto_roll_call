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
        line_bot_api.reply_message(event.reply_token, TextSendMessage(EAT[random.randint(0,len(EAT)-1)]))
    elif '要吃啥' in msg or msg == '吃啥':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(EAT[random.randint(0,len(EAT)-1)]))
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
        
    elif '/' == msg:#fastreply
            if (event.source.type == "group") :
                quick_reply(event.source.group_id)
            if (event.source.type == "user") :
                user_quick_reply(event.source.user_id)

    elif '/' in msg:#all command
            command(msg,event)

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
        print("限制使用")
    elif (event.source.type == "user") :
        user_quick_reply(event.source.user_id)
    else:
        print("不做quick_reply")
    return 