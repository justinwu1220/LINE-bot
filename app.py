import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message


load_dotenv()


machine = TocMachine(
    states=["awake", "command_failed", "new_anim", "search_anim", "today_anim", "hot_anim", "searching"],
    transitions=[

        {
            "trigger": "get_msg",
            "source": "awake",
            "dest": "new_anim",
            "conditions": "is_getting_new"
        },
        {
            "trigger": "get_msg",
            "source": "awake",
            "dest": "hot_anim",
            "conditions": "is_getting_hot"
        },
        {
            "trigger": "get_msg",
            "source": "awake",
            "dest": "today_anim",
            "conditions": "is_getting_today"
        },
        {
            "trigger": "get_msg",
            "source": "awake",
            "dest": "command_failed",
            "conditions": "is_getting_nothing"
        },
        {
            "trigger": "finished",
            "source": ["new_anim", "searching", "today_anim", "hot_anim", "command_failed"],
            "dest": "awake",
        },
        {
            "trigger": "get_msg",
            "source": "awake",
            "dest": "search_anim",
            "conditions": "is_getting_search"
        },
        {
            "trigger": "get_msg",
            "source": "search_anim",
            "dest": "searching",
        },

    ],
    initial="awake",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        machine.get_msg(event)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.getenv("PORT", None)
    app.run(host="0.0.0.0", port=port, debug=True)
    #machine.get_graph().draw("fsm.png",prog="dot",format="png")
