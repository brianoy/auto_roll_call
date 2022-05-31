from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

def roll_call_fail(username,password):#全學年點名未到
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('user-agent=Mozilla/5.0')
  chrome_options.add_argument('ignore-certificate-errors')
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--example-flag")
  wd = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),options=chrome_options)
  url = "https://itouch.cycu.edu.tw/active_system/login/loginfailt.jsp?User_url=/active_system/query_data/board/s_history_course_board.jsp"
  wd.get(url)
  wd.execute_script("document.getElementById('UserNm').value =" + username)
  wd.execute_script("document.getElementById('UserPasswd').value =" + password)
  wd.execute_script("document.getElementsByClassName('button12')[0].click();")
  url = "https://itouch.cycu.edu.tw/active_system/query_data/board/s_history_course_board.jsp"
  wd.get(url)
  msg = "歷年修課清單\n"
  order = 2
  while(True):
    try:
      i=2#從表格的第二個開始偵測
      xpath = "/html/body/table/tbody/tr[" + str(order) + "]/td[7]/div/a"#點名按鍵 #如果是索引呢
      a = wd.find_element(by=By.XPATH, value=xpath).text
      wd.find_element(by=By.XPATH, value=xpath).click()#點進去頁面了
      #print(wd.current_url)
      while(True):
        try:
          xpath = "/html/body/table/tbody/tr[" + str(i) + "]/td[3]"
          a = str(wd.find_element(by=By.XPATH, value=xpath).text)
          xpath = "/html/body/table/tbody/tr[" + str(i) + "]/td[5]"
          b = str(wd.find_element(by=By.XPATH, value=xpath).text)
          if "未到" == a:#如果未到
            print("抓到未到的")

            xpath = "/html/body/h3[1]"#去抓未到的課程
            a = str((wd.find_element(by=By.XPATH, value=xpath).text).replace("課程名稱：","").replace("學年期",""))
            if len(a)>4:
              a = a[0:9] + "..."
            print(a)
            msg = msg + a

            xpath = "/html/body/table/tbody/tr[" + str(i) + "]/td[1]"#去抓未到的日期
            a = wd.find_element(by=By.XPATH, value=xpath).text
            print(a)
            msg = msg + a

            xpath = "/html/body/table/tbody/tr[" + str(i) + "]/td[2]"#去抓未到的節數
            a = wd.find_element(by=By.XPATH, value=xpath).text
            print(a)
            msg = msg + " " + a + "節"
            if b != "":#如果已准假就在後面標記
              msg = msg + "(已准假)\n"
            else:
              msg = msg + "\n"
          i += 1
          #沒有else
        except NoSuchElementException:
          #url = "https://itouch.cycu.edu.tw/active_system/query_data/board/s_history_course_board.jsp"
          #wd.get(url)
          wd.back()#變快46%
          break 
      order += 1
    except NoSuchElementException:
      #print("碰到沒有按鍵的")
      try:
        if "學年課程清單" in wd.find_element(by=By.XPATH, value="/html/body/table/tbody/tr[" + str(order) + "]/td").text:
          a = str(wd.find_element(by=By.XPATH, value="/html/body/table/tbody/tr[" + str(order) + "]/td").text).replace("清單","點名未到")
          msg = msg + "----------\n" + a + ":\n"
          order += 1
          print("學年課程清單")
        elif "課程" in wd.find_element(by=By.XPATH, value="/html/body/table/tbody/tr[" + str(order) + "]/td[7]/div").text:#如果div有東西，div/a沒有 那就是忽略 繼續
          order += 1
          print("碰到索引 繼續")
      except NoSuchElementException:
        print("結束")
        break#真的已經到表格最底部了 #跳脫while
  #print(msg)
  return msg