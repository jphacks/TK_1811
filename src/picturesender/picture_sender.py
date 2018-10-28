#coding:utf-8



from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError,
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, Error, ImageSendMessage
)
from linebot.__about__ import __version__

from linebot.http_client import HttpClient, RequestsHttpClient
import os,sys
import json
import requests

AWS_S3_BUCKET_NAME = 'pictures'

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler      = WebhookHandler(os.environ["CHANNEL_SECRET"])

EC2_ADDR = 'tawashi.biz:5050'


@app.route('/')
def connect_test():
    return "access success!"

@app.route("/callback",methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: "+ body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# messageが送られてきたら...
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''
    self._post('/v2/bot/message/reply', data=json.dumps(data), timeout=timeout)
    '''
    if(event.message.text == "写真ちょうだい"):
        send_images(event)
    elif(event.message.text == "写真リセットして"):
        reset_images(event)
    else:
        echo(event)

def echo(event):
    reply_token = event.reply_token
    messages = TextSendMessage(text=event.message.text)
    app.logger.info("DEBUG:" + event.message.text)
    line_bot_api.reply_message(reply_token, messages)

def send_images(event):
    reply_token = event.reply_token
    #filename_l = get_images_from_server()
    messages = [ImageSendMessage(
        original_content_url="https://tawashi.biz/images/1.jpg", #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url="https://tawashi.biz/images/1.jpg" #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    ),
    ImageSendMessage(
        original_content_url="https://tawashi.biz/images/2.jpg", #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url="https://tawashi.biz/images/2.jpg" #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    ),
    ImageSendMessage(
        original_content_url="https://tawashi.biz/images/3.jpg", #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url="https://tawashi.biz/images/3.jpg" #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    )]

    #messages = TextSendMessage(text=ret_str)
    line_bot_api.reply_message(reply_token, messages)

def reset_images(event):
    delete_images_on_server()
    reply_token = event.reply_token
    messages = TextSendMessage(text='写真を全て削除しました')
    app.logger.info("DEBUG:" + event.message.text)
    line_bot_api.reply_message(reply_token, messages)    

def get_images_from_server():
    url_items = 'http://' + EC2_ADDR +'/get_list'
    r_json = requests.get(url_items).json()
    ls = r_json["data"]
    
    return ls
    


    

def delete_images_on_server():
    url_items = 'https://' + EC2_ADDR +'/delete'
    requests.post(url_items)
    

if __name__ == "__main__":
    port = int(os.getenv("PORT",5000))
    app.run(debug=False,host="0.0.0.0",port=port)
   
