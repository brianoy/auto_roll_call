# My auto roll call line-bot
單純給我的line-bot留下紀錄

## Requirements
1. Python environment

2. Create A heroku app **(https<area>://dashboard.heroku.com/apps)**

3. A line bot channel in line developer console **(https<area>://developers.line.biz/console/)**

4. Enable the webhook function in your line bot channel console **(https<area>://manager.line.biz/account/[your_linebot_id]/setting)**
  
5. Link the webhook in the line bot channel console to **(https<area>://[your_app_name].herokuapp.com/callback)**


## Add the env config manually
Copy the CHANNEL_SECRET and CHANNEL_ACCESS_TOKEN into the env config 
![image](https://user-images.githubusercontent.com/24865458/172822152-c5c3c5ee-c135-4857-a692-052e23556956.png)

## Add the build pack
```
heroku/python
https://github.com/heroku/heroku-buildpack-chromedriver
https://github.com/heroku/heroku-buildpack-apt
https://github.com/heroku/heroku-buildpack-google-chrome
```

![image](https://user-images.githubusercontent.com/24865458/209175654-15cae34f-9076-4641-b9c0-faa79f7dc0b1.png)

## Steps
1. Copy this repo

    ```gh repo clone brianoy/auto_roll_call```

2. Set the remote to the heroku

    ```heroku login```

    ```heroku git:remote -a [your_app_name]```

3. Deploy the app on heroku

    Save all the file```Ctrl + S```

    ```git add .```

    ```git commit -m "update"```

    ```git push -u heroku```


## Result
https://line.me/R/ti/p/%40963ypagh

**Heroku had changed their terms of use, free Heroku Dynos are no longer available. This line-bot might not respond any more.**

