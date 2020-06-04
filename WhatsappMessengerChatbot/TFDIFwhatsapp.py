from flask import Flask, request
from WhatsappMessengerChatbot.TFIDF.Transformer import Transformer
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
transformer = Transformer('WhatsappMessengerChatbot/data/train/QnA.csv')

@app.route('/', methods=['POST'])
def bot():
    full_msg = request.values
    print("full message: ", full_msg)
    incoming_msg = request.values.get('Body', '').lower()
    print("incoming msg: ", incoming_msg)
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

