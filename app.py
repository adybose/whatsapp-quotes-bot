from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Sorry, I could not retrieve a quote at this time. Please try again later.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if any('hi', 'hello') in incoming_msg:
        msg.body('Hi there! I am a bot that can send you quotes and cat pics. All you need is ask!')
        responded = True
    if not responded:
        msg.body('Sorry! I can only serve you famous quotes and cat pics.')
    return str(resp)


if __name__ == '__main__':
    app.run()
