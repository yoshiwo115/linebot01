from flask import Flask, request, abort
import os
import logging
import sys

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
# ログを標準出力に出力する
app.logger.addHandler(logging.StreamHandler(sys.stdout))
# （レベル設定は適宜行ってください）
app.logger.setLevel(logging.INFO)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
#ACCESS_TOKEN 乗っ取りを防ぐ

@app.route("/")
def hello_world():
    return "オウム返しのラインボットを作りました"

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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage) #Messageが来たとき、start()追加された時などもある
def handle_message(event):
    reply_text = event.message.text #コメントを抜き出す
	if "好き" or "すき" or "スキ" in event.message.text:
		reply_text= "私もよ"
	else:
		reply_text= event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text) #Messageが来たとき、これを送る
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
