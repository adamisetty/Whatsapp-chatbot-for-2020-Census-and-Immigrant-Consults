from flask import Flask, request
from WhatsappChatbot.TFIDF.Transformer import Transformer
from twilio.twiml.messaging_response import MessagingResponse
from language_detector import detect_language

app = Flask(__name__)
transformer = Transformer('WhatsappChatbot/data/train/QnA.csv', 'WhatsappChatbot/data/train/ChineseQnA.txt', 'WhatsappChatbot/data/train/SpanishQnA.csv')

numbers = []
greetings = {'English': 'Hello! Nice to meet you!', 'Spanish':'¡Mucho gusto! ¿Cómo estás?', 'Mandarin':'您好！很高兴为您服务'}

@app.route('/', methods=['POST'])
def bot():
    #full_msg = request.values
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    number = request.values.get('From', '')
    if not number in numbers:
        #signifies first message
        language = detect_language(incoming_msg)
        if language in greetings.keys():
            response = greetings.get(language)
        else:
            response = "I do not understand this language, let's proceed in English \n"
            response = response + greetings.get('English')
        msg.body(response)
        numbers.append(number)
        responded = True

    if not (incoming_msg == None or incoming_msg == '') and not responded:
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

