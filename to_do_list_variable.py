from pip import main


def variable_separator():
    separator = """
          {
            "type": "separator"
          }"""
    return separator

def variable_block():
    block = """{
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "order",
                "color": "#aaaaaa",
                "size": "md",
                "flex": 0,
                "gravity": "center",
                "align": "start",
                "position": "relative"
              },
              {
                "type": "text",
                "text": "name",
                "wrap": true,
                "color": "#666666",
                "size": "md",
                "gravity": "center"
              },
              {
                "type": "text",
                "text": "date",
                "wrap": true,
                "color": "#666666",
                "size": "xs",
                "gravity": "center",
                "flex": 0
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "postback",
                      "label": "刪除",
                      "data": "delete_data"
                    },
                    "height": "sm",
                    "gravity": "center",
                    "style": "primary"
                  }
                ],
                "width": "30%",
                "flex": 0
              }
            ]
          }"""
    return block

def variable_main_construct():
  main_construct = """{
    "type": "bubble",
    "size": "giga",
    "hero": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "filler"
        }
      ]
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "線上行事曆",
          "weight": "bold",
          "size": "xl"
        },
        {
          "type": "box",
          "layout": "vertical",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            main_construct
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "spacing": "sm",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "filler"
            }
          ],
          "margin": "sm"
        }
      ],
      "flex": 0
    }
  }"""
  return main_construct
