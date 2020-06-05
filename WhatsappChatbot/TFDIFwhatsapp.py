from flask import Flask, request
from WhatsappChatbot.TFIDF.Transformer import Transformer
from twilio.twiml.messaging_response import MessagingResponse
from langdetect import detect

app = Flask(__name__)
transformer = Transformer('WhatsappChatbot/data/train/QnA.csv', 'WhatsappChatbot/data/train/ChineseQnA.txt', 'WhatsappChatbot/data/train/SpanishQnA.csv')

numbers = []
greetings =  {'en': 'Hello! Nice to meet you!', 'es':'¡Mucho gusto! ¿Cómo estás?', 'zh-cn':'您好！很高兴为您服务'}
passings = {'en': 'Please wait! Our representative is on the way to help you!',
            'es': 'Por favor espera, nuestro representante te ayudará', 'zh-cn': '请稍候，工作人员正在接通中。'}

@app.route('/', methods=['POST'])
def bot():

    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    number = request.values.get('From', '')
    # signifies first message in a conversation
    if not number in numbers:
        language = detect(incoming_msg)
        if language in greetings.keys():
            response = greetings.get(language)
        else:
            response = "I do not understand this language, let's proceed in English \n"
            response = response + greetings.get('en')
        msg.body(response)
        numbers.append(number)
        responded = True

    if not (incoming_msg == None or incoming_msg == '') and not responded:
        response, similarity = transformer.match_query(incoming_msg)
        if similarity < 0.5:
            language = detect(incoming_msg)
            if language in passings.keys():
                response = passings.get(language)
            else:
                response = passings.get('en')
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

