from flask import Flask, request
from WhatsappChatbot.TFIDF.Transformer import Transformer
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
transformer = Transformer('WhatsappChatbot/data/train/QnA.csv', 'WhatsappChatbot/data/train/ChineseQnA.txt', 'WhatsappChatbot/data/train/SpanishQnA.csv')

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
        response, similarity = transformer.match_query(incoming_msg)
        if similarity < 0.5:
            response = "Please wait! Our representative is on the way to help you!"
            msg.body(response)
        else:
            responses = response.split('|')
            response = ''
            for r in responses:
                if r != '':
                    response = response + '\n' + r.strip()
            msg.body(response)
        responded = True

    if not responded:
        msg.body('Sorry, I cannot understand your message')
    return str(resp)


if __name__ == '__main__':
    app.run()

