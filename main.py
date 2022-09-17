from email import message
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)

import config as cf

app = Flask(__name__)

line_bot_api = LineBotApi(cf.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(cf.CHANNEL_SECRET)

# endpoint from linebot
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# handle message from LINE
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)

    with open("./static/" + event.message.id + ".jpg", "wb") as f:
        f.write(message_content.content)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="写真を取得しました。"))


if __name__ == "__main__":
    app.run(port="8000")
