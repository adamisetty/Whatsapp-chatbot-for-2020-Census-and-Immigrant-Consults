from flask import Flask, request
from FBMessengerChatbot.TFIDF.Transformer import Transformer
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
transformer = Transformer('FBMessengerChatbot/data/train/QnA.csv')

@app.route('/', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if not (incoming_msg == None or incoming_msg == ''):
        response = transformer.match_query(incoming_msg)
        msg.body(response)
        responded = True

    if not responded:
        msg.body('Sorry, I cannot understand your message')
    return str(resp)


if __name__ == '__main__':
    app.run()

