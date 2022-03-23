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
