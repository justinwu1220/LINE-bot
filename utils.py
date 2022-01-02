import os

from linebot import LineBotApi, WebhookParser
from linebot.models import *


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_multi_text_message(reply_token, text_arr):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, text_arr)

    return "OK"

def push_text_message(text):
    uid = "Ubd57dd263acc2367bddc6c01f886fed3"
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(uid, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token, content_arr):
    message_arr=[]
    for content in content_arr:
        acts = [URITemplateAction(
                    label="觀看",
                    uri=content[0]
                )]
        message = TemplateSendMessage(
            alt_text='Button_Template',
            template=ButtonsTemplate(
                thumbnail_image_url=content[1],
                text=content[2]+"\n"+content[3]+"\n"+content[4],
                actions=acts
            )
        )
        message_arr.append(message)

    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message_arr)

    return "OK"

def push_button_message(content):
    uid = "Ubd57dd263acc2367bddc6c01f886fed3"
    acts = [URITemplateAction(
                label="觀看",
                uri=content[0]
            )]
    message = TemplateSendMessage(
        alt_text='Template',
        template=ButtonsTemplate(
            thumbnail_image_url=content[1],
            text=content[2]+"\n"+content[3]+"\n"+content[4],
            actions=acts
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(uid, message)

    return "OK"


'''
def send_flex_message(reply_token, obj):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, FlexSendMessage("new msg", obj))
    
    return "OK"
'''

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
