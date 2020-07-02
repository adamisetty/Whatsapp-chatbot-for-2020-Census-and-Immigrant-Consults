from flask import Flask, request
from WhatsappChatbot.TFIDF.Transformer import Transformer
from twilio.twiml.messaging_response import MessagingResponse
from langdetect import detect

app = Flask(__name__)
transformer = Transformer('WhatsappChatbot/data/train/QnA.csv', 'WhatsappChatbot/data/train/SimplifiedChineseQnA.csv', 'WhatsappChatbot/data/train/traditionalChineseQnA.csv', 'WhatsappChatbot/data/train/SpanishQnA.csv')

numbers = []
greetings =  {'en': 'Hello! Nice to meet you!', 'es':'¡Mucho gusto! ¿Cómo estás?', 'zh-cn':'您好！很高兴为您服务'}
passings = {'en': 'Sorry, I did not understand your question. ',
            'es': 'Lo siento, no entiendo su pregunta', 'zh-cn': '请稍候，工作人员正在接通中。'}

@app.route('/', methods=['POST'])
def bot():

    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    number = request.values.get('From', '')
    if not (incoming_msg == None or incoming_msg == ''):
        response, similarity = transformer.match_query(incoming_msg)
        print("similarity: ", similarity)
        re = ''
        # signifies first message in a conversation
        if not number in numbers and similarity < 0.5:
            #print("number: ", number)
            language = detect(incoming_msg)
            #print("language:", language)
            if language in greetings.keys():
                re = greetings.get(language)
            else:
                re = re + greetings.get('en')
            msg.body(re)
            numbers.append(number)
            responded = True
        if not responded:
            if similarity < 0.5:
                language = detect(incoming_msg)
                if language in passings.keys():
                    re = passings.get(language)
                else:
                    re = passings.get('en')
                msg.body(re)
            else:
                responses = response.split('|')
                re = ''
                for r in responses:
                    if r != '':
                        re = re + '\n' + r.strip()
                msg.body(re)
            responded = True

    if not responded:
        msg.body('Sorry, I cannot understand your message')
    return str(resp)


if __name__ == '__main__':
    app.run()

