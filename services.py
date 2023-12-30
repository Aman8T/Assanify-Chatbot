from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAEdqkBTO0YBALmjtqH25q8U5ByE1l7mjT23w1jlYOvwxd0qpzOIpVeazHsy2eZCx8ZCUWlEw9V2ZBW2FOZCoeSUX6LCrw0KP9GZARQ75DD1aRkRXxwJXUkZBG3QW4KaNZCpk4VNufxwEx0cLOYkcNhY24poMH4R8I4PVHUiUGrnYTwRPLFt7ZCBTnLurwDKnz9spanjifJOnQZDZD"
VERIFY_TOKEN = "asanify"

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post(" https://graph.facebook.com/v13.0/105358718868002/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/webhook', methods=['GET'])
def handle_verification():
    print(f"handle_verification::whatsapp::{request.args}")
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        print('Hi')
        return request.args.get('hub.challenge')
    else:
        return "Invalid verification token"


@app.route('/webhook', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message)

    return "ok"


if __name__ == '__main__':
    app.run(debug=True, port=5002)