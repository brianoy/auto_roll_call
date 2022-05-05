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