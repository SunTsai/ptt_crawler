from flask import Flask, request, abort

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from db_controller import DB_Controller
from linebot_api import LineBot

app = Flask(__name__)

linebot = LineBot()

@app.route('/', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        linebot.handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@linebot.handler.add(MessageEvent, message=TextMessage)
def handle_message(event):    
    results = DB_Controller().search_by_keyword(event.message.text)
    titles = []
    if len(results) == 0:
        linebot.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='找不到相關的標題')
        )

    for result in results:
        text = result[0]
        url = result[1]
        titles.append(TextSendMessage(text=f'{text}\n{url}'))

    print(event.source.user_id)
        
    linebot.line_bot_api.reply_message(
        event.reply_token,
        titles
    )
    
if __name__ == "__main__":
    app.run()