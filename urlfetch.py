from selenium import webdriver
from bs4 import BeautifulSoup

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def url_login(msg):
  username = str('"11021340"')
  password = str('"Aa123456789"')
  url = str(msg)
  messageout = ""
  wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

  wd.get(url)
  wd.execute_script("document.getElementById('UserNm').value =" + username)
  wd.execute_script("document.getElementById('UserPasswd').value =" + password)
  wd.execute_script("document.getElementsByClassName('w3-button w3-block w3-green w3-section w3-padding')[0].click();")

  soup = BeautifulSoup(wd.page_source, 'html.parser')
  #print(soup.prettify())
  if (soup.find_all(stroke="#D06079") != []):#fail
      messageout =("點名失敗 好可憐" + wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text)

  elif (soup.find_all(stroke="#73af55") != []):#pass
      messageout =("點名成功 歐陽非常感謝你" + wd.find_element(By.XPATH,"/html/body/div[1]/div[3]/div").text)

  else:
      messageout = ("ERROR")
  message = TextSendMessage(messageout)
  return message