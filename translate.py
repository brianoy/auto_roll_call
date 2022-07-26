import os
import openai
import json
import requests
OPENAI_APIKEY = os.environ['openai_apikey']
TRANSLATOR_APIKEY = os.environ['translator_apikey']
openai.api_key = OPENAI_APIKEY
def AI(question):  
    def translate(language, msg_from):
        url = "https://microsoft-translator-text.p.rapidapi.com/translate"
        querystring = {"to[0]":language,"api-version":"3.0","profanityAction":"NoAction","textType":"plain"}
        payload = [{"Text": msg_from}]
        headers = {
  	        "content-type": "application/json",
  	        "X-RapidAPI-Key": TRANSLATOR_APIKEY,
  	        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
        }
        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
        msg = json.loads(response.text)
        return msg[0]["translations"][0]["text"]
    en_question = translate("en", question)
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=en_question,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    reply = str(response)
    reply = json.loads(reply)
    msg = reply["choices"][0]["text"]
    tw_respond = translate("zh-TW", msg)
    return tw_respond.replace("，","\n")